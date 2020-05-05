""" NewDadsDoor.methods

    A collection of useful methods/algorythms for creating doors.
    See NewDadsDoor.calculations for methods used in calculating aspects of a door.

"""

## This Module
from NewDadsDoor import calculations, classes, constants, pipecalculations
## Builtin
import collections
## Third Party
from alcustoms.text import format_list_to_columns

def create_curtain(door,slattype = None, gauge = None, endlocks = None, windlocks = None):
    """ Helper function to autopopulate a Torsion Spring Door's Curtain.

        This function will replace any existing curtain on the door with
        a curtain containing sufficient slats of the given type (default
        2-1/2 Flat with default endlocks for that slattype) and a
        standard Bottom Bar.
    """
    if not isinstance(door,classes.Door):
        raise ValueError("create_curtain requires a door object")
    if slattype is None: slattype = "brd"
    slat = classes.Slat(slattype, gauge = gauge)
    door.curtain = None
    door.setcurtain()
    curtain = door.curtain
    slats = classes.SlatSection(curtain, slat = slat)
    if endlocks is None:
        endlocks = slat.defaultendlocks
    slats.endlockpattern = classes.EndlockPattern(endlocks, windlocks = windlocks)
    curtain.append(slats)
    bottombar = classes.BottomBar(slat, curtain)
    curtain.append(bottombar)
    slats.slats = slats.getnumberslats(curtain.curtainshort())
    return curtain

def create_tracks(door, stopsize = None):
    if not isinstance(door, classes.Door):
        raise ValueError("create_tracks requires a door object")
    tracks = classes.Tracks(door, stopsize = stopsize)
    door.tracks = tracks
    guideheight = door.clearopening_height + tracks.stopsize
    tracks.inner = guideheight
    tracks.outer = guideheight
    tracks.wall = door.wall_length()
    return tracks

def basic_torsion_door(width, height, slat = None, endlocks = None, bracketplates = None):
    """ Constructs a basic Torsion Spring Door from the provided information.

        width and height are required and are clear opening sizes.
        slat and endlocks defaults to the defaults for create_curtain,
        which is used to create the curtain.
        bracketplates is an optional size for the bracketplates.
    """
    door = classes.Door(height,width)
    if bracketplates:
        door.bracketplatesize = bracketplates
    create_tracks(door)
    create_curtain(door, slattype = slat, endlocks = None)
    door.sethood()
    smallest = get_smallest_pipe(door)
    if smallest:
        pipe = door.setpipe(shell = constants.PIPESIZES[smallest])

    else:
        pipe = door.setpipe(shell = constants.PIPESIZES[max(constants.PIPESIZES)])
    pipe.width = pipecalculations.setpipewidth(door)

    return door

def get_smallest_pipe(door):
    """ Returns the smallest pipe size required for the given door (None if no assemblies could be generated). """
    oldpipe = door.pipe
    if oldpipe:
        width = oldpipe.width
    else:
        width = door.maxpipewidth()

    assembly = None
    pipes = [pipe for size,pipe in constants.PIPESIZES.items()]
    try:
        while not assembly and pipes:
            door.pipe = pipe = classes.Pipe(shell = pipes.pop(0)['size'], pipewidth = width)
            assembly = get_lightest_assembly(door)
        if not assembly: return None
        return door.pipe.size
    finally:
        door.pipe = oldpipe


def get_lightest_assembly(door):
    assemblies = pipecalculations.generate_all_assemblies(door.torqueperturn, door.totalturns, door.pipe)
    if not assemblies: return
    assemblies = sorted(assemblies,key = lambda assem: assem.weight)

    oldassembly = door.pipe.assembly
    try:
        for assembly in assemblies:
            door.pipe.assembly = assembly
            if door.validatepipesize() and door.validatepipeassembly():
                return assembly
    finally:
        door.pipe.assembly = oldassembly

def output_all_door_calculations(door):
    if not isinstance(door,classes.Door):
        raise TypeError(f"door must be Door type, not '{door.__class__.__name__}'")
    output = {v:None for v in [
        "Clear Opening Height", "Clear Opening Width", "Stop Size", "Upset", "Bracket Plate Height", "Bracket Plate Width", "Guide Height", "Wall Angle Height",
        "Pipe Diameter", "Pipe Length", "Barrel Rings", "Overall Pipe Radius", "Casting Sets", "Total Casting Lengths", "Springs", "Total Spring Length", "Shaft Length",
        "Height to Pipe Centerline", "Height to Stops", "Wrap Length", "Slat Type", "Slat Gauge", "Slat Height", "Slat Weight", "Slats to Stops", "Slats for Wrap", "Total Slats",
        "Slat Length", "Bottom Bar Weight", "Curtain Weight Closed", "Curtain Weight Open", "Initial Lever Arm", "Slat Increase Radius", "Final Lever Arm", "Turns to Raise", "Turns to Hold",
        "Total Turns", "Torque Required Open", "Torque Required Closed", "Average Torque Per Turn"
        ]}
    output["Clear Opening Height"], output["Clear Opening Width"] = door.clearopening_height, door.clearopening_width
    output["Upset"],output["Open Height"] = door.upset, door.openheight
    if door.tracks:
        output["Stop Size"] = door.tracks.stopsize
        output["Guide Height"], output["Wall Angle Height"] = door.tracks.guide_height, door.tracks.wall.length
    if door.bracketplate:
        output["Bracket Plate Height"], output["Bracket Plate Width"] = door.bracketplate.height, door.bracketplate.width
    if door.pipe:
        pipe = door.pipe
        output["Pipe Diameter"], output["Pipe Length"] = pipe.size, pipe.pipewidth
        output["Barrel Rings"], output["Overall Pipe Radius"] = pipe.barrelrings, pipe.totalradius
        if pipe.assembly:
            assembly = pipe.assembly
            castings = [socket.castings for socket in assembly.sockets if socket.castings]
            output["Casting Sets"], output["Total Casting Lengths"] = len(castings), sum([casting.outside_length for casting in castings])
            springs = sum([socket.springs for socket in assembly.sockets if socket.springs],[])
            output["Springs"] = len(springs)
            output["Shaft Length"] = assembly.length(door.turnstoraise)
    output["Height to Pipe Centerline"], output["Height to Stops"] = door.pipecenterlineheight, door.stopheight
    output["Wrap Length"] = door.getwraplength()
    if door.curtain:
        slats = door.curtain.slatsections()
        if slats:
            slats = slats[0]
            output["Slat Type"], output["Slat Height"], output["Slat Weight"] = slats.slat.slattype, slats.slat.slatheight, slats.slat.slatweight
            output["Slats to Stops"], output["Slats for Wrap"], output["Total Slats"] = slats.gethangingslats(), slats.getwrapslats(), slats.getnumberslats()
            output["Slat Gauge"], output["Slat Increase Radius"] = slats.slat.gauge, slats.slat.increaseradius
            output["Slat Length"] = slats.slatlength
        bottombar = door.curtain.bottombars()
        if bottombar:
            output["Bottom Bar Angle"], output["Bottom Bar Angle W/F"], output["Bottom Bar Weight"] = bottombar[0].angle,bottombar[0].angleweight, bottombar[0].weight
        output["Curtain Weight Closed"], output["Curtain Weight Open"] = door.curtain.weight_closed, door.curtain.weight_open
    output["Initial Lever Arm"], output["Final Lever Arm"] = door.initialradius, door.finalradius
    output["Turns to Raise"], output["Turns to Hold"], output["Total Turns"] = door.turnstoraise, door.preturns, door.totalturns
    output["Torque Required Open"], output["Torque Required Closed"], output["Average Torque Per Turn"] = door.requiredtorque_open, door.requiredtorque_closed, door.torqueperturn
    return output

def format_adc_output(output, columns = 2, width = 80):
    """ Converts the return of output_all_door_calculations() into a multiline string.

        output should be the output to convert.
        columns is number of output values per line.
        Each line is 80 characters long and whitespace will be used to align the columns.
    """
    o = [f"{k}: {v}" for k,v in output.items()]
    r = format_list_to_columns(o,columns, width = width, orientation = "rows")
    return r

def build_sockets(springs, castings):
    """ Builds Sockets from a list of springs and a corresponding list of Castings.
    
        springs should be a list of classes.Spring instances.
        castings should be a list of dictionaries taken from constants.CASTINGS or
        the string ['name'] value taken from that list.
        Returns a list of castings.
        Castings without Springs will simply be discarded.
        At least one Pipe Casting is required if any Springs are passed.
        Every Spring requires a Spring Casting.
        If the Springs and either type of Castings are mismatched (either too many
        of one or not enough) a ValueError is raised.
    """
    if not all(isinstance(spring, classes.Spring) for spring in springs):
        raise TypeError("Springs should be a list of Spring objects.")

    _c = []
    for casting in castings:
        ## Check if castings are strings and try to convert them if necessary.
        casting = convert_to_casting(casting)
        _c.append(casting)
    castings = _c
    del _c

    ## Sort Castings into pipe/spring types
    pipecastings, springcastings = [],[]
    for casting in sorted(castings, key = lambda casting: max(casting['ods']), reverse = True):
        if casting['type'] == 'pipe': pipecastings.append(casting)
        else: springcastings.append(casting)

    ## If there are no Springs, we can return an empty list since all
    ## Castings are extra and therefore disregarded
    if not springs: return []
    ## There should be atleast one Pipe Casting
    if len(pipecastings) < 1:
        raise ValueError("At least one Pipe Casting is required")
    ## Every spring should have its own Spring Casting
    if len(springs) != len(springcastings):
        raise ValueError("Insufficient Spring Castings")

    ## Sort Springs by OD, wire, and coiledlength (largest->smallest on all categories)
    springs = sorted(
        sorted(
            sorted(springs, key = lambda spring: spring.coiledlength, reverse = True),
            key = lambda spring: spring.wirediameter, reverse = True),
        key = lambda spring: spring.od, reverse = True)
    sockets = []
    """ Dev Note: Algorithm
        ( While Pipe Casting and Springs:
            Check Socket:
                If no socket: pop Pipe casting
            ( for Springs
                Check Next Spring:
                    Check pipe casting fit
                    Check previous spring fit
                If Next Spring:
                    ( for spring castings
                        Check next Spring Casting fit
                    )
            )
            If not Spring and Spring Casting:
                If Pipe Casting doesn't have a single successful spring:
                    raise Error
                add Socket to output
                clear socket
                continue from beginning
            Pop Spring and Spring Casting
            Add Spring and Spring Casting to Socket
            If no slots open on Socket:
                add Socket to output
                clear socket
        )
    """
    socket = None
    while (socket or pipecastings) and springs:
        if not socket:
            pipecasting = pipecastings.pop(0)
            castingset = classes.CastingSet(pipecasting)
            socket = classes.Socket(castings = castingset)
        
        spring = None
        springcasting = None
        for pospring in springs:
            ## If pipe casting can't accept the spring, skip it
            if pospring.od not in pipecasting['ods'][len(socket.springs):]: continue
            ## If previous spring can't accept the spring, skip it
            if socket.springs and socket.springs[-1].id < pospring.od: continue
            ## Otherwise we can find a spring casting for it
            for pocast in springcastings:
                if pospring.od in pocast['ods']:
                    springcasting = pocast
                    break
            if springcasting:
                spring = pospring
                break

        if not spring or not springcasting:
            ## Socket does not have any springs at all
            if not socket.springs:
                raise ValueError("Mismatched Pipe Casting")
            ## Socket is not a compound: store and restart with no socket
            sockets.append(socket)
            socket = None
            continue

        springs.remove(spring)
        springcastings.remove(springcasting)
        socket.addspring(spring)
        castingset.addcasting(springcasting)

        ## Socket is full: store and restart with no socket
        if len(socket.springs) == socket.castings.maxsprings:
            sockets.append(socket)
            socket = None
            continue

    ## Mismatched Springs
    if springs:
        raise ValueError(f"Mismatched Springs: {springs}")
    ## Mismatched Spring Castings
    if springcastings:
        raise ValueError("Mismatched Spring Castings: {springcastings}")

    ## If there's an open socket, add it to output
    if socket:
        sockets.append(socket)
    

    return sockets


def getcasting(*springs):
    """ Attempts to select castings for the given springs """
    if not springs: return None
    nsprings = len(springs)
    springods = sorted([spring.od for spring in springs])
    castings = [casting for casting in constants.CASTINGS if casting['type'] == "pipe"
                    and casting['springs'] >= nsprings
                    and all(od in casting['ods'] for od in springods)]
    ## There's a possibility we don't have a matching casting, so return None
    if not castings:
        return None
    ## We only have just so many casting options at this point... only one is going to work
    pipecasting = castings[0]

    springcastings = []
    for od in springods:
        castings = [casting for casting in constants.CASTINGS if casting['type']  == "spring"
                          and od in casting['ods']]
        ## As above, maybe we don't have a valid casting: return None
        if not castings:
            return None
        ## Pick the casting with the smallest loss of space
        ## As above,this maya s well be castings[0]
        springcastings.append(min(castings,key = lambda casting: casting['innerloss']))
    return classes.CastingSet(pipecasting,*springcastings)

def convert_to_casting(casting):
    """ Converts a string or dict into a casting dict (enforcing keys and data types)
    
        casting should be a string or a dict. If it is a string it should be a name of
        a casting dict in NDD.constants.CASTINGS. If it is a dict, it should conform
        to the specifications noted above CASTINGS.
    """
    if isinstance(casting, str):
        if casting not in constants.CASTINGLOOKUP:
            raise ValueError(f"Invalid Casting Name: {casting}")
        return constants.CASTINGLOOKUP[casting]
    if not isinstance(casting,dict):
        raise TypeError(f"Invalid Casting: should be a string Casting Name or a dict representing a Casting, not {casting.__class__.__name__}")
    output = {}
    ## This dict was originally made to be used with a generic type-checking algorythm,
    ## but this ended up getting dropped for the time being and we're checking manually
    ## TODO: revisit the possiblity in the future
    CASTINGTYPING = {"name":str, "type":["pipe","spring"], "springs": int, "ods":{list:float},
                     "castingod":float, "length":float, "innerloss": float, "weight": float}
    missingkeys = [key for key in CASTINGTYPING if key not in casting]
    if missingkeys:
        raise ValueError(f"Casting is missing the following keys: {', '.join(missingkeys)}")

    if not isinstance(casting['name'],str):
        raise TypeError("Casting name should be  a non-empty string")
    if not casting['name']:
        raise TypeError("Casting name should be  a non-empty string")
    if casting['type'] not in ["pipe","spring"]:
        raise ValueError("Casting type should be either 'pipe' or 'spring'")
    if not isinstance(casting['springs'], int):
        raise TypeError("Casting springs should be an integer")
    if not isinstance(casting['ods'], list):
        raise TypeError("Casting ods should be a list of floats")
    if not casting['ods']:
        raise ValueError("Casting ods should not be an empty list")
    if not all(isinstance(od, float) for od in casting['ods']):
        raise TypeError("Casting ods must be floats")
    if not isinstance(casting['castingod'], float):
        raise TypeError("Casting castingod should be float")
    if not isinstance(casting['length'], float):
        raise TypeError("Casting length should be a float")
    if not isinstance(casting['innerloss'], float):
        raise TypeError("Casting innerloss should be a float")
    if not isinstance(casting['weight'], float):
        raise TypeError("Casting weight should be a float")


    return {k:casting[k] for k in CASTINGTYPING}