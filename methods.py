""" NewDadsDoor.methods

    A collection of useful methods/algorythms for creating doors.
    See NewDadsDoor.calculations for methods used in calculating aspects of a door.

"""

from NewDadsDoor import classes, constants

def create_curtain(door,slattype = None, endlocks = None):
    """ Helper function to autopopulate a Torsion Spring Door's Curtain.

        This function will replace any existing curtain on the pipe with
        a curtain containing sufficient slats of the given type (default
        2-1/2 Flat with default endlocks for that slattype) and a
        standard Bottom Bar.
    """
    if not isinstance(door,classes.Door):
        raise ValueError("create_curtain requires a door object")
    if slattype is None: slattype = "brd"
    slat = classes.Slat(slattype)
    door.curtain = None
    door.setcurtain()
    curtain = door.curtain
    slats = classes.SlatSection(curtain, slat = slat)
    if endlocks is None:
        slats.endlockpattern = classes.EndlockPattern(slat.defaultendlocks)
    else:
        slats.endlockpattern = classes.EndlockPattern(endlocks)
    curtain.append(slats)
    bottombar = classes.BottomBar(slat, curtain)
    curtain.append(bottombar)
    slats.slats = slats.getnumberslats(curtain.curtainshort())

def basic_torsion_door(width, height, slat = None, endlocks = None):
    """ Constructs a basic Torsion Spring Door from the provided information.

        width and height are required and are clear opening sizes.
        slat and endlocks defaults to the defaults for create_curtain,
        which is used to create teh curtain.
    """
    door = classes.Door(height,width)
    create_curtain(door, slattype = slat, endlocks = None)
    door.sethood()
    smallest = get_smallest_pipe(door)
    if smallest:
        pipe = door.setpipe(shell = constants.PIPESIZES[smallest])

    else:
        pipe = door.setpipe(shell = constants.PIPESIZES[max(constants.PIPESIZES)])

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
    assemblies = classes.generate_all_assemblies(door.torqueperturn, door.totalturns, door.pipe)
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