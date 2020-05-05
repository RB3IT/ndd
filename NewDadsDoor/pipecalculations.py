## This Module
from NewDadsDoor.constants import *
from NewDadsDoor import classes

## Builtin
import functools

def setpipewidth(door):
    """ Sets the default width for a pipe """
    if not door.pipe:
        raise ValueError("Door does not have a pipe")
    ## Our default is simply 2 inches longer than the opening width
    door.pipe.pipewidth = door.clearopening_width + 2.0

def validate_assembly_pipe(pipe):
    """ Validation method for Asssembly Generation Functions """
    if pipe is None: pipe = PIPESIZES[max(PIPESIZES)]
    if isinstance(pipe,str):
        if pipe in PIPELOOKUP: pipe = PIPELOOKUP[pipe]
        else:
            try: pipe = int(pipe)
            except: pass
    if isinstance(pipe,int):
        if pipe in PIPESIZES: pipe = PIPESIZES[pipe]
    if isinstance(pipe,dict) and 'size' in pipe:
        pipe = classes.Pipe(shell = pipe['size'])
    if not isinstance(pipe,classes.Pipe):
        raise ValueError("Invalid Pipe")
    return pipe

def validate_compound_assemblies(func):
    """ Validation decorator for centralized validation """
    @functools.wraps(func)
    def inner(torque,turns,*,pipe = None,**kw):

        def validator(assembly):
            """ The actual validation function """
            if not all(socket.validate(turns) for socket in assembly.sockets):
                #print("fail 1")
                #for socket in assembly.sockets:
                    #print(socket)
                return False
            if not all(all(spring.validatemaxturns(turns) for spring in socket) for socket in assembly.sockets):
                #print("fail 2")
                return False
            if not assembly.validatetorque(torque):
                #print("fail 3")
                return False
            return True

        assemblies = func(torque = torque, turns = turns, pipe = pipe,**kw)
        #print(func)
        return list(filter(validator,assemblies))
    return inner

def assemblywrapper(func):
    """ Since the most common case is a single Socket in an Assembly, this function can
        be used to wrap functions to automatically convert Socket results into Assemblies
        via convertassembly. """
    
    @functools.wraps(func)
    def inner(*args,**kw):
        result = func(*args,**kw)
        return convertassembly(result)
    return inner

def convertassembly(springs):
    """ Takes an item and attempts to coerce it into an Assembly instance.
    
        Inputs Supported:
            Assemblies
            Lists of Sockets
            Lists of Springs
            Lists of Lists of Springs
    """
    def convertitem(item):
        """ Convenience Function """
        ## We don't recurse for Springs (which would then convert to Assembly) 
        ## because this Spring may be part of a list of single-spring sockets
        if isinstance(item,classes.Spring):
            return classes.Socket(item)
        ## Sockets get converted to Assemblies
        if isinstance(item,classes.Socket):
            assembly = classes.Assembly()
            assembly.addsocket(item)
            return assembly
        ## Assemblies are already in the end state
        if isinstance(item,classes.Assembly):
            return item
        ## Lists that are passed to this function should only contain Sockets
        ## (which are used to construct an Assembly)
        if isinstance(item,(list,tuple)):
            if not all(isinstance(x,classes.Socket) for x in item):
                raise ValueError(f"Lists should only contain Sockets: {item}")
            asssembly = classes.Assembly()
            for socket in item: assembly.addsocket(socket)
            return assembly
        ## Anything else is an Exception
        raise ValueError(f"Invalid Item: {item}")
    def sortout(item):
        """ Separate sorting function for recurse-ability """
        ## Springs and Sockets should be unlikely, but both are converted first to a Socket in
        ## convertitem, which then recurses
        if isinstance(item,(classes.Spring,classes.Socket)): return sortout(convertitem(item))
        ## We don't have to worry about wrapping it
        if isinstance(item,classes.Assembly): return output.append(item)
        ## Handle Lists
        if isinstance(item,(list,tuple)):
            ## List is an unassembled Assembly
            if all(isinstance(x,(classes.Socket,classes.Spring)) for x in item):
                out2 = []
                for x in item:
                    if isinstance(x,classes.Spring):
                        x = convertitem(x)
                    ## There should only be sockets now
                    out2.append(convertitem(x))
                ## sortout the Assembly created by convertitem(list_of_sockets)
                ## This should probably just be rewritten to "return output.append(convertitem(out2))"
                ## but we're going to throw it back through incase convertitem returns a bad value
                return sortout(convertitem(out2))
            ## Lists of Assemblies are flattened
            if all(isinstance(x,classes.Assembly) for x in item):
                for x in item: output.append(x)
                return
        ## Everything else are Exceptions
        raise ValueError(f"Could not sort item: {item}")

    output = []
    if not isinstance(springs, (list,tuple)):
        springs = [springs,]
    for out in springs:
        sortout(out)
    return output
        

def get_all_compounds(pipe = None):
    """ Based on the given pipe, return a list of all 2-Spring Compound sockets that will fit inside.
   
        This only validates that each inner wire will fit inside the outer wire and that 
        the outerwire will fit inside the pipe: it DOES NOT validate that the given
        set of springs will be valid for any given amount of required torque (if at all).
    """
    pipe = validate_assembly_pipe(pipe)
    output = _get_all_compound_springs(pipe = pipe)
    return [classes.Socket(*[classes.Spring(**spring, cycles = pipe.cycles) for spring in springs]) for springs in output]

def _get_all_compound_springs(pipe = None):
    """ For extension and testing purposes, the body of get_all_compounds was extracted so that its output is Class Agnostic.

        This function returns tuple-pairs of dicts (outer,inner) -> {wire:wirediameter [float], od:wire_od [float]}
    """
    pipe = validate_assembly_pipe(pipe)
    maxindex = max([i for i,od in enumerate(WIREODINDEX) if od <= pipe.max_wireod])
    ## If we can only use the smallest OD, then we can't generate any Compounds
    if maxindex < 1: return []

    output = []

    ## Stop before the smallest OD
    outerods = WIREODINDEX[maxindex:0:-1]
    for out_od in outerods:
        #print()
        #print(out_od)
        out_wires = [wire for wire in WIRE.values() if wire['min_od'] <= out_od]
        for outer in out_wires:
            #print(">>>",outer['wirediameter'])
            outerspring = classes.Spring(wire = outer, od = out_od, cycles = pipe.cycles)

            id = outerspring.id
            #print(">>>>>>>",id)
            ## Try for every possible id
            for in_od in [od for od in WIREODINDEX if od < id]:
                #print(">>>>>>>>>>>",in_od)
                ## Inner Wires are a natural subset of Outer Wires
                in_wires = [wire for wire in out_wires if wire['min_od'] <= in_od]
                for inner in in_wires:
                    #print(">>>>>>>>>>>>>>>",inner['wirediameter'])
                    ospring = dict(wire = outer['wirediameter'], od = out_od)
                    ispring = dict(wire = inner['wirediameter'], od = in_od)

                    output.append((ospring, ispring))
    ## NOTE: I don't think this should ever need to be pared down (i.e.- I don't
    ##       think it will ever produce duplicates) but it's something to keep in mind
    return output

def get_rti(o,i):
    """ Helper function to get the Ratio of Torque for a Compound Socket """
    ## RTI = RMD * RWD**5
    ## RMD = Outer.md / Inner.md
    ## RWD = Inner.wirediameter / Outer.wirediameter
    rti = (o.md / i.md) * (i.wirediameter / o.wirediameter)**5
    return rti

@assemblywrapper
def generate_all_assemblies(torque, turns, pipe = None):
    """ Runs all assembly creation methods and returns a list of valid assemblies
    
        All assembly creation methods require torque per turn and total turns. Pipe is optional
        and should either be a  Pipe instance, a Pipe Dict (as per PIPELOOKUP/PIPESIZE),
        or an str or int that can be used as a key for PIPELOOKUP/PIPESIZE.
    """
    output = []
    for fun in [generate_single_spring,
                generate_compound_rti,
                generate_compound_general,
                ]:
        res = fun(torque,turns,pipe = pipe)
        #print(fun,res)
        output.extend(res)

    return output

@assemblywrapper
def generate_single_spring(torque, turns, pipe = None):
    """ Generates a list of valid Assemblies """
    pipe = validate_assembly_pipe(pipe)
    od = max([od for od in WIREODINDEX if od <= pipe.max_wireod])
    ## Get a list of springs that will fit inside the OD
    potential_springs = [classes.Spring(wire = wire['wirediameter'], od = od, cycles = pipe.cycles) for wire in WIRE.values() if wire['min_od'] <= od]
    ## Set length of all springs to match torque
    for spring in potential_springs: spring.setlengthbytorque(torque)
    ## Validate springs
    valid_springs = list(filter(lambda spring: spring.validatemaxturns(turns),potential_springs))
    ## Return valid springs
    return valid_springs

@validate_compound_assemblies
@assemblywrapper
def generate_compound_rti(torque,turns,pipe = None):
    """ Uses the inhouse Compound Torque Ratio (RTI) """
    pipe = validate_assembly_pipe(pipe)
    sockets = get_all_compounds(pipe)
    out = []
    for socket in sockets:
        o,i = socket.springs
        rti = get_rti(o,i)
        ## TRU = TPT / (RTI + 1)    ## Torque Required for Outer
        ## TRI = TRU * RTI          ## Torque Required for Inner
        tru = torque / (rti + 1)
        tri = tru * rti
        o.setlengthbytorque(tru)
        i.setlengthbytorque(tri)
        
        out.append(socket)

    return out

@validate_compound_assemblies
@assemblywrapper
def generate_compound_general(torque,turns,pipe = None):
    """ Uses the old method for constructing a Compound Assembly """
    pipe = validate_assembly_pipe(pipe)
    for wire in [wire for wire in iterwire(reverse= True) if wire['min_od'] <= pipe.max_wireod]:
        spring = classes.Spring(wire, od = pipe.max_wireod, cycles= pipe.cycles)
        ## Strongest a spring can be is when turns is equal to max turns
        ## Max turns is MP / Torque, therefore Torque = MP / Max Turns
        ## 1.05 is a safety factor (increased from 1.015)
        st = spring.mp / turns / 1.05
        ## If outerwire can do all the pulling itself, we won't return it with this method
        ## (generate_single_springs will return it)
        if st >= torque * .95:
            continue
        spring.setlengthbytorque(st)
        #print(torque, st, spring.lift)
        remaining = torque - spring.lift
        maxod = max(od for od in SPRINGOD if od and od < spring.id)
        modmp = turns * remaining / pipe.cyclerating
        inners = [wire for wire in iterwire(reverse = True) if wire['min_od'] <= maxod and wire['mp_base'] > turns * remaining / pipe.cyclerating]
        for inner in inners:
            innerspring = classes.Spring(inner, od = maxod, cycles = pipe.cycles)
            innerspring.setlengthbytorque(remaining)
            assembly = classes.Socket(spring,innerspring)


            if assembly.validate(turns):
                return assembly
    
    ## TODO: Mostly a placeholder; not sure whether to raise Exception if no compounds generated or just return an empty list.
    return []
