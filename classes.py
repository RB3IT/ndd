## Builtin
import functools
import math

## Custom Module
from alcustoms import methods as almethods
from alcustoms import measurement

## This Module
from NewDadsDoor.constants import *

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

def measurementconversion(function):
    """ A Wrapper which checks if an instance method's 'value' argument is a string reperesenting a measurement
   
    Note that this function is for instance methods and automatically assumes "self"
    Converts the string to inches as a float.
    """
    @functools.wraps(function)
    def inner(self,*args,value=None,**kw):
        argflag = False
        ## If value is not provided, have to check if it is an argument
        if value is None:
            ## If there are no args, proceed as normal (value must therefore
            ## be a keyword for the function, and therefore will be the
            ## function's default). *args is just a formality.
            if not args: return function(self,*args,**kw)
            ## Otherwise, parse(assume) the first argument as value
            args = list(args)
            value = args.pop(0)
            ## Make sure we track that we pulled value out so we can put it back
            argflag = True
        
        ## Convert our value

        ## We'll allow for Feet to be passed as an argument as int/float
        ## There's a chance that the measurment was provided as a string-format of an int/float
        if isinstance(value,str):
            try: value = float(value)
            except: pass
        ## Handle Int/Float assuming it represents feet
        if isinstance(value,(int,float)):
            value = value * 12
        ## Otherwise, we attempt to parse the value
        else:
            value = measurement.convertmeasurement(value)
        ## If Value was an arg, put it back
        if argflag: args = [value,] + args
        ## Otherwise, we can add it as a kw
        else: kw['value'] = value
        ## continue as normal
        return function(self,*args,**kw)
    return inner

class Door():
    def __init__(self, clearopening_height, clearopening_width, upset = None, stopsize = 2):
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
        self.stopsize = stopsize

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
        if not isinstance(value,Pipe): raise AttributeError("Door's pipe must be Pipe Instance")
        self._pipe = value
        self.pipe.door = self

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
        pipe = self.pipefactory(**kw)
        self.pipe = pipe
        return pipe

    def sethood(self,**kw):
        hood = Hood(**kw)
        self.hood = hood
        return hood

    @property
    def clearopening_height(self):
        return self._clearopening_height
    
    @clearopening_height.setter
    @measurementconversion
    def clearopening_height(self,value):
        self._clearopening_height = value

    @property
    def clearopening_width(self):
        return self._clearopening_width
    
    @clearopening_width.setter
    @measurementconversion
    def clearopening_width(self,value):
        self._clearopening_width = value

    @property
    def bracketplatesize(self):
        if not self._bracketplatesize: return 18
        return self._bracketplatesize

    @bracketplatesize.setter
    @measurementconversion
    def bracketplatesize(self,value):
        if value and not isinstance(value,(int,float)):
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
        """ Returns the distance between the bottom of the curtain and the center of the bracket plates

        Note that for a door with standard upset, bracket plates, and bottomabar this number
        is constant regardless of size of door
        """
        return self.pipecenterlineheight - self.stopheight + self.curtain.bottomheight

    @property
    def stopheight(self):
        return self.clearopening_height + self.stopsize

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
        return self.initialradius + (self.turnstoraise * self.curtain.increaseradius)

    @property
    def hangingweight_closed(self): ## HW
        """ Total weight of the Curtain (when closed)"""
        return self.curtain.getweight(self.pipecenterlineheight)

    @property
    def hangingweight_open(self): ## WU
        """ Weight of the Curtain when the door is Open """
        weight = self.curtain.weight_open
        if self.stopheight >=192: return weight * 1.2
        if self.stopheight < 50: return weight + 5
        #if 50 < self.curtain.stopheight < 100: return weight + 10
        return weight * 1.1

    @property
    def pipecenterlineheight(self): ## HC
        """ Height from the floor to the center of the Pipe """
        ## Stop Height + Upset + Half Bracket Plate Height (Pipe is centered on bracket plates)
        return self.stopheight + self.upset + self.bracketplate.height/2

    @property
    def wall_length(self):
        """ Returns the necessary height to cover the openheight, stops, upset, and Bracket Plates """
        return self.stopheight + self.upset + self.bracketplate.height

    @property
    def preturns(self): ## PT
        """ Number of turns required in order to achieve requiredtorque_open """
        return self.requiredtorque_open / self.torqueperturn 

    @property
    def requiredtorque_closed(self): ## TD
        """ Required amount of force required to lift door """
        return self.initialradius * self.hangingweight_closed

    @property
    def requiredtorque_open(self): ## TU
        """ Required amount of force required to hold the door open """
        return self.finalradius * self.hangingweight_open

    @property
    def torqueperturn(self): ## IP
        """ The amount of torque (inch/pound) for each turn (IPPT in handbook)
        
        Handbook notes this should be rounded up to nearest 1/8.
        """
        return rounduptofraction(
            (self.requiredtorque_closed - self.requiredtorque_open) / self.turnstoraise,
            1/8)

    @property
    def totalturns(self): ## TT
        """ Total number of time the pipe will be turned """
        return self.turnstoraise + self.preturns    
        

    @property
    def turnstoraise(self): ## TR
        """ Number of Barrel Rotations required to fully raise the door (TR)

        Equation to Raise door is based on: 2 * Pi * R * T + Pi * R1 * T**2 = SH
        Where R: Pipe (Initial, Total) Radius, R1: Radius Increase each Turn
        T: Turns to Raise (TR otherwise), SH: Stop Height

        This equation reflects that the Stop Height (when rolled) will be wrapped
        around the pipe's circumference on each turn (2 * Pi * R * T) plus an
        additional distance on each turn based on the layers beneath it (Pi * R1 * T**2).

        The equation is converted to quadratic form Pi*R1*T**2  +  2*Pi*R*T  -SH
        (A*X**2 + B*X + C) which then can be solved with the quadratic equation:
        ( -B +/- sqrt(B**2 - 4AC) ) / 2A
        Being ( -2*Pi*R +/- sqrt((2*Pi*R)**2 - 4 * (R1*Pi) * (-SH)) ) / (2 * Pi * R1)
        """
        ## A: Extra Circumference each Turn
        A = math.pi * self.curtain.increaseradius
        ## B: Base Circumference each Turn (per Pipe)
        B = 2 * math.pi * self.pipe.totalradius
        ## C: Stop Height
        C = -self.stopheight
        ## Solve quadratic
        return (-B + math.sqrt(B**2 - 4*A*C)) / (2*A)

    def getwraplength(self):
        """ Gets the calculated distance for the wrap """
        return \
            2 * math.pi * self.pipe.totalradius * (.75 - self.pipe.getadjusterratio()) +\
           self.pipecenterlineheight - self.stopheight

    def validatepipesize(self):
        return self.pipe.weight + self.curtain.hangingweight_closed <= self.pipe.maxdeflectionweight * .97

    def validatepipeassembly(self):
        """ Returns whether the pipe's assembly is valid for the given curtain. """
        return self.pipe.assembly.validate(ippt = self.torqueperturn, turns = self.totalturns)

    def maxpipewidth(self):
        """ Calculates the maximum width for the pipe between the brackets. """
        return self.clearopening_width + 2

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

class Tracks():
    """ TODO """
 
class ExtrudedGuides(Tracks):
    """ TODO """


class Curtain():
    """ A Container object for collecting sections
    """
    def __init__(self, door):
        self.door = door
        self._sections = list()

    def slatlength(self,section):
        """ A Curtain's Slat length is often wider than the width """
        ## TODO Create FireDoorSection Subclass
        clow = self.door.clearopening_width
        length = clow
        if not getattr(section,"endlockpattern",None):
            if getattr(section,"slattype",None) in ["3 5/8 INCH CROWN SLAT","2 7/8 INCH CROWN SLAT"]: length += 1
            elif getattr(section,"slattype",None) == "2 1/2 INCH FLAT SLAT": length += .25
        if getattr(section,"endlockpattern",None) and (section.endlockpattern.endlock == "CAST IRON" and section.slattype == "2 1/2 INCH FLAT SLAT"):
           length -= .5

        if isinstance(self.door.tracks,ExtrudedGuides):
            return length + 2.5
        if getattr(section,"slattype",None) in ["3 5/8 INCH CROWN SLAT","2 7/8 INCH CROWN SLAT"]:
            if not getattr(section,"endlockpattern",None) and section.endlockpattern.windlocks:
                if clow < 149: return length + 3.5
                if clow <=221: return length + 3.875
        if getattr(section,"slattype",None) == "2 7/8 INCH CROWN SLAT":
            if getattr(section,"endlockpattern",None) and section.endlockpattern.windlocks:
                if clow < 293: return length + 3.875
                return length + 4.875
        if not isinstance(self.door.tracks,ExtrudedGuides):
            if clow < 149: return length + 3.5
            if clow < 221: return length + 3.875
            if clow < 293: return length + 4.5
            if clow <= 365: return length + 5.5
        if getattr(section,"slattype",None) == "2 1/2 INCH FLAT SLAT":
            if not getattr(section,"endlockpattern",None) and section.endlockpattern.windlocks:
                if clow < 149: return length + 4.25
                if clow < 197: return length + 4.625
            else:
                if clow < 293: return length + 4
                return length + 5
        if getattr(section,"slattype",None) == "MIDGET CROWN SLAT < 2 INCH >":
            if clow < 149: return length + 3.75
            return length + 4.125

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
        return self.feederslatweight * self.slatlength * .65

    @property
    def slopeweight(self):
        """ Returns the weight added by the slopped portion of the bottom bar """
        length = self.slatlength
        if not self.slope: return 0
        slopereach =  self.slope + 3
        reachsquarearea = slopereach * (length  + 1)
        slopetrianglearea = self.slope * (length + 1) / 2
        diff_feet = (reachsquarearea - slopetrianglearea) / 144 * 5
        return diff_feet + (length + 1) * .05316

    @property
    def slatlength(self):
        return self.curtain.slatlength(self)

    def __repr__(self):
        return f"{self.__class__.__name__} Object"

class SlatSection(Section):
    def __init__(self, curtain=None, endlockpattern = None, slats = 0, slat = None):
        super().__init__(curtain=curtain)
        if not endlockpattern is None and not isinstance(endlockpattern,EndlockPattern):
            raise AttributeError("endlockpattern must be None or EndlockPattern instance")
        self.endlockpattern = endlockpattern
        self.slats = slats
        if slat is None: slat = Slat("2 1/2 INCH FLAT SLAT")
        if not isinstance(slat,Slat):
            slat = Slat(slat)
        self.slat = slat

    @property
    def height(self):
        if not self.slats: return 0
        return self.slats * self.slat.slatheight

    @property
    def weight(self):
        return self.getslatweight(self.slats) + self.endlockpattern.getweight(math.ceil(self.slats/2))

    @property
    def slattype(self):
        return self.slat.slattype

    @property
    def slatlength(self):
        return self.curtain.slatlength(self)

    def getnumberslats(self,height = None):
        """ Returns the number of slats needed for the given height, rounding up """
        if height is None:
            height = self.curtain.door.stopheight + self.curtain.door.getwraplength()
        return math.ceil(height / self.slat.slatheight)

    def getslatweight(self,slats):
        """ Returns the slat weight given the number of slats """
        return slats * self.slatlength * self.slat.slatweight

    @property
    def increaseradius(self):
        return self.slat.increaseradius

    def __repr__(self):
        return f"{self.__class__.__name__} Object ({self.slattype}{' x' + self.slats if self.slats else ''})"

class PerforatedSlats(SlatSection):
    def __init__(self, curtain=None, endlockpattern = None, slats = 0, slattype = None, slatgage = None):
        super().__init__(curtain=curtain, endlockpattern=endlockpattern, slats=slat, slattype=slattype, slatgage=slatgage)
    @property
    def slatlength(self):
        clow  = self.curtain.door.clearopening_width
        length = super().slatlength
        if isinstance(self.curtain.door.guides,ExtrudedGuides):
            return length
        if not self.endlockpattern.windlocks:
            if clow <= 149: return length + 3.875
            if clow < 264: return length + 4.25
        else:
            if clow <= 293: return length + 4
            return length + 5

    @property
    def weight(self):
        return super().weight() - self.perforatedweightloss
    @property
    def perforationsperslat(self):
        """ Determine number of perforation Windows based on Curtain Width """
        ## Windows every 8.5 Inches, skip first and last window
        ## This calculation is from the original, but I would probably like it
        ## better written "(self.slatlength - edgepadding)/8.5" so that the distance
        ## from the edge can be customized (as opposed to being 8.5)
        return self.slatlength/8.5 - 2

    @property
    def perforatedweightloss(self):
        ## (Slat Weight per Window-size) * Weight Loss Per Window *  Number of perforations/Slat * Number of Slats
        return (self.slat.slatweight/5.25) * 4.648175 * self.curtain.perforationsperslat * self.slats

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
        """ Attempts to determine the base Slat type of the given value and returns a Slat instance with the default gage for that type """
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

    def __init__(self, slattype = None, gage = None):
        if slattype is None: slattype = "2 1/2 INCH FLAT SLAT"
        if slattype not in SLATLOOKUP:
            slattype = Slat.parsetype(slattype)
        self.slattype = slattype
        if gage is None: gage = DEFAULTS[self.slattype]["gage"]
        elif isinstance(gage,str): gage = int(gage.strip())
        else: gage = int(gage)
        self.gage = gage
    @property
    def slatheight(self):
        return SLATLOOKUP[self.slattype]['slatheight']
    @property
    def increaseradius(self):
        return SLATLOOKUP[self.slattype]['increaseradius']
    @property
    def slatweight(self):
        return SLATLOOKUP[self.slattype]["GAGE"][self.gage]["slatweight"]

    @property
    def defaultendlocks(self):
        return DEFAULTS[self.slattype]['endlocks']

class EndlockPattern():
    def __init__(self,endlock,windlocks = None):
        if endlock is None: endlock = Endlock("STAMPED STEEL")
        if not isinstance(endlock,Endlock):
            endlock = Endlock(endlock)
        self.endlock = endlock

        if windlocks is True: windlocks = 6
        elif not windlocks: windlocks = 0
        if windlocks and not isinstance(windlocks,int) or windlocks < 0:
            raise AttributeError("Endlock Pattern's windlocks should be None or a positive integer")
            
        self.windlocks = windlocks

    def getendlocks(self,slats):
        """ Returns a tuple of the number of (endlocks,windlocks) to be used on a given number of slats """
        if slats == 0: return (0,0)
        if not self.windlocks:
            return (math.ceil(slats/2)*2,0)
        singleendlocks = math.ceil(slats/2)
        singlewindlocks = (singleendlocks / self.windlocks)
        return (singleendlocks * 2, singlewindlocks * 2)

    def getweight(self,slats):
        """ Returns the endlock weight given the number of slats that have endlocks """
        if slats == 0: return 0
        if self.windlocks:
            endlockweight = (((slats / self.windlocks) * .656) / slats ) + .17
        else: endlockweight = self.endlock.endlockweight
        ## Endlock on each side
        return slats * endlockweight * 2

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
    def endlockweight(self):
        return ENDLOCKLOOKUP[self.endlocktype]['endlockweight']


class Pipe():
    def __init__(self,pipewidth = None, shell = None, shaft = None, assembly = None, cycles = None, barrelrings = True, adjuster = False):
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
    def assembly(self):
        return self._assembly
    @assembly.setter
    def assembly(self,value):
        if not value:
            self._assembly = None
            return
        if not isinstance(value,Assembly):
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
            self._shell = int(value)

    @property
    def max_wireod(self):
        ## NOTE: In the original code there was no check that the spring would actually fit inside the pipe
        ## (it was just programmed not to reach that point) so there is no hard numbers on ID of pipes
        ## It is fastest, at this point, to assume that pipes will generally have less than 1/4 inch walls
        return self.shell['size'] - .25

    @property
    def radius(self):
        """ Radius of the pipe by itself """
        return self.shell['radius']

    @property
    def shaft(self):
        return self.shell['shaft']

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
        """ Amount of weight that the pipe can support without bending

        This equation was taken as-is from the source code; its origins could not
        be found the handbook.
        """
        ## I4 / Width-in-feet^2 * 38667
        return self.shell['I4'] / (self.pipewidth/12) ** 2 * 38667

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
            return self.pipe == other.pipe and self.sockets == other.sockets


    def __str__(self):
        ## Add two tabs padding to each socket
        socketstring = "\n".join( almethods.linepadder(str(socket))
            for socket in self.sockets)
        return \
f"""Assembly:
    Pipe: {self.pipesize}
    Cycles: {self.cycles}
    Req. Torque: {self.torque}
    Turns: {self.turns}
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
            castings = getcasting(*self.springs)
        self.castings = castings

    @property
    def castings(self):
        return self._castings
    @castings.setter
    def castings(self,value):
        if value is None:
            self._castings = None
            return
        if isinstance(value,(list,tuple)):
            value = CastingSet(*castings)
        if not isinstance(value,CastingSet):
            raise ValueError(f"Invalid Castings: {value}")
        self._castings = value

    @property
    def springs(self):
        return list(self._springs)

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
                print("Fail a")
                return False

        ## Validators for compound
        if len(self.springs) > 1:
            ## Compare ID to next OD
            for i in range(len(self.springs[:-1])):
                if self.springs[i].id <= self.springs[i+1].od:
                    print("Fail b")
                    return False

            ## Make sure inner springs are shorter by an amount based on size
            ## short based on size
            short = 6
            if self.springs[0].od >3.75:
                short = 9.600001 ## <- ... I dunno...
            ## for each spring from the outermost to the 2nd-to-last innermost,
            ## compare the outerspring to the next (inner) spring
            for i in range(len(self.springs[:-1])):
                ## Coiledlength of next inner spring is is greater than the outerspring + short (clearance allowance)
                if self.springs[i+1].totallength(turns) > self.springs[i].totallength(turns) - short:
                    print("Fail c")
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
        return f"""Socket:
{springs}
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
        if isinstance(casting,str):
            casting = CASTINGLOOKUP.get(casting,None)
        if not isinstance(casting,dict):
            raise TypeError(f"Invalid Casting: {casting}")
        ## These attrs are required for casting dicts
        missing = [attr for attr in ["type","springs","ods","castingod","length","innerloss"] if casting.get(attr,None) is None]
        if missing:
            raise ValueError("Casting missing the following values: {}")
        self._castings.append(casting)

    @property
    def outside_length(self):
        return self.castings[0]['length'] + self.castings[-1]['length']

    def __eq__(self,other):
        if isinstance(other,CastingSet):
            return all(x==y for x,y in itertools.zip_longest(self._castings,other._castings))

    ## TODO: Casting weight?

def getcasting(*springs):
    """ Attempts to select castings for the given springs """
    nsprings = len(springs)
    springods = sorted([spring.od for spring in springs])
    castings = [casting for casting in CASTINGS if casting['type'] == "pipe"
                    and casting['springs'] >= nsprings
                    and all(od in casting['ods'] for od in springods)]
    ## There's a possibility we don't have a matching casting, so return None
    if not castings:
        return None
    ## We only have just so many casting options at this point... only one is going to work
    pipecasting = castings[0]

    springcastings = []
    for od in springods:
        castings = [casting for casting in CASTINGS if casting['type']  == "spring"
                          and od in casting['ods']]
        ## As above, maybe we don't have a valid casting: return None
        if not castings:
            return None
        ## Pick the casting with the smallest loss of space
        ## As above,this maya s well be castings[0]
        springcastings.append(min(castings,key = lambda casting: casting['innerloss']))
    return CastingSet(pipecasting,*springcastings)

class Spring():
    def __init__(self,wire = .1875, od = 2.75, uncoiledlength = 0, tails = 3, cycles = None):
        """ Creates a new Spring.

        Defaults are: .1875 wire, 2.75 od, 0 uncoiledlength.
        """
        self._wire = None
        self._od = 0
        self._uncoiledlength = 0
        self._tails = 3
        if cycles is None: cycles = min(CYCLES)
        
        self.wire = wire
        self.od = od
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

def create_curtain(door,slattype = None):
    """ Helper function to autopopulate a door's Curtain.

        This function will replace any existing curtain on the pipe with
        a curtain containing sufficient slats of the given type (default
        2-1/2 Flat with default endlocks for that slattype) and a
        standard Bottom Bar.
    """
    if not isinstance(door,Door):
        raise ValueError("create_curtain requires a door object")
    if slattype is None: slattype = "brd"
    slat = Slat(slattype)
    door.curtain = None
    door.setcurtain()
    curtain = door.curtain
    slats = SlatSection(curtain, slat = slat)
    slats.endlockpattern = EndlockPattern(slat.defaultendlocks)
    curtain.append(slats)
    bottombar = BottomBar(slat, curtain)
    curtain.append(bottombar)
    slats.slats = slats.getnumberslats(curtain.curtainshort())    

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
        pipe = Pipe(shell = pipe['size'])
    if not isinstance(pipe,Pipe):
        raise ValueError("Invalid Pipe")
    return pipe

def validate_compound_assemblies(func):
    """ Validation decorator for centralized validation """
    @functools.wraps(func)
    def inner(torque,turns,*,pipe = None,**kw):

        def validator(assembly):
            """ The actual validation function """
            if not all(socket.validate(turns) for socket in assembly.sockets):
                print("fail 1")
                for socket in assembly.sockets:
                    print(socket)
                return False
            if not all(all(spring.validatemaxturns(turns) for spring in socket) for socket in assembly.sockets):
                print("fail 2")
                return False
            if not assembly.validatetorque(torque):
                print("fail 3")
                return False
            return True

        assemblies = func(torque = torque, turns = turns, pipe = pipe,**kw)
        print(func)
        return list(filter(validator,assemblies))
    return inner

def assemblywrapper(func):
    """ Since the most common case is a single Socket in an Assembly, this function can
    be used to wrap functions to automatically convert Socket results into Assemblies. """

    @functools.wraps(func)
    def inner(*args,**kw):
        results = func(*args,**kw)
        output = []
        def convertitem(item):
            """ Convenience Function """
            ## We don't recurse for Springs (which would then convert to Assembly) 
            ## because this Spring may be part of a list of single-spring sockets
            if isinstance(item,Spring):
                return Socket(item)
            ## Sockets get converted to Assemblies
            if isinstance(item,Socket):
                assembly = Assembly()
                assembly.addsocket(item)
                return assembly
            ## Assemblies are already in the end state
            if isinstance(item,Assembly):
                return item
            ## Lists that are passed to this function should only contain Sockets
            ## (which are used to construct an Assembly)
            if isinstance(item,(list,tuple)):
                if not all(isinstance(x,Socket) for x in item):
                    raise ValueError(f"Lists should only contain Sockets: {item}")
                asssembly = Assembly()
                for socket in item: assembly.addsocket(socket)
                return assembly
            ## Anything else is an Exception
            raise ValueError(f"Invalid Item: {item}")
        def sortout(item):
            """ Separate sorting function for recurse-ability """
            ## Springs should be unlikely, but both it's converted first to a Socket in
            ## convertitem, which then recurses
            if isinstance(item,(Spring,Socket)): return sortout(convertitem(item))
            ## We don't have to worry about wrapping it
            if isinstance(item,Assembly): return output.append(item)
            ## Handle Lists
            if isinstance(item,(list,tuple)):
                ## List is an unassembled Assembly
                if all(isinstance(x,(Socket,Spring)) for x in item):
                    out2 = []
                    for x in item:
                        if isinstance(x,Spring):
                            x = convertitem(x)
                        ## There should only be sockets now
                        out2.append(convertitem(x))
                    ## sortout the Assembly created by convertitem(list_of_sockets)
                    ## This should probably just be rewritten to "return output.append(convertitem(out2))"
                    ## but we're going to throw it back through incase convertitem returns a bad value
                    return sortout(convertitem(out2))
                ## Lists of Assemblies are flattened
                if all(isinstance(x,Assembly) for x in item):
                    for x in item: output.append(x)
                    return
            ## Everything else are Exceptions
            raise ValueError(f"Could not sort item: {item}")

        if not isinstance(results, (list,tuple)):
            results = [results,]
        for out in results:
            sortout(out)
        return output
        ## } <inner>

    return inner

def get_all_compounds(pipe = None):
    """ Based on the given pipe, return a list of all 2-Spring Compound sockets that will fit inside.
   
        This only validates that each inner wire will fit inside the outer wire and that 
        the outerwire will fit inside the pipe: it DOES NOT validate that the given
        set of springs will be valid for any given amount of required torque (if at all).
    """
    pipe = validate_assembly_pipe(pipe)
    output = _get_all_compound_springs(pipe = pipe)
    return [Socket(*[Spring(**spring, cycles = pipe.cycles) for spring in springs]) for springs in output]

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
            outerspring = Spring(wire = outer, od = out_od, cycles = pipe.cycles)

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
        print(fun,res)
        output.extend(res)

    return output

@assemblywrapper
def generate_single_spring(torque, turns, pipe = None):
    """ Generates a list of valid Assemblies """
    pipe = validate_assembly_pipe(pipe)
    od = max([od for od in WIREODINDEX if od <= pipe.max_wireod])
    ## Get a list of springs that will fit inside the OD
    potential_springs = [Spring(wire = wire['wirediameter'], od = od, cycles = pipe.cycles) for wire in WIRE.values() if wire['min_od'] <= od]
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
        spring = Spring(wire, od = pipe.max_wireod, cycles= pipe.cycles)
        ## Strongest a spring can be is when turns is equal to max turns
        ## Max turns is MP / Torque, therefore Torque = MP / Max Turns
        ## 1.05 is a safety factor (increased from 1.015)
        st = spring.mp / turns / 1.05
        ## If outerwire can do all the pulling itself, we won't return it with this method
        ## (generate_single_springs will return it)
        if st >= torque * .95:
            continue
        spring.setlengthbytorque(st)
        print(torque, st, spring.lift)
        remaining = torque - spring.lift
        maxod = max(od for od in SPRINGOD if od and od < spring.id)
        modmp = turns * remaining / pipe.cyclerating
        inners = [wire for wire in iterwire(reverse = True) if wire['min_od'] <= maxod and wire['mp_base'] > turns * remaining / pipe.cyclerating]
        for inner in inners:
            innerspring = Spring(inner, od = maxod, cycles = pipe.cycles)
            innerspring.setlengthbytorque(remaining)
            assembly = Socket(spring,innerspring)


            if assembly.validate(turns):
                return assembly
    
    ## TODO: Mostly a placeholder; not sure whether to raise Exception if no compounds generated or just return an empty list.
    return []
        
""" The Following is Old Code that should be Deprecated that we're saving temporarily, just in case """
#class Assembly():
#    def __init__(self, totalturns, outerspring, innerspring=None):
#        self.totalturns = totalturns ## TT; door.totalturns
#        self.outerspring=outerspring
#        self.innerspring = innerspring

#class SingleAssembly(Assembly):
#    def __init__(self, totalturns, outerspring, innerspring = None):
#        super().__init__(totalturns = totalturns, outerspring=outerspring, innerspring=innerspring)
#        self.outerspring._LI = lambda spring: spring.liftrate / self.requiredtorque ## LR / IP
#    def validate(self):
#        return validate_single_spring

#class DuplexAssembly(Assembly):
#    def __init__(self, totalturns, outerspring, innerspring = None):
#        super().__init__(totalturns = totalturns, outerspring = outerspring, innerspring = innerspring)
#        self.outerspring._LI = lambda spring: spring.liftrate / (spring.MP / self.totalturns) ## LR / ( MP / TT)
#        self.innerspring._LI = lambda spring: spring.liftrate / (self.requiredtorque - self.outerspring.torque) ## LR / ( IP - S1 )
#    def validate(self):
#        return validate_outer_inner_spring

#class Spring():
#    def __init__(self,cycles,outerdiameter,wireindex, lenthuncoiled = None, stretch = 0):
#        self.cycles = cycles
#        self.outerdiameter = outerdiameter ## OD
#        self.wireindex = wireindex
#        if lenthuncoiled is None:
#            def lenthuncoiled(*args,**kw): raise AttributeError("Spring lenthuncoiled is not Set")
#        self._lenthuncoiled = lenthuncoiled
#        self._stretch = stretch
#    @property
#    def stretch(self):
#        return self._stretch
#    @stretch.setter
#    def stretch(self,value):
#        try: value = float(value)
#        except: raise AttributeError("Spring Stretch must be numeric")
#        if value < 0:
#            raise AttributeError("Spring Stretch cannot be negative")
#        self._stretch = value
#    @property
#    def coillength(self):
#        """ Returns the length of a single coil """
#        return self.meandiameter * math.pi

#    @property
#    def cyclecompensation(self):
#        return CYCLES[self.cycles]['torquepercentage']
#    @property
#    def averagetensile(self): ## AT
#        return WIRELOOKUP[self.wireindex]['averagetensile']
#    @property
#    def liftrate(self): ## LR
#        return WIRELOOKUP[self.wireindex]['liftrate']
#    @property
#    def weightperinch(self): ## LW
#        return WIRELOOKUP[self.wireindex]['weightperinch']
#    @property
#    def wirediameter(self): ## WD
#        return WIRELOOKUP[self.wireindex]['wirediameter']

#    @property
#    def lengthcoiled(self): ## LC
#        return self.numberofcoils * self.wirediameter
#    @property
#    def lenthuncoiled(self):
#        return self._lenthuncoiled(self)
#    @property
#    def liftpercoillength(self): ## CN
#        return self.liftrate / self.coillength
#    @property
#    def maxturns(self): ## MT
#        return self.MP / self.torque
#    @property
#    def meandiameter(self): ## MD
#        return self.outerdiameter - self.wirediameter

#    @property
#    def MP_base(self):
#        """ Pregenerated value equal to averagetensile * wirediameter**3 / 10.2. See MP docstring """
#        return WIRELOOKUP[self.wireindex]['mp_base']
#    @property
#    def MP(self): ## MP
#        """ Unknown abbreviation
        
#        This equation was originally springrating * wirediameter**3 / 10.2;
#        spring rating equal averagetensile * cyclecompensation and thus =>
#        averagetensile * cyclecompensation * wirediameter**3 / 10.2.
#        Since (averagetensile * wirediameter**3 / 10.2) is a constant value
#        per Spring, this value can be stored which makes future calculations
#        easier
#        """
#        return self.cyclecompensation * self.MP_base
#    @property
#    def numberofcoils(self): ## NC
#        return self.lenthuncoiled / self.coillength
#    @property
#    def springrating(self): ## SR
#        """ abbreviation is a guess """
#        return self.averagetensile * self.cyclecompensation
#    @property
#    def torque(self): ## TQ
#        return self.liftpercoillength / self.numberofcoils
#    @property
#    def weight(self): ## WS
#        return self.lenthuncoiled * self.weightperinch

#def setstretch(door,spring):
#    """ Sets the spring's required stretch based on door """
#    spring.stretch = door.totalturns * spring.wirediameter * 2

#def validate_single_spring(door):
#    """ Validates the current spring and outputs it if it is completely valid, otherwise validates
#    it as the Outer Spring, or iterates if it is completely invalid
    
#    L10050
#    """
#    outerspring = door.pipe.assembly.outerspring
#    ## TT: Total Turns, MP: ???, IP: Inch/Pound per Turn
#    if door.totalturns >= outerspring.MP / door.torqueperturn * 1.015:
#        return False

#    ## TQ: Rate Inch/Pound Calculation Holder, MT: Max Turns Calculation Holder
#    if outerspring.torque <= door.torqueperturn * 1.01 and outerspring.torque >= door.torqueperturn * .99\
#        and outerspring.maxturns >= door.totalturns*.985:
#        setstretch(door,outerspring)
#        return True

#    ## Normally, this line would validate Outer spring to prepare to iterate into a duplex
#    ## Since this function is no longer involved in iteration, we're simply returning False
#    return False

#def validate_outer_inner_spring(door):
#    return validate_outer_spring(door) and validate_inner_spring(door)

#def validate_outer_spring(door):
#    """ Checks the validity of the Outer Spring and sets it if valid, otherwise iterates W/O """
#    outerspring = door.pipe.assembly.outerspring
#    if (outerspring.MP / door.totalturns) * .99 <= outerspring.torque <= (outerspring.MP / door.totalturns)*1.015:
#        setstretch(door,outerspring)
#        return True
#    return False

#def validate_inner_spring(door):
#    """ Validates Inner and Outer Spring Calculation and sets if valid, otherwise iterates """
#    outerspring = door.pipe.assembly.outerspring
#    innerspring = door.pipe.assembly.innerspring
#    if door.totalturns >= innerspring.MP / (door.torqueperturn - outerspring.torque) * 1.015:
#        return False

#    if (door.torqueperturn - outerspring.torque) * .99 <= innerspring.torque <= (door.torqueperturn - outerspring.torque) * 1.015:
#        if door.pipe.radius < 3:
#            if outerspring.lengthcoiled - 6 >= innerspring.lengthcoiled >= 12:
#                setstretch(door,innerspring)
#                return True
#        else:
#            if outerspring.lengthcoiled - 9.600001 > innerspring.lengthcoiled > 16:
#                setstretch(door,innerspring)
#                return True
#    return False

#def validate_tandem_spring(door):
#    """ Validates calculations for Tandem Springs and sets them if Valid, otherwise iterates
    
#    L9830
#    """
#    outerspring = door.pipe.assembly.outerspring
#    if (outerspring.MP / (door.torqueperturn / 2)) * .94 >= door.totalturns >= (outerspring.MP / (door.torqueperturn / 2)) * 1.015:
#        return False

#    if (door.torqueperturn / 2)*.99 < outerspring.torque < (door.torqueperturn / 2) * 1.015:
#        setstretch(door,outerspring)
#        return True
#    return False