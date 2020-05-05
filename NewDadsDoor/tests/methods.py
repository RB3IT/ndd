## This Package
from NewDadsDoor import classes
## Builtin
from collections import namedtuple
import functools
from itertools import zip_longest
## 3rd Party
from alcustoms import methods as almethods

Difference = namedtuple("Difference",["type","difference"])

def format_comparison(objs):
    """ Formats comparison as a strings """
    def formatter(comp):
        if not isinstance(comp, tuple):
            return str(comp)
        output = []
        return "\n".join([comp.type] + ["    "+errmessage for errmessage in output])

    results = map(formatter,objs)
    return "\n".join(results)
        
        #obj1,obj2 = comp


        ### Sections
        #for i,s1,s2 in diffs:
        #    if s1 and s2:
        #        output.append(f"Section {i} does not match:")
        #        result = compare_sections(s1,s2)
        #        output.extend(almethods.linepadder(result))
        #    else:
        #        if s1:
        #            output.append(f"Door 2 missing Section {i}")
        #        else:
        #            output.append(f"Door 1 missing Section {i}")
        
def none_comparison(func):
    """ Catches a difference when one or both of the objects are None (since it is handled the same across methods) """
    @functools.wraps(func)
    def inner(obj1,obj2):
        if obj1 is not None and obj2 is not None:
            return func(obj1, obj2)
        if obj1 is None and obj2 is None:
            return []
        if obj1 is not None and obj2 is None:
            return Difference(f"Second {obj1.__class__.__name__} is None",(obj1,None))
        return Difference(f"First {obj2.__class__.__name__} is None",(None,obj2))
    return inner

def attr_comparison(obj1,obj2,attrs):
    """ Compares Attributes between 2 objects via getattr, returning the attribute values as a tuple if they do not match """
    return [Difference(f"{obj1.__class__.__name__}.{attr}",(result1,result2)) for attr in attrs if (result1 := getattr(obj1,attr)) != (result2 := getattr(obj2,attr))]
def sub_comparison(obj1,obj2,translate):
    """ Given a list of tuples comparised of (subcomparison method, attr name for comparison), returns any Difference tuple retunred by each method using the given attr of obj1 and obj2 as arguments (if that method is not None) """
    return [Difference(f"{obj1.__class__.__name__} > {meth.__name__}",result) for (meth,attr) in translate if (result := meth(getattr(obj1,attr),getattr(obj2,attr))) is not None]
def list_comparison(list1,list2, differencetype):
    list1,list2 = list(list1), list(list2)
    diffs = []
    for item in list1:
        if item in list2:
            list2.remove(item)
        else:
            diffs.append(item)

    diffs = [(1,item) for item in diffs]
    diffs.extend([(2,item) for item in list2])

    return [Difference(differencetype, diff) for diff in diffs]

@none_comparison
def compare_door(door1,door2):
    attrs = ["clearopening_height","clearopening_width","bracketplatesize","upset","mounting"]
    diffs = attr_comparison(door1,door2,attrs)
    ## Output these methods instead
    translate = [
        (compare_curtain, "curtain"),   ## door.curtain
        (compare_pipe, "pipe"),          ## door.pipe
        (compare_tracks, "tracks"),    ## door.tracks
        (compare_hood, "hood")]          ## door.hood
    diffs.extend(sub_comparison(door1,door2,translate))
    return diffs

@none_comparison
def compare_curtain(curtain1,curtain2):
    sections = zip_longest(curtain1.sections, curtain2.sections)
    diffs = [(i,compare_sections(s1,s2)) for i,(s1,s2) in enumerate(sections, start = 1) if s1!=s2]
    return [Difference("Curtain",diff) for diff in diffs]

@none_comparison
def compare_sections(section1, section2):
    attrs = ["increaseradius","height","weight","bottomheight"]
    if isinstance(section1,classes.BottomBar) or isinstance(section2,classes.BottomBar):
        if not isinstance(section1, classes.BottomBar) or not isinstance(section2, classes.BottomBar):
            return [Difference("Section Type", (section1.__class__.__name__,section2.__class__.__name__)),]
        attrs.extend(["feederslatweight","angle","edge","slope"])
    elif isinstance(section1,classes.SlatSection) or isinstance(section2, classes.SlatSection):
        if not isinstance(section1, classes.SlatSection) or not isinstance(section2, classes.SlatSection):
            return [Difference("Section Type", (seciton1.__class__.__name__, section2.__class__.__name__)),]
        attrs.extend(["slat","slats","endlockpattern"])
    return attr_comparison(section1,section2,attrs)

@none_comparison
def compare_pipe(pipe1, pipe2):
    attrs = ["pipewidth","shell","assembly","barrelrings","cycles","adjuster"]
    diffs = attr_comparison(pipe1, pipe2, attrs)
    translate = [
        (compare_shell, "shell"),           ## Shell
        (compare_assembly, "assembly")]  ## Assembly
    diffs.extend(sub_comparison(pipe1,pipe2,translate))
    return diffs

@none_comparison
def compare_shell(shell1,shell2):
    ## Dev Note: currently shells are just Dictionary Constants
    if shell1 == shell2: return []
    return [Difference("Shell", (shell1,shell2)),]

@none_comparison
def compare_assembly(assembly1, assembly2):
    ## Dev Note: Sockets do not have to be in the same order and therefore are
    ## not compared positionallly
    diffs = []
    sockets1, sockets2 = list(assembly1.sockets), list(assembly2.sockets)

    for socket in sockets1:
        if socket in sockets2:
            socket2.remove(socket)
        else:
            diffs.append(socket)
    ## Tracking which Assembly they came out of
    diffs = [(1,socket) for socket in diffs]
    diffs.extend([(2,socket) for socket in sockets2])
    
    return [Difference("Assembly Extra Socket",diff) for diff in diffs]

@none_comparison
def compare_tracks(tracks1, tracks2):
    attrs = ["inner","outer","wall","stopsize"]
    return attr_comparison(tracks1,tracks2,attrs)

@none_comparison
def compare_hood(hood1, hood2):
    attrs = ["width","baffle","shape"]
    return attr_comparison(hood1,hood2,attrs)

@none_comparison
def compare_socket(socket1,socket2):
    ## Dev Note: Unlike other compare_ methods, this is not used by it's parent
    ## object (i.e.- compare_assembly) because sockets do are not compared
    ## positionally (simply the presence or absence of a socket matters)
    
    ## Dev Note 2: There is no need to compare Springs or Castings positionally
    ## as there is exactly one valid order that any set of Springs or Castings 
    ## can have within a single socket

    springs1,castings1,springs2,castings2 = list(socket1.springs), list(socket1.castings.castings), list(socket2.springs),list(socket2.castings.castings)
    springdiffs = list_comparison(springs1,springs2,"Extra Spring")
    castingdiffs = list_comparison(castings1,castings2,"Extra Casting")

    return [Difference("Socket Difference",diff) for diff in springdiffs + castingdiffs]