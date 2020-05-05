## Builtin
import functools
import inspect
import math

## Custom Module
from alcustoms import methods as almethods
from alcustoms import measurement

## This Module
from NewDadsDoor.constants import *
from NewDadsDoor import calculations, methods, pipecalculations

"""
NOTES

Abbreviation Comments (i.e.- LI, OD, TQ) are original Spring Program variable names preserved for backreference.

Initial/Final Lever Arm:
    When looking at source material, you may see "Final" and "Initial" Lever Arm listed.
    The Lever Arm, in basic terms, is the radius of the Pipe/Wrap: it is the length of
    the "arm" that is leveraging the weight around the axis. This means that the
    "Initial Lever Arm"- the length of the radius when the door is closed,unwrapped-
    is the radius of the pipe (with Barrel Rings, if available) and the
    "Final Lever Arm"- or the Lever Arm when the door is open- is this length plus the
    Increase in Radius from the slats wrapped around pipe.
"""

###################################################
"""
               MISC Classes and Functions
                                                """
###################################################

def measurementconversion(function):
    """ A Wrapper which checks if an instance method's 'value' argument and tries to convert it to a measurement.ImperialMeasure object.
    """
    sig = inspect.signature(function)
    @functools.wraps(function)
    def inner(*args,value=None,**kw):
        ba = sig.bind(*args,**kw)
        ba.apply_defaults()
        if ba.arguments.get("value"):
            value = ba.arguments.get("value")
            ## Ints should be floats for measurement.Imperial
            if isinstance(value, int): value = float(value)
            try: ba.arguments['value'] = measurement.Imperial(value)
            except Exception as e: pass
        return function(*ba.args,**ba.kwargs)
    return inner

class Angle():
    def __init__(self,leg1, leg2, thickness, length):
        self._material = "steel"
        self._leg1 = 3
        self._leg2 = 3
        self._thickness = '1/8in'
        self._length = None

    @property
    def leg1(self):
        return self._leg1
    @property
    def leg2(self):
        return self._leg2
    @property
    def thickness(self):
        return self._thickness
    @property
    def length(self):
        return self._length

    @leg1.setter
    @measurementconversion
    def leg1(self,value):
        self._leg1 = value
    @leg2.setter
    @measurementconversion
    def leg2(self,value):
        self._leg2 = value
    @thickness.setter
    @measurementconversion
    def thickness(self,value):
        self._thickness = value
    @length.setter
    @measurementconversion
    def length(self,value):
        self._length = value

###################################################
"""
                    DOOR CLASSES
                                                """
###################################################

class Door():
    def __init__(self, clearopening_height, clearopening_width, upset = None, mounting = "interior"):
        self.pipefactory = Pipe
        self.curtainfactory = Curtain
        self.tracksfactory = Tracks
        self.hoodfactory = Hood
        self._curtain = None
        self._pipe = None
        self._tracks = None
        self._hood = None
        self._clearopening_height = 0
        self.clearopening_height = clearopening_height
        self._clearopening_width = 0
        self.clearopening_width = clearopening_width
        self._bracketplatesize = BRACKETPLATESIZE
        if upset is None: upset = .25
        self.upset = upset
        self.mounting = mounting
        self.accessories = list()

    @property
    def curtain(self):
        return self._curtain
    @curtain.setter
    def curtain(self,value):
        if value is None:
            self._curtain = None
            return
        if not isinstance(value,Curtain): raise AttributeError("Door's curtain must be Curtain Instance")
        self._curtain = value
        self.curtain.door = self
    @property
    def pipe(self):
        return self._pipe
    @pipe.setter
    def pipe(self,value):
        if value:
            if not isinstance(value,Pipe): raise AttributeError("Door's pipe must be Pipe Instance")
            self._pipe = value
            self.pipe.door = self
        else:
            self._pipe = None

    @property
    def hood(self):
        return self._hood
    @hood.setter
    def hood(self,value):
        if not isinstance(value,Hood): raise AttributeError("Door's hood must be Hood Instance")
        self._hood = value
        self._hood.door = self
    @property
    def tracks(self):
        return self._tracks
    @tracks.setter
    def tracks(self,value):
        if not isinstance(value,Tracks): raise AttributeError("Door's tracks must be Tracks Instance")
        self._tracks = value
        self._tracks.door = self

    def setall(self):
        """ Calls all constructor functions of Door
        
            Does not accept any arguments: component properies must be edited separately
        """
        self.settracks()
        self.setpipe()
        self.setcurtain()
        self.sethood()

    def setcurtain(self,**kw):
        """ A constructor function to initialize and add a curtain
        
        Does not accept positional arguments.
        """
        if not self.curtainfactory: raise AttributeError("Door's curtainfactory is not set")
        curtain = self.curtainfactory(door = self,**kw)
        self.curtain = curtain
        return curtain

    def setpipe(self,**kw):
        """ A constructor function to initialize and add a pipe 
        
        Does not accept positional arguments,
        """
        if not self.pipefactory: raise AttributeError("Door's pipefactory is not set")
        pipe = self.pipefactory(door = self, **kw)
        self.pipe = pipe
        return pipe

    def sethood(self,**kw):
        hood = Hood(**kw)
        self.hood = hood
        return hood

    def settracks(self,**kw):
        if not self.tracksfactory: raise AttributeError("Door's trackfactory is not set")
        tracks = self.tracksfactory(**kw)
        self.tracks = tracks
        return tracks

    @property
    def clearopening_height(self):
        return self._clearopening_height
    
    @clearopening_height.setter
    @measurementconversion
    def clearopening_height(self,value):
        if not isinstance(value,measurement.Imperial):
            raise TypeError(f"Invalid clearopening_height (should be Imperial): {value}({value.__class__.__name__})")
        self._clearopening_height = value

    @property
    def clearopening_width(self):
        return self._clearopening_width
    
    @clearopening_width.setter
    @measurementconversion
    def clearopening_width(self,value):
        if not isinstance(value,measurement.Imperial):
            raise TypeError(f"Invalid clearopening_width (should be Imperial): {value}({value.__class__.__name__})")
        self._clearopening_width = value

    @property
    def bracketplatesize(self):
        if not self._bracketplatesize: return 18
        return self._bracketplatesize

    @bracketplatesize.setter
    @measurementconversion
    def bracketplatesize(self,value):
        if value and not isinstance(value,(int,float, measurement.Measurement)):
            raise AttributeError("Door.bracketplatesize must be a size or None")
        if not value:
            self._bracketplatesize = None
        else:
            self._bracketplatesize = value

    @property
    def bracketplate(self):
        return BracketPlate(size = self.bracketplatesize)

    @property
    def openheight(self):
        """ Returns the distance between the bottom of the curtain and the center of the bracket plates when the door is open

        Note that for a door with standard upset, bracket plates, and bottomabar this number
        is constant regardless of size of door
        """
        return calculations.curtain_openheight(self.pipecenterlineheight, self.stopheight, self.curtain.bottomheight)

    @property
    def stopheight(self):
        """ The height at which the Stops engage the bottom bar (or other stop) """
        return self.tracks.guide_height - self.tracks.stopsize

    @property
    def initialradius(self): ## IR
        """ Initial Lever Arm/Initial distance from center of pipe to pipe centerline """
        return self.pipe.totalradius

    @property
    def betweenbrackets(self): ## GR
        pass

    @property
    def finalradius(self): ## FL
        """ Final Lever Arm/Final distance from center of pipe to pipe centerline """
        return calculations.curtain_finalradius(self.initialradius, self.turnstoraise, self.curtain.increaseradius)

    @property
    def hangingweight_closed(self): ## HW
        """ Total weight of the Curtain (when closed)"""
        return self.curtain.getweight(self.pipecenterlineheight)

    @property
    def hangingweight_open(self): ## WU
        """ Weight of the Curtain when the door is Open with safety factor """
        return calculations.safetyfactor_curtain_hangingweight_open(self.curtain.weight_open,self.stopheight)

    @property
    def pipecenterlineheight(self): ## HC
        """ Height from the floor to the center of the Pipe """
        ## Stop Height + Upset + Half Bracket Plate Height (Pipe is centered on bracket plates)
        return calculations.pipe_centerlineheight(self.stopheight, self.tracks.stopsize, self.upset, self.bracketplate.height/2)

    def wall_length(self):
        """ Returns the necessary height to cover the openheight, stops, upset, and Bracket Plates """
        return calculations.tracks_wall_length(self.stopheight, self.upset, self.bracketplate.height)

    @property
    def preturns(self): ## PT
        """ Number of turns required in order to achieve requiredtorque_open """
        return calculations.pipe_preturns(self.requiredtorque_open, self.torqueperturn)

    @property
    def requiredtorque_closed(self): ## TD
        """ Required amount of force required to lift door while closed """
        return calculations.pipe_requiredtorque_closed(self.initialradius, self.hangingweight_closed)

    @property
    def requiredtorque_open(self): ## TU
        """ Required amount of force required to hold the door open """
        return calculations.pipe_requiredtorque_open(self.finalradius, self.hangingweight_open)

    @property
    def torqueperturn(self): ## IP
        """ The amount of torque (inch/pound) for each turn (IPPT in handbook) """
        return calculations.pipe_torqueperturn(self.requiredtorque_closed, self.requiredtorque_open, self.turnstoraise)

    @property
    def totalturns(self): ## TT
        """ Total number of time the pipe will be turned """
        return calculations.pipe_totalturns(self.turnstoraise, self.preturns)

    @property
    def turnstoraise(self): ## TR
        """ Number of Barrel Rotations required to fully raise the door (TR) """
        return calculations.door_turnstoraise(self.stopheight, self.pipe.totalradius, self.curtain.increaseradius)

    def getwraplength(self):
        """ Gets the calculated distance for the wrap """

        ## If no pipe is available, we'll go with the default wrap length
        if not self.pipe: return calculations.curtain_getwraplength_estimate(self.curtain.slatsections()[0].slat.slatheight)

        return calculations.curtain_getwraplength(self.pipecenterlineheight - self.stopheight, self.pipe.totalradius, self.pipe.getadjusterratio())

    def validatepipesize(self):
        return calculations.validation_pipesize(self.pipe.weight, self.hangingweight_closed, self.pipe.maxdeflectionweight)

    def validatepipeassembly(self):
        """ Returns whether the pipe's assembly is valid for the given curtain. """
        return self.pipe.assembly.validate(ippt = self.torqueperturn, turns = self.totalturns)

    def validatepipeassembly(self):
        """ Returns whether the pipe's assembly is valid for the given curtain. """
        return self.pipe.assembly.validate(ippt = self.torqueperturn, turns = self.totalturns)

    def maxpipewidth(self):
        """ Calculates the maximum width for the pipe between the brackets. """
        return self.clearopening_width + 2

    def __eq__(self,other):
        if isinstance(other,Door):
            return all(getattr(self,attr) == getattr(other,attr) for attr in ["curtain","pipe","tracks","hood","clearopening_height","clearopening_width","bracketplatesize","upset","mounting"])

    def __repr__(self):
        return f"{self.clearopening_width}x{self.clearopening_height} {self.__class__.__name__} Object"

class FireDoor(Door): pass

class BracketPlate():
    """ At current, this class isn't really necessary. However it is used to follow
    the heavily object-oriented philosophy of this module
    """
    def __init__(self,size):
        """ Creates a new BracketPlate with the given size

        Bracket Plates are Square, so BracketPlate.height and BP.width
        will both equal BP.size
        """
        self.size = size
    @property
    def height(self):
        return self.size
    @property
    def width(self):
        return self.size

class Hood():
    def __init__(self,door = None, width = None, baffle = False, shape = None):
        self._door = None
        self.door = door
        self._width = width
        self._baffle = False
        self.baffle = baffle
        self._shape = None
        self.shape = shape

    @property
    def door(self):
        return self._door
    @door.setter
    def door(self,value):
        if value and not isinstance(value,Door):
            raise AttributeError("Hood's door must be a Door instance")
        self._door =value

    @property
    def baffle(self):
        return self._baffle
    @baffle.setter
    def baffle(self,value):
        if not isinstance(value,bool):
            raise AttributeError("Hood baffle must be a boolean")
        self._baffle = value


    @property
    def shape(self):
        return self._shape
    @shape.setter
    def shape(self,value):
        if value and not isinstance(value,str):
            raise AttributeError("Hood shape must be a string")
        self._shape = value

    @property
    def width(self):
        if not self.door and self._width: return None
        if not self._width and self.door:
            return self.door.clearopening_width + HOODEXTENSION
        return self._width

    def __eq__(self,other):
        if isinstance(other, Hood):
            return all(getattr(self,attr) == getattr(other,attr) for attr in ["width","baffle","shape"])

class Tracks():
    
    type = "3 Piece Tracks"
    def __init__(self,door = None, inner = None, outer = None, wall = None, stopsize = None):
        self.door = door
        self._inner = None
        self._outer = None
        self._wall = None

        self.inner = inner
        self.outer = outer
        self.wall = wall

        self._stopsize = None
        if stopsize is None:
            stopsize = 2.0
        self.stopsize = stopsize

    @property
    def outer(self):
        return self._outer
    @property
    def inner(self):
        return self._inner
    @property
    def wall(self):
        return self._wall
    @property
    def stopsize(self):
        return self._stopsize
    @outer.setter
    @measurementconversion
    def outer(self,value):
        if value is None:
            self._outer = None
            return
        if isinstance(value,measurement.Measurement):
            length = value
            value = self.get_default("outer")
            value.length = length
        if not isinstance(value,Angle):
            raise ValueError(f"Invalid Outer Angle: {value}")
        self._outer = value
    @inner.setter
    @measurementconversion
    def inner(self,value):
        if value is None:
            self._inner = None
            return
        if isinstance(value,measurement.Measurement):
            length = value
            value = self.get_default("inner")
            value.length = length
        if not isinstance(value,Angle):
            raise ValueError(f"Invalid Inner Angle: {value}")
        self._inner = value
    @wall.setter
    @measurementconversion
    def wall(self,value):
        if value is None:
            self._wall = None
            return
        if isinstance(value,measurement.Measurement):
            length = value
            value = self.get_default("wall")
            value.length = length
        if not isinstance(value,Angle):
            raise ValueError(f"Invalid Wall Angle: {value}")
        self._wall = value
    @stopsize.setter
    @measurementconversion
    def stopsize(self,value):
        if value is None:
            self._stopsize = None
            return
        if not isinstance(value, measurement.Measurement):
            raise TypeError(f"Invalid stopsize: {value}")
        self._stopsize = value
        
    @property
    def guide_height(self):
        return self.outer.length

    def get_default(self, angle):
        """ Return an angle appropriate for the given piece of Track.

            angle should be "outer","inner", or "wall".
            The returned angle will have a length of 0.
        """
        if angle not in ["outer","inner","wall"]:
            raise AttributeError(f"Invalid guide piece: {angle}")
        if angle == "outer" or angle == "wall":
            return Angle(3,3,3/16,0)
        else:
            return Angle(3,2,3/16,0)

    def __eq__(self,other):
        if isinstance(other, Tracks):
            return all(getattr(self,attr) == getattr(other,attr) for attr in ["inner","outer","wall","stopsize"])
 
class ExtrudedGuides(Tracks):
    """ TODO """
    
    type = "Extruded Tracks"


class Curtain():
    """ A Container object for collecting sections
    """
    def __init__(self, door):
        self.door = door
        self._sections = list()

    def slatlength(self,section):
        """ A Curtain's Slat length is often wider than the width """
        endlocks = getattr(section,"endlockpattern",None)
        windlocks = None
        if endlocks:
            windlocks = endlocks.windlocks
            endlocks = endlocks.endlock.endlocktype
        slattype = getattr(section,"slattype", self.slattype)
        tracks = self.door.tracks
        if tracks: tracks = tracks.type
        return calculations.curtain_slatlength(self.door.clearopening_width, slattype= slattype, endlocks = endlocks, windlocks = windlocks, tracks = tracks)

    def getweight(self,height):
        """ Returns the weight of the curtain at a certain height (assumes that any additional weight is supported by the pipe (as opposed to springs) """
        weight = 0
        ## For each section, what portion of the remaining height the section will fill
        for section in reversed(self.sections):
            heightportion = min(height,section.height)
            height -= heightportion
            weight += section.weight * (heightportion / section.height)
        return weight

    @property
    def weight_closed(self):
        return self.getweight(self.door.pipecenterlineheight)

    @property
    def weight_open(self):
        return self.getweight(self.door.openheight)

    @property
    def bottomheight(self):
        ## Determine stop-point
        stoppoint = None
        for section in self.sections:
            if section.bottomheight is not None:
                stoppoint = True
                break
        ## If not stoppoint, curtain will keep spinning
        if not stoppoint: raise AttributeError("No section found with bottomheight value (curtain will keep spinning)")
        
        index = self.index(section)
        height = 0
        ## Add heights from bottom section to bottomheight-section
        ## Will not include that section just yet
        for bottom in self.sections[-1:index:-1]: height += bottom.height

        ## Now add that section's bottomheight
        return height + section.bottomheight

    @property
    def increaseradius(self):
        return max(section.increaseradius for section in self)

    @property
    def sections(self):
        return list(self._sections)

    def slatsections(self):
        """ Returns a list of all SlatSection subclass instances in the Curtain. """
        return [section for section in self.sections if isinstance(section,SlatSection)]

    def bottombars(self):
        """ Returns a list of all BottomBar subclass instances in the Curtain
            (generally, there should be at most one)
            
        """
        return [section for section in self.sections if isinstance(section, BottomBar)]

    @property
    def slattype(self):
        types = {section.slat.slattype for section in self.slatsections()}
        if len(types) == 1:
            return list(types)[0]
        raise ValueError("Cannot Determine Slattype of a curtain with multiple slattypes.")

    @property
    def curtainheight(self):
        """ Returns the height of the entire curtain (including wrap) """
        return sum(section.height for section in self.sections)

    def curtainshort(self):
        """ Takes the height of all Sections and compares it to the required length to complete the door. """
        requiredheight = self.door.pipecenterlineheight + self.door.getwraplength()
        return requiredheight - self.curtainheight

    def insert(self,index,section):
        if not isinstance(section,Section):
            raise TypeError("Requires Section-type object.")
        self._sections.insert(index,section)
        section.curtain = self

    def append(self,section):
        if not isinstance(section,Section):
            raise TypeError("Requires Section-type object")
        self._sections.append(section)
        section.curtain = self

    def index(self,section):
        return self._sections.index(section)

    def remove(self,section):
        return self._sections.remove(section)

    def __eq__(self,other):
        if isinstance(other, Curtain):
            return self.sections == other.sections

    def __getitem__(self,key):
        return self._sections[key]
    def __contains__(self,*args,**kw):
        return self._sections.__contains__(*args,**kw)
    def __len__(self,*args,**kw):
        return self._sections.__len__(*args,**kw)
    def __iter__(self,*args,**kw):
        return self._sections.__iter__(*args,**kw)

    def __repr__(self):
        return f"Curtain Object ({len(self.sections)} sections)"

class Section():
    def __init__(self,curtain=None):
        self.curtain = curtain

    @property
    def increaseradius(self):
        return 0

    @property
    def weight(self):
        return 0

    @property
    def height(self):
        return 0

    @property
    def bottomheight(self):
        return None
    
class BottomBar(Section):
    def __init__(self, slatweight, curtain=None, angle = None, edge = None, slope = 0):
        super().__init__(curtain=curtain)
        if isinstance(slatweight,Slat): slatweight = slatweight.slatweight
        if not isinstance(slatweight,(int,float)):
            raise ValueError("Invalid Slat Weight")
        self.feederslatweight = slatweight
        if angle is None: angle = '2" x 2" x 1/8" STEEL'
        self.angle = angle
        if edge not in BOTTOMEDGELOOKUP: edge = None
        self.edge = edge
        self.slope = slope
    @property
    def height(self):
        return BOTTOMBARLOOKUP[self.angle]['height'] + self.getedgeheight()
    @property
    def weight(self):
        ## Bottom Bar Weights were originally per-foot  (self.curtainclearopening/12)
        return (self.angleweight +
                self.getedgeweight())\
                    *self.slatlength/12 + \
                    self.slopeweight + \
                    self.getfeederslatweight()
    
    @property
    def bottomheight(self):
        """ Provides the Stop Height adjustment for Large Tubular Bottom Bars (returns 0 otherwise) """
        if "large tubular" in self.angle: return 3.5
        return 0

    @property
    def angleweight(self):
        """ Returns the angle weight per foot """
        return BOTTOMBARLOOKUP[self.angle]['angleweight']

    def getedgeheight(self):
        """ Returns height added by a Safety Edge (if any) """
        return BOTTOMEDGELOOKUP[self.edge]['height'] if self.edge else 0

    def getedgeweight(self):
        """ Returns the (safety) edge weight-per-foot, if any """
        return BOTTOMEDGELOOKUP[self.edge]['edgeweight'] if self.edge else 0

    def getfeederslatweight(self):
        """ Returns the weight of the feeder slat (not a property to avoid conflict with feederslatweight attribute) """
        return calculations.bottombar_feederslatweight(self.feederslatweight, self.slatlength)

    @property
    def slopeweight(self):
        """ Returns the weight added by the slopped portion of the bottom bar """
        if not self.slope: return 0
        return calculations.bottombar_slopeweight(self.slatlength, self.slope)

    @property
    def slatlength(self):
        return self.curtain.slatlength(self)

    def __eq__(self,other):
        if isinstance(other,BottomBar):
            return all(getattr(self,attr) == getattr(other,attr) for attr in ["feederslatweight","angle","edge","slope"])

    def __repr__(self):
        return f"{self.__class__.__name__} Object"

class SlatSection(Section):
    def __init__(self, curtain=None, endlockpattern = None, slats = 0, slat = None):
        super().__init__(curtain=curtain)
        if isinstance(endlockpattern,Endlock):
            endlockpattern = EndlockPattern(endlockpattern)
        if not endlockpattern is None and not isinstance(endlockpattern,EndlockPattern):
            raise AttributeError("endlockpattern must be None or EndlockPattern instance")
        self.endlockpattern = endlockpattern
        self.slats = slats
        self._slat = None
        if slat is None: slat = Slat("2 1/2 INCH FLAT SLAT")
        self.slat = slat

    @property
    def height(self):
        if not self.slats: return 0
        return self.slats * self.slat.slatheight

    @property
    def weight(self):
        return self.getslatweight(self.slats) + self.getendlockweight()

    @property
    def slattype(self):
        return self.slat.slattype

    @property
    def slatlength(self):
        if self.curtain:
            return self.curtain.slatlength(self)
        return 0

    @property
    def slat(self): return self._slat
    @slat.setter
    def slat(self,slat):
        if not isinstance(slat,Slat):
            slat = Slat(slat)
        self._slat = slat

    def getnumberslats(self,height = None):
        """ Returns the number of slats needed for the given height, rounding up """
        if height is None:
            height = self.curtain.door.stopheight + self.curtain.door.getwraplength()
        return math.ceil(height / self.slat.slatheight)

    def gethangingslats(self,height = None):
        if height is None: height = self.curtain.door.stopheight
        return self.getnumberslats(height)

    def getwrapslats(self,height = None):
        if height is None:
            height = self.curtain.door.getwraplength()
        return self.getnumberslats(height)

    def getslatweight(self,slats):
        """ Returns the slat weight given the number of slats """
        return slats * self.slatlength * self.slat.slatweight

    def getendlockweight(self, slats = None):
        if not self.endlockpattern: return 0
        if slats is None: slats = self.slats
        return self.endlockpattern.getweight(math.ceil(slats/2))

    @property
    def increaseradius(self):
        return self.slat.increaseradius

    def __repr__(self):
        return f"{self.__class__.__name__} Object ({self.slattype}{' x' + str(self.slats) if self.slats else ''})"

class PerforatedSlats(SlatSection):
    def __init__(self, curtain=None, endlockpattern = None, slats = 0, slattype = None, slatgauge = None):
        super().__init__(curtain=curtain, endlockpattern=endlockpattern, slats=slat, slattype=slattype, slatgauge=slatgauge)
    @property
    def slatlength(self):
        endlocks = getattr(section,"endlockpattern",None)
        windlocks = None
        if endlocks:
            windlocks = endlocks.windlocks
            endlocks = endlocks.endlock
        slattype = getattr(section,"slattype")
        return calculations.curtain_slatlength_perforatedslats(self.door.clearopening_width, slattype= slattype, endlocks = endlocks, windlocks = windlocks, tracks = tracks)

    @property
    def weight(self):
        return super().weight() - self.perforatedweightloss
    @property
    def perforationsperslat(self):
        """ Determine number of perforation Windows based on Curtain Width """
        return calculations.curtain_perforationsperslat(self.slatlength)

    @property
    def perforatedweightloss(self):
        ## (Slat Weight per Window-size) * Weight Loss Per Window *  Number of perforations/Slat * Number of Slats
        return calculations.curtain_perforatedweightloss(self.slat.slatweight, self.curtain.perforationsperslat, self.slats)


class RollingGrilleSection(Section):
    def __init__(self, curtain=None, rodtype="ALUM. LINKS/PLASTIC TUBES", rods = 0, lexaninserts = False):
        super().__init__(curtain=curtain)
        self.rodtype = rodtype
        self.rods = rods
        self.lexaninserts = lexaninserts
    @property
    def rodsize(self):
        if self.lexaninserts: return 3
        return 2.25
    @property
    def rodweight(self):
        if self.lexaninserts: return RODLOOKUP["LEXAN INSERTS"]['rodweight']
        return RODLOOKUP[self.rodtype]['rodweight']
    @property
    def height(self):
        return self.getheight(self.rods)
    @height.setter
    def height(self,value):
        """ Sets number of rods based on provided height (rounding up) """
        if height < 0: raise ValueError("Height must be a positive number")
        self.rods = math.ceil(self.getnumberrods(height))
    @property
    def weight(self):
        return self.rods * self.rodweight * self.width
    def getheight(self,rods = None):
        """ Gets height based on number of rods """
        if rods is None: rods = self.rods
        ## Rod Height is 3 inches if lexaninserts
        return self.rodsize * rods - 1
    def getnumberrods(self,height):
        """ Gets number of rods based on height. Does NOT round up. """
        return height / self.rodsize

class Slat():
    def parsetype(slattype):
        """ Attempts to determine the base Slat type of the given value and returns a Slat instance with the default gauge for that type """
        slattypecheck = checkslattype(slattype)
        if not slattypecheck:
            ## We'll assume slattype is a number cast as something else
            try:
                if isinstance(slattype,str):
                    slattype = int(slattype.strip())
                else:
                    slattype = int(slattype)
                slattype = SLATINDEXCONVERSION[slattype]
            except:
                raise ValueError("Could not determine type of Slat")
        else: slattype = slattypecheck
        return slattype

    def __init__(self, slattype = None, gauge = None):
        if slattype is None: slattype = "2 1/2 INCH FLAT SLAT"
        if slattype not in SLATLOOKUP:
            slattype = Slat.parsetype(slattype)
        self.slattype = slattype
        if gauge is None: gauge = DEFAULTS[self.slattype]["gauge"]
        elif isinstance(gauge,str): gauge = int(gauge.strip())
        else: gauge = int(gauge)
        self.gauge = gauge
    @property
    def slatheight(self):
        return SLATLOOKUP[self.slattype]['slatheight']
    @property
    def increaseradius(self):
        return SLATLOOKUP[self.slattype]['increaseradius']
    @property
    def slatweight(self):
        return SLATLOOKUP[self.slattype]["GAUGE"][self.gauge]["slatweight"]

    @property
    def defaultendlocks(self):
        return DEFAULTS[self.slattype]['endlocks']

    def __eq__(self,other):
        if isinstance(other,Slat):
            return self.slattype == other.slattype and self.gauge == other.gauge

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.gauge} gauge {self.slattype}"

class EndlockPattern():
    def __init__(self,endlock,windlocks = None):
        if endlock is None: endlock = Endlock("STAMPED STEEL")
        if not isinstance(endlock,Endlock):
            endlock = Endlock(endlock)
        self.endlock = endlock
            
        self._windlocks = 0
        self.windlocks = windlocks

    @property
    def windlocks(self):
        return self._windlocks
    @windlocks.setter
    def windlocks(self,windlocks):
        if windlocks is True: windlocks = 6
        elif not windlocks: windlocks = 0
        elif isinstance(windlocks,str):
            try: windlocks = int(windlocks)
            except: pass
        if windlocks and not isinstance(windlocks,int) or windlocks < 0:
            raise AttributeError("Endlock Pattern's windlocks should be None or a positive integer")
        self._windlocks = windlocks

    def getendlocks(self,slats):
        """ Returns a tuple of the number of (endlocks,windlocks) to be used on a given number of slats """
        return calculations.curtain_getendlocks(slats, self.windlocks)

    def getweight(self,slats):
        """ Returns the endlock weight given the number of slats that have endlocks """
        return calculations.curtain_getendlockweight(slats, self.endlock.weight, self.windlocks)

    def __repr__(self):
        return f"{self.__class__.__name__}: Endlocks- {self.endlock}{', Windlocks-'+self.windlocks if self.windlocks else ''}"


class Endlock():
    """ At current, this class isn't really necessary. However it is used to follow
    the heavily object-oriented philosophy of this module.
    """
    def __init__(self,endlocktype):
        endlocktype = checkendlockalias(endlocktype)
        if not endlocktype:
            raise AttributeError("Invalid Endlock Type")
        self.endlocktype = endlocktype

    @property
    def weight(self):
        return ENDLOCKLOOKUP[self.endlocktype]['endlockweight']

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.endlocktype}"

class Pipe():
    def __init__(self,door = None, pipewidth = None, shell = None, shaft = None, assembly = None, cycles = None, barrelrings = True, adjuster = False):
        self._door = None
        if door:
            self.door = door
        self._pipewidth = 0
        if pipewidth:
            self.pipewidth = pipewidth
        self._shell = None
        self.shell = shell
        self._assembly = None
        self.assembly= assembly
        self.barrelrings = barrelrings
        self._cycles = None
        self.cycles = cycles
        self.adjuster = int(adjuster)

    @property
    def door(self):
        return self._door
    @door.setter
    def door(self,door):
        if door and not isinstance(door,Door):
            raise AttributeError("Pipe's Door must be a Door instance")
        self._door = door
    @property
    def assembly(self):
        return self._assembly
    @assembly.setter
    def assembly(self,value):
        if not value:
            self._assembly = None
            return
        if not isinstance(value,Assembly):
            ## convertassembly returns a list of assemblies
            try: value = pipecalculations.convertassembly(value)[0]
            except:
                raise TypeError("assembly should be an Assembly type object")
        self._assembly = value
        value.pipe = self
    def setassembly(self,*args,**kw):
        self.assembly = Assembly(pipe = self)
        return self.assembly
    @property
    def cycles(self):
        return self._cycles
    @cycles.setter
    def cycles(self,value):
        if value is None: value = min(CYCLES)
        if value not in CYCLES:
            try:
                value = int(value)
                assert value in CYCLES
            except:
                raise ValueError("Invalid Cycles value")
        self._cycles = value
    @property
    def cyclerating(self):
        return CYCLES[self.cycles]["torquepercentage"]

    @property
    def pipewidth(self):
        return self._pipewidth
    
    @pipewidth.setter
    @measurementconversion
    def pipewidth(self,value):
        self._pipewidth = value

    @property
    def shell(self):
        if not self._shell: return None
        return PIPESIZES[self._shell]
    @shell.setter
    def shell(self,value):
        if value is not None:
            if isinstance(value,str):
                value = PIPELOOKUP.get(value,value)
            if isinstance(value,dict):
                value = value['size']
            try: value = int(value)
            except: pass
            if not isinstance(value,int):
                raise AttributeError(f"Invalid shell value: {value}")
            self._shell = value

    @property
    def max_wireod(self):
        ## NOTE: In the original code there was no check that the spring would actually fit inside the pipe
        ## (it was just programmed not to reach that point) so there is no hard numbers on ID of pipes
        ## It is fastest, at this point, to assume that pipes will generally have less than 1/4 inch walls
        return self.size - .25

    @property
    def size(self):
        """ Size of the pipe shell """
        return self.shell['size']

    @property
    def radius(self):
        """ Radius of the pipe by itself """
        return self.shell['radius']

    @property
    def shaft(self):
        return measurement.Imperial(self.shell['shaft'])

    def required_shaftlength(self, turns):
        """ Calculates the required shaft length for the given assembly. """
        out = CHARGESHAFTLENGTH
        out += self.assembly.length(turns = turns)
        ## This is a random spacer between the shell-edge and the first casting
        ## Added by me, may need to be adjusted
        out += 2
        return out

    @property
    def totalradius(self):
        """ Radius of the barrel (including barrelrings if used) """
        return self.radius + self.shell['barrelringsize'] * int(bool(self.barrelrings))

    @property
    def weight(self):
        """ Weight of the pipe itself """
        return self.shell['weight'] * (self.pipewidth/12)

    @property
    def maxdeflectionweight(self):
        """ Amount of weight that the pipe can support without bending """
        return calculations.pipe_maxdeflectionweight(self.shell['I4'], self.pipewidth)

    def getadjusterratio(self):
        if not self.adjuster: return 0
        return PIPEADJUSTERLOOKUP[self.adjuster]['ratio']

    def __eq__(self,other):
        if isinstance(other,Pipe):
            return all(getattr(self,atr) == getattr(other,atr) for atr in ["pipewidth","shell","assembly","barrelrings","cycles","adjuster"])

    def __str__(self):
        return f"{self._shell} x {self.pipewidth} Pipe"

    def __repr__(self):
        return f"{self.__class__.__name__} Object ({self._shell})"

class Assembly():
    def requirepipe_property(func):
        """ Wraps the function with Property, and checks that self.pipe is set each time the property is read (raising an AttributeError if it is unset) """
        @property
        def inner(self,*args,**kw):
            if not self.pipe:
                raise AttributeError("pipe not set for Assembly")
            return func(self,*args,**kw)
        return inner

    def __init__(self,pipe = None):
        self._pipe = None
        self.pipe = pipe
        self._sockets = AssemblySockets()
    ## Socket Methods/Properties
    @property
    def sockets(self):
        return self._sockets

    def addsocket(self,*args,**kw):
        result = self.sockets.addsocket(*args,**kw)
        if self.pipe:
            result.cycles = self.cycles
        return result
    def insertsocket(self,index,socket,*args,**kw):
        try:
            result = self.sockets.insertsocket(index,socket,*args,**kw)
        except: pass
        else:
            if self.pipe:
                socket.cycles = self.cycles
            return result
    def removesocket(self,*args,**kw):
        return self.sockets.removesocket(*args,**kw)
    def popsocket(self,*args,**kw):
        return self.sockets.popsocket(*args,**kw)
    def sockettype(self,*args,**kw):
        return self.sockets.sockettype(*args,**kw)
    def clear(self,*args,**kw):
        return self.sockets.clear(*args,**kw)
    ## Stats
    @property
    def pipe(self):
        return self._pipe
    @pipe.setter
    def pipe(self,value):
        if value is not None and not isinstance(value,Pipe):
            raise ValueError("Asssembly's pipe must be Pipe instance")
        self._pipe = value
    @property
    def weight(self):
        return sum(socket.weight for socket in self.sockets)
    def length(self, turns):
        return sum(socket.length(turns = turns) for socket in self.sockets) + CASTINGGAP * (len(self.sockets) - 1)
    @property
    def torquepercentage(self):
        return CYCLES[self.cycles]['torquepercentage']
    @requirepipe_property
    def torque(self):
        return self.pipe.door.requiredtorque_open
    @requirepipe_property
    def turns(self):
        return self.pipe.door.turnstoraise
    @requirepipe_property
    def pipesize(self):
        return self.pipe.radius
    @requirepipe_property
    def cycles(self):
        return self.pipe.cycles

    @property
    def lift(self):
        """ Returns the total lift generated by the assembly """
        return sum([socket.lift for socket in self.sockets])

    def validatetorque(self,ippt):
        """ Checks that the spring is good for the given torque (not too strong or too weak) """
        return ippt * .985 <= self.lift  <= ippt * 1.01

    def validate(self, ippt, turns):
        if not self.validatetorque(ippt): return False
        if not all(socket.validate(turns) for socket in self.sockets): return False
        return True

    def __eq__(self, other):
        if isinstance(other, Assembly):
            return self.sockets == other.sockets


    def __str__(self):
        ## Add two tabs padding to each socket
        socketstring = "\n".join( almethods.linepadder(str(socket))
            for socket in self.sockets)
        ## Debugging with print fails if Pipe is not set for Assembly
        attrs = {k:"N/A" for k in ["pipesize","cycles","torque","turns"]}
        for k in attrs: 
            try: attrs[k] = getattr(self,k)
            except AttributeError: pass
        return \
f"""Assembly:
    Pipe: {attrs['pipesize']}
    Cycles: {attrs['cycles']}
    Req. Torque: {attrs['torque']}
    Turns: {attrs['turns']}
    Sockets:
{socketstring}
"""

    def __repr__(self):
        return super().__repr__()

class AssemblySockets():
    """ Custom Container-type Object used by Assembly with special validating functions """
    def checksockettype(sockettype):
        if not isinstance(sockettype,str)\
           or sockettype.lower() not in ["spring","compound"]:
            raise ValueError('Socket Type must be "spring" or "compound".')
    
    def __init__(self):
        """ Initializes a new AssemblySockets object """
        self._sockets = list()
    def __getitem__(self,index):
        return self._sockets[index]
    def __len__(self):
        return self._sockets.__len__()
    def __iter__(self):
        return self._sockets.__iter__()
    def __contains__(self,item):
        return self._sockets.__contains__(item)
    def addsocket(self,socket = None):
        """ Appends a new "spring" or "compound" socket to the end (append method) and returns a reference to it.
       
            If a socket is provided, appends the socket instead of creating a new one
        """
        if socket and not isinstance(socket,Socket):
            raise ValueError("socket must be a Socket instance")
        if not socket:
            socket = Socket()
        self.insertsocket(-1,socket)
        return socket
    def insertsocket(self,index,socket):
        """ Inserts a socket-type object into the sockets at the given position """
        if not isinstance(socket,Socket):
            raise ValueError("socket must be a Socket instance")
        try: self._sockets.insert(index,socket)
        except IndexError: raise IndexError("Could not insert Socket at given index")
    def removesocket(self,index):
        """ Removes a socket by index """
        if not isinstance(index,int):
            raise ValueError("Socket index should be integer")
        try: socket = self[index]
        except IndexError: raise IndexError(f"Could not remove index: {index}")
        del self._sockets[index]
    def popsocket(self,index):
        """ Removes and returns a socket by index """
        if not isinstance(index,int):
            raise ValueError("Socket index should be integer")
        try: socket = self[index]
        except IndexError: raise IndexError(f"Could not remove index: {index}")
        del self._sockets[index]
        return socket
    def clear(self):
        """ Clears all castings from the assembly """
        self._sockets.clear()

    def __eq__(self,other):
        if isinstance(other,AssemblySockets):
            return self._sockets == other._sockets
        if isinstance(other,Assembly):
            return self == other.sockets

class Socket():
    """ A representation of a pair of castings connected by one or more Springs.
    
    Spring order for Socket.springs is Outermost -> Innermost. This is because when
    building Sockets it is most often useful to start with the strongest (largest)
    spring and then compensate with inner springs (i.e.- *appending* smaller Springs).
    This may be reworked to encompass other items attached to the Shaft in the future.
    """
    def __init__(self, *springs, castings = False):
        """ Initializes a new Socket Object.

            Accepts springs of the socket as positional arguements; springs should
            be provided larget-od to smallest.
            Default castings are used. To remove castings altogether, set castings
            to None.
        """
        self._castings = None
        self._springs = []
        for spring in springs:
            self.addspring(spring)

        if castings is False:
            castings = methods.getcasting(*self.springs)
        self.castings = castings

    @property
    def castings(self):
        return self._castings
    @castings.setter
    def castings(self,value):
        if value is None:
            self._castings = CastingSet()
            return
        if isinstance(value,(list,tuple)):
            value = CastingSet(*castings)
        if not isinstance(value,CastingSet):
            raise ValueError(f"Invalid Castings: {value}")
        self._castings = value

    @property
    def springs(self):
        return list(self._springs)

    @property
    def weight(self):
        ## TODO: This is currently a hack to ensure it works. We should probably do something else
        return (self.castings.weight if self.castings else 0) + sum(spring.weight for spring in self)

    def __iter__(self, *args, **kw):
        """ A shortcut for "for spring in socket.springs" """
        return self.springs.__iter__(*args,**kw)
    
    def addspring(self,spring):
        """ Simply Adds a Spring to the Socket. Validation must be done Separately. """
        if not isinstance(spring,Spring):
            raise TypeError(f"spring must be a Spring Instance")
        self._springs.append(spring)

    def length(self,turns):
        """ Returns the total length of the socket, including stretch and castings. """
        out = 0
        out += self.castings.outside_length
        if self.springs:
            ## Only need outermost spring: all other springs are garaunteed to 
            ## be contained in outer
            out += self.springs[0].totallength(turns = turns)
            
        return out

    @property
    def lift(self):
        """ The total lift of all springs in a Socket """
        return sum(spring.lift for spring in self.springs)

    def validate(self, turns):
        """ Runs a series of basic validations (diameter, ... more in future?).
       
            The pattern for this function is to shortcircuit on failure (return False
            on very first failure: only return True at end of function).
        """
        ## For each spring, make sure that max turns is greater than actual turns
        for spring in self.springs:
            if not spring.validatemaxturns(turns):
                #print("Fail a")
                return False

        ## Validators for compound
        if len(self.springs) > 1:
            ## Compare ID to next OD
            for i in range(len(self.springs[:-1])):
                if self.springs[i].id <= self.springs[i+1].od:
                    #print("Fail b")
                    return False

            ## Make sure inner springs are shorter by an amount based on size
            ## short based on size
            short = 6
            if self.springs[0].od >3.75:
                short = 9.600001 ## <- ... I dunno why this is...
            ## for each spring from the outermost to the 2nd-to-last innermost,
            ## compare the outerspring to the next (inner) spring
            for i in range(len(self.springs[:-1])):
                ## Coiledlength of next inner spring is is greater than the outerspring + short (clearance allowance)
                if self.springs[i+1].totallength(turns) > self.springs[i].totallength(turns) - short:
                    #print("Fail c")
                    return False

        ## Test existence of a Casting
        if not self.castings:
            return False

        ## None of the tests have failed
        return True

    def validatetorque(self,ippt):
        """ Checks that the socket is good for the given torque (not too strong or too weak) """
        return ippt * .985 <= self.lift  <= ippt * 1.01

    def validatemaxturns(self,turns):
        """ Runs turns validation on each spring in the assembly """
        return all(spring.validatemaxturns(turns) for spring in self.springs)

    def __eq__(self,other):
        if isinstance(other,Socket):
            return self.castings == other.castings and self.springs == other.springs

    def __str__(self):
        springs = almethods.linepadder(
            "\n".join([str(spring) for spring in self.springs]))
        castings = almethods.linepadder(str(self.castings) if self.castings else "")
        return f"""Socket:
{springs}
{castings}
        """

    def __repr__(self):
        return f"SocketObject ({', '.join([str(spring.wirediameter) for spring in self.springs])})"

class CastingSet():
    def __init__(self,*castings):
        self._castings = list()
        for casting in castings:
            self.addcasting(casting)

    @property
    def castings(self):
        return list(self._castings)

    def addcasting(self,casting):
        """ Appends a casting to the current CastingSet """
        casting = methods.convert_to_casting(casting)
        if(casting['type'] == "pipe" and self.pipecasting):
            self._castings.remove(self.pipecasting)
        self._castings.append(casting)
        self._sortcastings()

    def _sortcastings(self):
        self._castings = sorted(
            sorted(self.castings, key = lambda casting: casting['castingod']), ## Order smallest casting first
            key = lambda casting: casting['type'] != "pipe") ## Put pipe casting start

    @property
    def pipecasting(self):
        pc = [casting for casting in self.castings if casting['type'] == "pipe"]
        if not pc: return None
        if len(pc) > 1: raise AttributeError("CastingSet can only have One Pipe Casting")
        return pc[0]

    @property
    def maxsprings(self):
        return self.castings[0]['springs']

    @property
    def outside_length(self):
        return self.castings[0]['length'] + self.castings[-1]['length']

    @property
    def weight(self):
        return sum(casting['weight'] for casting in self.castings)

    def __eq__(self,other):
        if isinstance(other,CastingSet):
            return all(x==y for x,y in itertools.zip_longest(self._castings,other._castings))

    def __str__(self):
        castingstring = '\n\t'.join([casting['name'] for casting in self.castings])
        return f"""Casting Set:
    Outside Length: {self.outside_length}
    Weight: {self.weight}
    Castings:
        {castingstring}"""


class Spring():
    def __init__(self,wire = .1875, od = None, uncoiledlength = 0, tails = 3, cycles = None, coiledlength = None):
        """ Creates a new Spring.

        Defaults are: .1875 wire, 0 uncoiledlength.
        """
        if uncoiledlength and coiledlength:
            raise SyntaxError("It is invalid to set spring by both uncoiledlength and coiledlength")
        self._wire = None
        self._od = 0
        self._uncoiledlength = 0
        self._tails = 3
        if cycles is None: cycles = min(CYCLES)
        
        self.wire = wire
        if od is None:
            od = self.wire['min_od']
        else:
            if od < self.wire['min_od']:
                raise ValueError("Invalid Wire od: od is smaller than Wire's minimum od")
        self.od = od
        if coiledlength:
            self.coiledlength  = coiledlength
        else:
            self.uncoiledlength = uncoiledlength
        self.tails = tails
        self.cycles = cycles

    ## Core Stats
    @property
    def wire(self):
        return dict(self._wire)
    @wire.setter
    def wire(self,wire):
        if isinstance(wire,float):
            try: wire = WIRE[wire]
            except KeyError:
                raise ValueError("Wire diameter is not predefined in module")
        elif isinstance(wire,dict):
            if not iswiredict(wire):
                raise ValueError("Invalid wire dict: required keys- 'wirediameter','liftrate','weightperinch','averagetensile','mp_base','min_od'")
        else:
            raise ValueError("wire must be a float denoting wirediameter, or a properly structured wire dict.")
        self._wire = wire
        if wire['min_od'] > self._od:
            self._od = wire['min_od']
    @property
    def od(self):
        return self._od
    @od.setter
    def od(self,value):
        if not isinstance(value,(int,float)):
            raise ValueError("od must be float or int")
        if value <= 0:
            raise ValueError("od must be greater than 0")
        self._od = value
    @property
    def id(self):
        return self.od - self.wirediameter * 2
    @property
    def uncoiledlength(self):
        return self._uncoiledlength
    @uncoiledlength.setter
    def uncoiledlength(self,value):
        if not isinstance(value,(int,float)):
            raise ValueError("Uncoiled Length must be an integer or float")
        if value < 0:
            raise ValueError("Uncoiled Length must be positive")
        self._uncoiledlength = value
    @property
    def tails(self):
        return self._tails
    @tails.setter
    def tails(self,value):
        if not isinstance(value,(int,float,tuple,list)):
            raise ValueError("Tails must be int or float, or a tuple or list of ints or floats.")
        if isinstance(value,(tuple,list)) and (len(value) != 2 or any(not isinstance(v,(int,float)) for v in value)):
            raise ValueError("Iterable tails must be length 2 and have values that are ints or floats")
        if isinstance(value,(int,float)):
            if value < 3:
                raise ValueError("Minimum of 3-inch tail required.")
        else:
            if any(v < 3 for v in value):
                raise ValueError("Minimum of 3-inch tail required.")
        self._tails = value

    ## Basic Stats
    @property
    def torquepercentage(self):
        return CYCLES[self.cycles]['torquepercentage']
    @property
    def wirediameter(self):
        return self.wire['wirediameter']
    @property
    def md(self):
        """ Mean Diameter """
        return self.od - self.wirediameter
    @property
    def lengthcoil(self):
        return self.md*math.pi
    def stretch(self, turns):
        ## Double the stretch allowance to provide space for future preturns
        return self.wirediameter * 2 * turns
    def totallength(self,turns):
        """ Length of the coiled spring with stretch applied """
        return self.coiledlength + self.stretch(turns)
    @property
    def lift(self):
        ## It is useful to be able to return a value for debugging,
        ## so when uncoiledlength is not set, we'll return None
        try:
            return self.wire['liftrate'] / self.uncoiledlength
        except:
            return None
    @property
    def mp(self):
        return self.wire['mp_base'] * self.torquepercentage
    @property
    def maxturns(self):
        ## self.lift may be None if self.uncoiledlength is not set
        if self.lift:
            return self.mp / self.lift
        ## We will also return None
        return None

    ## Complex Stats
    @property
    def coils(self):
        return self.uncoiledlength/self.lengthcoil
    @coils.setter
    def coils(self,value):
        """ Sets uncoiledlength based on number of coils """
        if not isinstance(value,(int,float)) or value < 0:
            raise ValueError("Invalid number of coils")
        self.uncoiledlength = value * self.lengthcoil
    @property
    def coiledlength(self):
        return self.coils*self.wirediameter
    @coiledlength.setter
    def coiledlength(self,value):
        """ Setting coiledlength sets uncoiledlength instead, which may lead to (very) minor rounding errors. """
        if not isinstance(value,(int,float)):
            raise ValueError("Coiled Length must be an integer or float")
        if value < 0:
            raise ValueError("Coiled Length must be positive")
        self.uncoiledlength = value / self.wirediameter * self.lengthcoil
    @property
    def volume(self):
        """ Calculates the total volume of the spring """
        return math.pi() * (self.wirediameter/2)**2 * self.uncoiledlength
    @property
    def weight(self):
        return self.wireweight
    @property
    def wireweight(self):
        ##                  Total Length                  PI               radius-squared
        volume = (self.uncoiledlength + self.taillength) * math.pi * (self.wirediameter/2)**2
        ##  Cubic Volume * Weight per Cubic Inch
        return volume * WIREWEIGHTCUBEINCH
    @property
    def taillength(self):
        if isinstance(self.tails,(tuple,list)):
            return sum(self.tails)
        return self.tails * 2

    ## Validations
    def validatetorque(self,ippt):
        """ Checks that the spring is good for the given torque (not too strong or too weak) """
        return ippt * .985 <= self.lift  <= ippt * 1.01
    def validatemaxturns(self, totalturns):
        """ Compares the spring's max turns against the provided turns """
        return self.maxturns >= totalturns * .985

    ## Methods
    def setlengthbytorque(self,torque):
        """ Sets the Spring's length based on Torque required """
        self.uncoiledlength = self.wire['liftrate']/torque

    def __eq__(self,other):
        if isinstance(other,Spring):
            return all(getattr(self,atr) == getattr(other,atr) for atr in ["wire","od","uncoiledlength","tails","cycles"])

    def __str__(self):
        return \
f"""Spring:
    Wire Size: {self.wirediameter}
    OD: {self.od}
    Torque: {self.lift}
    Max Turns: {self.maxturns}
    Length:
        Uncoiled: {self.uncoiledlength}
        Coiled: {self.coiledlength}
    Number Coils: {self.coils}
    Tails: {self.tails}
    Weight: {self.weight}"""
        
    def __repr__(self):
        return f"{self.__class__.__name__} Object ({self.wirediameter}x{self.od}x{self.coiledlength})"