## Builtin
import functools
import math
## This Module
from NewDadsDoor import methods

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

## angleweight is per-foot
BOTTOMBARLOOKUP = {
    '1 1/2" x 1 1/2" x 1/8" (STL)' : dict(angleweight = 2.46, height = 2),
    '2" x 2" x 1/8" (ALUM.)' : dict(angleweight = 1.14, height = 3),
    '2" x 2" x 1/8" STEEL' : dict(angleweight = 3.3, height = 2.5),
    '2 1/2" x 2" x 1/8"' : dict(angleweight = 3.72, height = 3),
    '2 1/2" x 2" x 3/16" (STL)' : dict(angleweight = 5.5, height = 2.5),
    '2 1/2" x 2 1/2" x 1/8"' : dict(angleweight = 1.462, height = 4),
    '3" x 2" x 3/16"' : dict(angleweight = 2.14, height = 3),
    '3" x 2" x 3/16" (STEEL)' : dict(angleweight = 6.2, height = 2.5),
    'LARGE TUBULAR ALUMINUM' : dict(angleweight = 2.06, height = 4),
    'LARGE TUBULAR ALUMINUM WITH (1) 2 1/2" x 2" x 3/16" (STL) STIFFENER' : dict(angleweight = 5.16, height = 4),
    'LARGE TUBULAR ALUMINUM WITH (2) 2 1/2" x 2" x 3/16" (STL) STIFFENER' : dict(angleweight = 8.26, height = 4),
    'LARGE TUBULAR ALUMINUM WITH (2) 3" x 2" x 3/16" ALUMINUM STIFFENER' : dict(angleweight = 4.2, height = 4),
    'STANDARD TUBULAR ALUMINUM' : dict(angleweight = 1.82, height = 3.5),
    'STANDARD TUBULAR ALUMINUM WITH (1) 2" x 2" x 1/8" STEEL STIFFENER' : dict(angleweight = 3.47, height = 3.5),
    'STANDARD TUBULAR ALUMINUM WITH (1) 3" x 2" x 3/16" (STEEL) STIFFENER': dict(angleweight = 4.92, height = 3.5),
    'STANDARD TUBULAR ALUMINUM WITH (2) 3" x 2" x 3/16" (STEEL) STIFFENER': dict(angleweight = 8.020002, height = 3.5)
    }

## edgeweight is per-foot
BOTTOMEDGELOOKUP = {
    "ASTRAGAL": dict(edgeweight = .5, height = 0),
    "ELECTRIC (Miller Edge)": dict(edgeweight = .6, height = 0),
    "PNEAUMATIC (Air)": dict(edgeweight = .6, height = 1),
    }

CYCLES = {
    ## torquepercentage: TP
    12500:{"torquepercentage":1.055},
    25000:{"torquepercentage":.92},
    50000:{"torquepercentage":.79},
    100000:{"torquepercentage":.68},
    ## The following was estimated as a baseline
    16500:{"torquepercentage":1},
    }

ENDLOCKLOOKUP = {
    "STAMPED STEEL":dict(endlockweight = .09375),
    "CAST IRON":dict(endlockweight = .17)
    }

GRILLEPATTERNLOOKUP ={
    "ASL":dict(TL = 4.5, LC = 4.625),
    "CSL":dict(TL = 9, LC = 9.25),
    }

PIPELOOKUP = {
    ## Both 4- and 6-inch pipes have a 4.25 radius when Barrelrings are added
    ## We do not normally make larger pipes and therefore do not have barrelring sizes; a
    ## default of 1 does not seem unreasonable and allows for the pipe.barrelrings attribute
    ## to be set to the ring height if necessary
    ## radius: IL, shaft: IS, I4:I4, weight: WT
    ## A[41]
    '4 INCH TUBE': dict(radius=2.25,    shaft = "1 1/4",   I4 = 5.86,  weight = 8.56*2.5, barrelringsize = 2),
    ## A[42]
    '4 INCH PIPE': dict(radius=2.25,    shaft = "1 1/4",   I4 = 7.23,  weight = 10.79*2, barrelringsize = 2),
    ## A[43]
    '6 INCH TUBE': dict(radius=3.3125,    shaft = "1 1/2",   I4 = 19.71,  weight =12.93*2.93, barrelringsize = .9375),
    ## A[44]
    '6 INCH PIPE': dict(radius=3.3125,    shaft = "1 1/2",   I4 = 28.1,  weight = 18.97*1.75, barrelringsize = .9375), 
    ## A[45]
    '8 INCH PIPE': dict(radius=4.3125,  shaft = "1 3/4",   I4 = 72.5,  weight = 28.55*1.7, barrelringsize = 0), 
    ## A[46]
    '10 INCH PIPE': dict(radius=5.375,   shaft = "2",       I4 = 161,  weight = 40.48*1.7, barrelringsize = 0), 
    ## A[47]
    '12 INCH PIPE': dict(radius=6.375,   shaft= "2 1/2",   I4 = 279,  weight = 49.56*2, barrelringsize = 0), 
    ## A[48]
    '14 INCH <30> PIPE': dict(radius=7,       shaft = "3",       I4 = 372,  weight = 54.57+50, barrelringsize = 0), 
    ## A[49]
    '14 INCH <40> PIPE': dict(radius=7,       shaft = "3",       I4 = 428,  weight = 63.37+50, barrelringsize = 0), 
    ## A[50]
    '16 INCH <30> PIPE': dict(radius=8,       shaft = "3",       I4 = 561,  weight = 62.58+55, barrelringsize = 0), 
    ## A[51]
    '16 INCH <40> PIPE': dict(radius=8,       shaft = "3",       I4 = 730,  weight = 82.77+55, barrelringsize = 0), 
    }

## A lookup strictly for pipes based on numeric size
PIPESIZES = {
    4: PIPELOOKUP["4 INCH PIPE"],
    6: PIPELOOKUP["6 INCH PIPE"],
    8: PIPELOOKUP["8 INCH PIPE"],
    10: PIPELOOKUP["10 INCH PIPE"],
    12: PIPELOOKUP["12 INCH PIPE"],
    }

## For Pipe Adjusters, 0 means Default- which is 6- and
### ratio is a ratio of the default (ergo, 0/6 = 0 Ratio)
PIPEADJUSTERLOOKUP = {
    0:dict(ratio = 0),
    4:dict(ratio = .42),
    6:dict(ratio = 0),
    }

RODLOOKUP = {
    "ALUM. LINKS/PLASTIC TUBES": dict(rodweight = .02544),
    "MILL ALUMINUM":dict(rodweight = .0272176),
    "ANODIZED ALUMINUM":dict(rodweight = .0272176),
    "DURANODIC ALUMINUM" : dict(rodweight = .0272176),
    "LEXAN INSERTS":dict(rodweight = .0355171),
    }

## The original program used both a numerical index and the slat name
SLATINDEXCONVERSION = {
    1 : "3 5/8 INCH CROWN SLAT",
    2 : "2 7/8 INCH CROWN SLAT",
    3 : "2 1/2 INCH FLAT SLAT",
    4 : "MIDGET CROWN SLAT < 2 INCH >",
    5 : "SOLID SLATS AT BOTTOM OF ROLLING GRILLE",
    6 : "PERFORATED SLATS"
    }

SLATLOOKUP ={
    ## <1>
    "3 5/8 INCH CROWN SLAT":dict(slatheight = 3.625, increaseradius = .5, 
           GAGE={
               "20":dict(SG = "20", slatweight=.058514166),
               "22":dict(SG = "22", slatweight=float("5.78666E-02"))
               }),
    ## <2>
    "2 7/8 INCH CROWN SLAT":dict(slatheight = 2.875, increaseradius = .6,
           GAGE={
               18:dict(SG = "18", slatweight=.071269154),
               20:dict(SG = "20", slatweight=float("5.485475E-02")),
               }),
    ##  <3>
    "2 1/2 INCH FLAT SLAT":dict(slatheight = 2.625, increaseradius = .715,
           GAGE={
               18:dict(SG = "18", slatweight=.071269154),
               20:dict(SG = "20", slatweight=float("5.729167E-02"))
               }),
    ##  <4>
    "MIDGET CROWN SLAT < 2 INCH >":dict(increaseradius = .438),
    ## <5>
    "SOLID SLATS AT BOTTOM OF ROLLING GRILLE":dict(RS=2.25,increaseradius=.815),
    ## <6> 
    "PERFORATED SLATS":dict(slatheight=2.5,increaseradius=.82,slatweight=.07388854,SG="22/22"),
    }

## Gap Required between tandem castings
CASTINGGAP = 3.5

SPRINGOD = [None, 2.75, 3.75, 5.625, 7.5, 9.5, 11.5]

WIRELOOKUP = [
    ## wirediameter: WD, liftrate: LR, weightperinch:weightperinch, averagetensile:AT (guess), mp_base: MP before Cycle Adjustment (AT * WD^3 * 10.2); this number was generated since it was constant
    None,
    dict(wirediameter= .1875  , liftrate=   11420 ,   weightperinch= .0078142 ,    averagetensile= 222500 , mp_base =   143.791647518382 , min_od = 2.75 ),
    dict(wirediameter= .25    , liftrate=   36093 ,   weightperinch= .0138916 ,    averagetensile= 212500 , mp_base =   325.520833333333 , min_od = 2.75 ),
    dict(wirediameter= .3125  , liftrate=   88119 ,   weightperinch= .0217083 ,    averagetensile= 202500 , mp_base =   605.863683363971 , min_od = 2.75 ),
    dict(wirediameter= .375   , liftrate=  182724 ,   weightperinch= .0312583 ,    averagetensile= 197500 , mp_base =  1021.08226102941  , min_od = 3.75 ),
    dict(wirediameter= .40625 , liftrate=  251546 ,   weightperinch= .0366833 ,    averagetensile= 191000 , mp_base =  1255.49017214308  , min_od = 3.75 ),
    dict(wirediameter= .4375  , liftrate=  338448 ,   weightperinch= .0425416 ,    averagetensile= 190000 , mp_base =  1559.86711090686  , min_od = 3.75 ),
    dict(wirediameter= .46875 , liftrate=  445807 ,   weightperinch= .0488416 ,    averagetensile= 185000 , mp_base =  1868.07969037224  , min_od = 3.75 ),
    dict(wirediameter= .5     , liftrate=  577500 ,   weightperinch= .0555666 ,    averagetensile= 180000 , mp_base =  2205.88235294118  , min_od = 5.625 ),
    dict(wirediameter= .5625  , liftrate=  925044 ,   weightperinch= .070325  ,    averagetensile= 175000 , mp_base =  3053.55296415441  , min_od = 5.625 ),
    dict(wirediameter= .625   , liftrate= 1409913 ,   weightperinch= .0868335 ,    averagetensile= 172500 , mp_base = 41288.4880514706   , min_od = 5.625 )
    ]

WIRE = {wire['wirediameter']:wire for wire in WIRELOOKUP if wire}

WIREINDEX = {
    .1875: 1,
    .25: 2,
    .3125: 3,
    .375: 4,
    .40625: 5,
    .4375: 6,
    .46875: 7,
    .5: 8,
    .5625: 9,
    .625: 10,
    }

def iterwire(reverse = False):
    """ A helper function for ignoring the blank 0-index. Provides reverse iteration as well (reverse = True). """
    if not reverse:
        for wire in WIRELOOKUP[1:]: yield wire
    else:
        for wire in WIRELOOKUP[-1:0:-1]: yield wire

## This is an estimation of the weight of any wire per inch^3 of volume
WIREWEIGHTCUBEINCH = 0.283008608782093

def iswiredict(wire):
    """ Validates that a dictionary contains all required keys to be a wire dict """
    if not isinstance(wire,dict): return False
    return not any(wire.get(key,None) is None or not isinstance(wire[key],vtype)
                   for key,vtype in
                   [('wirediameter',float),('liftrate',(float,int)),
                    ('averagetensile',(float,int)), ('mp_base',(float,int)),
                    ('min_od',(float,int))]
                   )
WIREODINDEX = [2.75, 3.75, 5.625]

DEFAULTS = {
    "2 1/2 INCH FLAT SLAT":dict(
        endlocks="STAMPED STEEL",
        gage=20
        ),
    "2 7/8 INCH CROWN SLAT":dict(
        endlocks="CAST IRON",
        gage=20
        ),

    }

## Number of Slats for the wrap
WRAPSLATS = 7

def rounduptofraction(number,fraction):
    """ Rounds a number to a fraction """
    recipricol = 1/fraction
    return math.ceil(number * recipricol) / recipricol


def measurementconversion(function):
    """ A Wrapper which checks if an instance method's 'value' argument is a string reperesenting a measurement
   
    Note that this function is for instance methods and automatically assumes "self"
    Converts the string to inches as a float.
    """
    @functools.wraps(function)
    def inner(self,*args,value=None,**kw):
        argflag = False
        if value is None:
            if not args: return function(self,*args,**kw)
            args = list(args)
            value = args.pop(0)
            argflag = True
        if isinstance(value,str):
            value = methods.convertmeasurement(value)
        if argflag: args = [value,] + args
        else: kw['value'] = value
        return function(self,*args,**kw)
    return inner

class Door():
    def __init__(self,width = 0, upset = None):
        self.curtainfactory = Curtain
        self.pipefactory = Pipe
        self._curtain = None
        self._pipe = None
        self._width = 0
        self.width = width
        self.bracketplatesize = 18
        if upset is None: upset = 2
        self.upset = upset

    @property
    def curtain(self):
        return self._curtain
    @curtain.setter
    def curtain(self,value):
        if not isinstance(value,Curtain): raise AttributeError("Door's curtain must be Curtain Instance")
        self._curtain = value
    @property
    def pipe(self):
        return self._pipe
    @pipe.setter
    def pipe(self,value):
        if not isinstance(value,Pipe): raise AttributeError("Door's pipe must be Pipe Instance")
        self._pipe = value

    def setcurtain(self,width = None, **kw):
        """ A constructor function to initialize and add a curtain
        
        Does not accept positional arguments. If width is not supplied, width will be set
        automatically
        """
        if not self.curtainfactory: raise AttributeError("Door's curtainfactory is not set")
        width = self.width
        curtain = self.curtainfactory(width = width,**kw)
        self.curtain = curtain
    def setpipe(self,**kw):
        """ A constructor function to initialize and add a pipe 
        
        Does not accept positional arguments,
        """
        if not self.pipefactory: raise AttributeError("Door's pipefactory is not set")
        pipe = self.pipefactory(**kw)
        self.pipe = pipe

    @property
    def width(self):
        return self._width
    
    @measurementconversion
    @width.setter
    def width(self,value):
        self._width = value
        if self.curtain: self.curtain.width = value

    @property
    def bracketplate(self):
        return BracketPlate(size = self.bracketplatesize)

    @property
    def openheight(self):
        """ Returns the distance between the stops and the center of the bracket plates

        Note that for a door with standard upset and standard bracket plates, this number
        is constant regardless of size of door
        """
        return self.pipecenterlineheight - self.curtain.stopheight - self.curtain.getbottombarheight()

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
        return self.initialradius + (self.turnstoraise * self.curtain.slat.increaseradius)

    @property
    def hangingweight_closed(self): ## HW
        """ Total weight of the Curtain (when closed)"""
        ## Slat Weight
        ## Bottom Bar Weight
        ## Endlock Weight
        ## Grille Weight
        ## Weight Loss from perforated Slats
        return self.curtain.getslatweight(self.slatstocenterline) \
            + self.curtain.getbottombarweight() \
            + self.curtain.getendlockweight(self.slatstocenterline / 2) \
            + self.curtain.getgrilleweight() \
            - self.curtain.perforatedweightloss

    @property
    def hangingweight_open(self): ## WU
        """ Weight of the Curtain when the door is Open """
        ## This is the area between the pipecenterline and the stopheight, less the bottombar
        ## Note, this was parsed out for testing purposes
        openheight = self.openheight
        ##       Normal Door
        ## +--------------------+
        ## |xxxxxxxxxxxxxxxxxxxx| <- Pipe Center Line
        ## +--xxxxxxxxxxxxxxxx--+ <- Bottom Pipe
        ## |xxxxxxxxxxxxxxxxxxxx| <- Gap between Stops and pipe
        ## |]mmmmmmmmmmmmmmmmmm[| <- Bottom Bar / Stops
        bottomslatheight =  min(self.curtain.floortogrille, openheight)
        ##  Right Hand Pass Door
        ## +--------------------+
        ## |xxxxxxxxxxxxxxxxxxxx| <- Pipe Center Line
        ## +--xxxxxxxxxx--------+ <- Bottom Pipe
        ## |xxxxxxxxxxxx        | <- Gap between Stops and pipe
        ## |]mmmmmmmmmmm       [| <- Bottom Bar / Stops
        ##         Grille
        ## +--------------------+
        ## |?x?\?x?\?x?\?x?\?x?\| <- Pipe Center Line           (Grille or Top Slats)
        ## +\-\-\-\-\-\-\-\-\-\-+ <- Bottom Pipe                (Grille)
        ## |xxxxxxxxxxxxxxxxxxxx| <- Gap between Stops and pipe (Bottom Slats)
        ## |]mmmmmmmmmmmmmmmmmm[| <- Bottom Bar / Stops
        bottomslats = self.curtain.getnumberslats(bottomslatheight)
        remainingheight = openheight - bottomslatheight
        ## Get Grille Section size
        grilleheight = min(self.curtain.getgrilleheight(), remainingheight)
        ## In the case of non-grille (or passdoor), the remaining height will not change
        remainingheight = remainingheight - grilleheight
        ## In practice, top slats should be excedingly rare, but this is included just in case
        topslats = self.curtain.getnumberslats(remainingheight)
        weight = self.curtain.getbottomslatweight(bottomslats)\
            + self.curtain.getendlockweight(bottomslats/2)\
            + self.curtain.getgrilleweight(self.curtain.getnumberrods(grilleheight))\
            + self.curtain.gettopslatweight(topslats)\
            + self.curtain.getendlockweight(topslats/2)\
            + self.curtain.getbottombarweight()
        if self.curtain.stopheight >=192: return weight * 1.2
        if self.curtain.stopheight < 50: return weight + 5
        #if 50 < self.curtain.stopheight < 100: return weight + 10
        return weight * 1.1

    @property
    def pipecenterlineheight(self): ## HC
        """ Height from the floor to the center of the Pipe """
        ## Stop Height + Upset + Half Bracket Plate Height (Pipe is centered on bracket plates)
        return self.curtain.stopheight + self.upset + self.bracketplate.height/2

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
    def slatstocenterline(self): ## NS
        """ Number of Slats to Centerline of Pipe """
        grille = 0
        if self.curtain.grille:
            grille = self.curtain.grille.getheight(self.curtain.grille.numberofrods-1)
        ## Distance from Floor to Centerline - BottomBar Height - 1.5 - Grille Section
        return self.curtain.getnumberslats(self.pipecenterlineheight - self.curtain.bottombar.height - 1.5\
           - grille )

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
        A = math.pi * self.curtain.slat.increaseradius
        ## B: Base Circumference each Turn (per Pipe)
        B = 2 * math.pi * self.pipe.totalradius
        ## C: Stop Height
        C = -self.curtain.stopheight_adjusted
        ## Solve quadratic
        return (-B + math.sqrt(B**2 - 4*A*C)) / (2*A)

    def gettotalslats(self):
        """ Gets the total number of slats with calculated wraps slats """
        if not self.curtain: raise AttributeError("Door's curtain is not set")
        return self.getwrapslats() + self.curtain.getnumberslats(self.curtain.stopheight)
    def getwrapslats(self):
        """ Gets the calculated number of wrap slats """
        if not self.curtain or not self.pipe: raise AttributeError("Door's curtain and pipe are not currently set")
        return self.curtain.getnumberslats(
            2 * math.pi * self.pipe.totalradius * (.75 - self.pipe.getadjusterratio()) +\
           self.pipecenterlineheight - self.curtain.getslatheight(self.curtain.getnumberslats()+1)
            )

    def validatepipesize(self):
        return self.pipe.weight + self.curtain.hangingweight_closed <= self.pipe.maxdeflectionweight * .97

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

class Curtain():
    """ The Base-class of Curtain. Assumes no Grille or Vision sections (see subclasses).

    width and stopheight are in inches
    """
    def __init__(self,width, stopheight, doortype = None, extrudedguides = False, slattype = None, slatgage = None, endlocktype = None, windlocks = 0, hasbottombar = True, bottombarangle = None, bottombaredge = None):
        self._stopheight = 0
        self.stopheight = stopheight
        self._width = 0
        self.width = width
        self._doortype = None
        self.doortype = doortype
        self.extrudedguides = extrudedguides
        if slattype is None: slattype = "2 1/2 INCH FLAT SLAT"
        if slattype not in SLATLOOKUP:
            ## We'll assume slattype is a number
            if isinstance(slattype,str):
                slattype = int(slattype.strip())
            else: slattype = int(slattype)
            slattype = SLATINDEXCONVERSION[slattype]
        self.slattype = slattype
        if slatgage is None: slatgage = DEFAULTS[self.slattype]["gage"]
        elif isinstance(slatgage,str): slatgage = int(slatgage.strip())
        else: slatgage = int(slatgage)
        self.slatgage = slatgage
        if endlocktype is None: endlocktype = DEFAULTS[self.slattype]["endlocks"]
        self.endlocktype = endlocktype
        self.windlocks = int(windlocks)
        ## Bottom bars handle defaults
        self.hasbottombar = hasbottombar
        self.bottombarangle = bottombarangle
        self.bottombaredge = bottombaredge

    @property
    def stopheight(self):
        return self._stopheight

    @stopheight.setter
    @measurementconversion
    def stopheight(self,value):
        self._stopheight = value

    @property
    def width(self):
        return self._width
    @width.setter
    @measurementconversion
    def width(self,value):
        self._width = value

    @property
    def slatlength(self):
        """ A Curtain's Slat length is often wider than the width """
        ## TODO Create FireDoorCurtain Subclass
        length = self.width
        if not self.endlocktype:
            if self.slattype in ["3 5/8 INCH CROWN SLAT","2 7/8 INCH CROWN SLAT"]: length += 1
            elif self.slattype == "2 1/2 INCH FLAT SLAT": length += .25
        if self.endlocktype == "CAST IRON" and self.slattype == "2 1/2 INCH FLAT SLAT":
           length -= .5

        if self.extrudedguides:
            return length + 2.5
        if self.slattype == "PERFORATED SLATS":
            if not self.windlocks:
                if self.width <= 149: return length + 3.875
                if self.width < 264: return length + 4.25
            else:
                if self.width <= 293: return length + 4
                return length + 5
        if self.slattype in ["3 5/8 INCH CROWN SLAT","2 7/8 INCH CROWN SLAT"]:
            if not self.windlocks:
                if self.width < 149: return length + 3.5
                if self.width <=221: return length + 3.875
        if self.slattype == "2 7/8 INCH CROWN SLAT":
            if self.windlocks:
                if self.width < 293: return length + 3.875
                return length + 4.875
        if not self.extrudedguides:
            if self.width < 149: return length + 3.5
            if self. width < 221: return length + 3.875
            if self.width < 293: return length + 4.5
            if self.width <= 365: return length + 5.5
        if self.slattype == "2 1/2 INCH FLAT SLAT":
            if not self.windlocks:
                if self.width < 149: return length + 4.25
                if self.width < 197: return length + 4.625
            else:
                if self.width < 293: return length + 4
                return length + 5
        if self.slattype == "MIDGET CROWN SLAT < 2 INCH >":
            if self.width < 149: return length + 3.75
            return length + 4.125


    @property
    def bottombar(self):
        if self.hasbottombar:
            return BottomBar(width = self.slatlength, slatweight = self.slat.slatweight ,angle = self.bottombarangle, edge = self.bottombaredge)
    @property
    def doortype(self):
        return self._doortype
    @doortype.setter
    def doortype(self,value):
        self._doortype = value
    @property
    def grille(self):
        return None
    @property
    def slat(self):
        return Slat(self.slattype, self.slatgage)
    @property
    def endlock(self):
        return Endlock(self.endlocktype)
    @property
    def floortogrille(self):
        return self.stopheight
    @property
    def perforatedslats(self):
        return 0
    @property
    def perforatedweightloss(self):
        return 0
    @property
    def stopheight_adjusted(self):
        return self.stopheight - (self.bottombar.stopheightadjustment() if self.bottombar else 0)

    @property
    def totalweight(self):
        return self.getslatweight(self.totalslats) + self.getendlockweight(math.ceil(self.totalslats/2)) + self.bottombar.weight
    @property
    def totalslats(self, wrapslats = WRAPSLATS):
        return self.getnumberslats() + wrapslats

    def getbottombarheight(self):
        """ Returns height of bottombar if curtain has one """
        if self.bottombar: return self.bottombar.height
        return 0 
    def getbottombarweight(self):
        """ Returns weight of bottombar if curtain has one """
        if self.bottombar: return self.bottombar.weight
        return 0

    def getendlockweight(self,slats = None):
        """ Returns the endlock weight given the number of slats that have endlocks """
        if slats is None: slats = self.totalslats / 2
        if slats == 0: return 0
        if self.windlocks:
            endlockweight = (((slats / self.windlocks) * .656) / slats ) + .17
        else: endlockweight = self.endlock.endlockweight
        ## Endlock on each side
        return slats * endlockweight * 2
    def getgrilleheight(self, rods = None):
        """ Returns the height of the grille, if any """
        return 0
    def getgrilleweight(self, rods = None):
        """ Returns the weight of the grille, if any """
        return 0
    def getnumberrods(self,height):
        """ Returns the number of rods needed for the given height """
        return 0
    def getnumberslats(self,height = None):
        """ Returns the number of slats needed for the given height """
        if height is None: height = self.stopheight_adjusted
        return math.ceil(height / self.slat.slatheight)
    def getslatweight(self,slats):
        """ Returns the slat weight given the number of slats """
        return slats * self.slatlength * self.slat.slatweight
    def getbottomslatweight(self,slats):
        """ Returns the weight for bottom slats (requires subclass) """
        return self.getslatweight(slats)
    def gettopslatweight(self,slats):
        """ returns the weight for top slats (requires subclass) """
        return self.getslatweight(slats)
    def getslatheight(self,slats = None):
        """ Returns the total height of the number of slats """
        if slats is None: slats = self.getnumberslats()
        return slats * self.slat.slatheight


    @property
    def perforationsperslat(self):
        """ Determine number of perforation Windows based on Curtain Width """
        ## Windows every 8.5 Inches, skip first and last window
        ## This calculation is from the original, but I would probably like it
        ## better written "(self.slatlength - edgepadding)/8.5" so that the distance
        ## from the edge can be customized (as opposed to being 8.5)
        return self.slatlength/8.5 - 2

class RollingGrilleCurtain(Curtain):
    def __init__(self,width, height,
                 rodtype,
                 doortype = None, slattype = None, slatgage = None, endlocktype = None, bottombarangle = None, bottombaredge = None,
                 floortogrille = 0, lexaninserts = False, numberofrods = 0):
        super().__init__(height, doortype, slattype, slatgage, endlocktype, bottombarangle, bottombaredge, lexaninserts)
        self.rodtype = rodtype
        self.floortogrille = floortogrille
        self.numberofrods = numberofrods
    @property
    def grille(self):
        return Grille(rodtype = self.rodtype, width = self.width + 1, lexaninserts = self.lexaninserts)
    @property
    def numberbottomslats(self):
        return max(0,self.floortogrille - self.getbottombarheight() -1.5) / self.slat.slatheight
    def getnumberrods(self,height):
        """ Returns the number of rods needed for the given height """
        return self.grille.getnumberrods(height)
    def getgrilleweight(self, rods = None):
        return self.grille.getweight(rods)
    def getgrilleheight(self, rods = None):
        return self.grille.getheight()

class perforatedCurtain(Curtain):
    def __init__(self,width, height, stopheight, doortype = None, slattype = None, slatgage = None, endlocktype = None, bottombarangle = None, bottombaredge = None,
                 perforatedslatheight = 0):
        super().__init__(height, stopheight, doortype, slattype, slatgage, endlocktype, bottombarangle, bottombaredge)
        self._perforatedslatheight = 0
    @property
    def perforatedslats(self):
        """ Returns the number of slats that have perforations (based on desired height of perforations) """
        return math.ceil(self.perforatedslatheight / self.slat.slatheight)
    @property
    def perforatedslatheight(self):
        return max(0,self._perforatedslatheight)
    @perforatedslatheight.setter
    def perforatedslatheight(self,height):
        if height > self.stopheight:
            raise AttributeError("perforatedslatheight cannot be greater than stopheight")
        self._perforatedslatheight = height

    @property
    def perforatedweightloss(self):
        ## (Slat Weight per Window-size) * Weight Loss Per Window *  Number of perforations/Slat * Number of Slats
        return (self.curtain.slat.slatweight/5.25) * 4.648175 * self.curtain.perforationsperslat * self.perforatedslats

class BottomBar():
    def __init__(self,width, slatweight, angle = None, edge = None, slope = 0):
        self.width = width
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
        ## Bottom Bar Weights were originally per-foot  (self.width/12)
        return (self.angleweight +
                self.getedgeweight())\
                    * self.width/12 + \
                    self.slopeweight + \
                    self.getfeederslatweight()
    
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
        return self.feederslatweight * self.width * .65

    @property
    def slopeweight(self):
        """ Returns the weight added by the slopped portion of the bottom bar """
        if not self.slope: return 0
        slopereach =  self.slope + 3
        reachsquarearea = slopereach * (self.width  + 1)
        slopetrianglearea = self.slope * (self.width + 1) / 2
        diff_feet = (reachsquarearea - slopetrianglearea) / 144 * 5
        return diff_feet + (self.width + 1) * .05316


    def stopheightadjustment(self):
        """ Provides the Stop Height adjustment for Large Tubular Bottom Bars (returns 0 otherwise) """
        if "large tubular" in self.angle: return 3.5
        return 0


class Grille():
    def __init__(self, rods, rodtype, width, lexaninserts = False):
        self.rods = rods
        self.rodtype = rodtype
        self.lexaninserts = lexaninserts
        self.width = width
    @property
    def height(self):
        return self.getheight()
    @property
    def rodsize(self):
        if self.lexaninserts: return 3
        return 2.25
    @property
    def rodweight(self):
        if self.lexaninserts: return RODLOOKUP["LEXAN INSERTS"]['rodweight']
        return RODLOOKUP[self.rodtype]['rodweight']
    @property
    def weight(self):
        return self.getweight()
    def getheight(self,rods = None):
        """ Gets height based on number of rods """
        if rods is None: rods = self.rods
        ## Rod Height is 3 inches if lexaninserts
        return self.rodsize * rods - 1
    def getnumberrods(self,height):
        """ Gets number of rods based on height """
        return height / self.rodsize
    @property
    def getweight(self, rods = None):
        if rods is None: rods = self.rods
        return rods * self.rodweight * self.width

class Slat():
    def __init__(self, slattype = None, gage = None):
        if slattype is None: slattype = "2 1/2 INCH FLAT SLAT"
        self.slattype = slattype
        if gage is None: gage = str(min([int(k) for k in SLATLOOKUP["GAGE"].keys()]))
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

class Endlock():
    """ At current, this class isn't really necessary. However it is used to follow
    the heavily object-oriented philosophy of this module.
    """
    def __init__(self,endlocktype):
        self.endlocktype = endlocktype

    @property
    def endlockweight(self):
        return ENDLOCKLOOKUP[self.endlocktype]['endlockweight']


class Pipe():
    def __init__(self,pipewidth, shell = None, assembly = None, barrelrings = True, adjuster = False):
        self._pipewidth = 0
        self.pipewidth = pipewidth
        self.shell = shell
        self.assembly = assembly
        self.barrelrings = barrelrings
        self.adjuster = int(adjuster)

    @property
    def pipewidth(self):
        return self._pipewidth
    
    @measurementconversion
    @pipewidth.setter
    def pipewidth(self,value):
        self._pipewidth = value

    @property
    def radius(self):
        """ Radius of the pipe by itself """
        return PIPELOOKUP[self.shell]['radius']

    @property
    def shaft(self):
        return PIPELOOKUP[self.shell]['shaft']

    @property
    def totalradius(self):
        """ Radius of the barrel (including barrelrings if used) """
        return self.radius + PIPELOOKUP[self.shell]['barrelringsize'] * int(bool(self.barrelrings))

    @property
    def weight(self):
        """ Weight of the pipe itself """
        return PIPELOOKUP[self.shell]['weight'] * (self.pipewidth/12)

    @property
    def maxdeflectionweight(self):
        """ Amount of weight that the pipe can support without bending

        This equation was taken as-is from the source code; its origins could not
        be found the handbook.
        """
        ## I4 / Width-in-feet^2 * 38667
        return PIPELOOKUP[self.shell]['I4'] / (self.pipewidth/12) ** 2 * 38667

    def getadjusterratio(self):
        if not self.adjuster: return 0
        return PIPEADJUSTERLOOKUP[self.adjuster]['ratio']

class Assembly():
    def __init__(self, totalturns, outerspring, innerspring=None):
        self.totalturns = totalturns ## TT; door.totalturns
        self.outerspring=outerspring
        self.innerspring = innerspring

class SingleAssembly(Assembly):
    def __init__(self, totalturns, outerspring, innerspring = None):
        super().__init__(totalturns = totalturns, outerspring=outerspring, innerspring=innerspring)
        self.outerspring._LI = lambda spring: spring.liftrate / self.requiredtorque ## LR / IP
    def validate(self):
        return validate_single_spring

class DuplexAssembly(Assembly):
    def __init__(self, totalturns, outerspring, innerspring = None):
        super().__init__(totalturns = totalturns, outerspring = outerspring, innerspring = innerspring)
        self.outerspring._LI = lambda spring: spring.liftrate / (spring.MP / self.totalturns) ## LR / ( MP / TT)
        self.innerspring._LI = lambda spring: spring.liftrate / (self.requiredtorque - self.outerspring.torque) ## LR / ( IP - S1 )
    def validate(self):
        return validate_outer_inner_spring

class Spring():
    def __init__(self,cycles,outerdiameter,wireindex, LI = None, stretch = 0):
        self.cycles = cycles
        self.outerdiameter = outerdiameter ## OD
        self.wireindex = wireindex
        if LI is None:
            def LI(*args,**kw): raise AttributeError("Spring LI is not Set")
        self._LI = LI
        self._stretch = stretch
    @property
    def stretch(self):
        return self._stretch
    @stretch.setter
    def stretch(self,value):
        try: value = float(value)
        except: raise AttributeError("Spring Stretch must be numeric")
        if value < 0:
            raise AttributeError("Spring Stretch cannot be negative")
        self._stretch = value
    @property
    def coillength(self):
        """ Returns the length of a single coil """
        return self.meandiameter * math.pi

    @property
    def cyclecompensation(self):
        return CYCLES[self.cycles]['torquepercentage']
    @property
    def averagetensile(self): ## AT
        return WIRELOOKUP[self.wireindex]['averagetensile']
    @property
    def liftrate(self): ## LR
        return WIRELOOKUP[self.wireindex]['liftrate']
    @property
    def weightperinch(self): ## LW
        return WIRELOOKUP[self.wireindex]['weightperinch']
    @property
    def wirediameter(self): ## WD
        return WIRELOOKUP[self.wireindex]['wirediameter']

    @property
    def lengthcoiled(self): ## LC
        return self.numberofcoils * self.wirediameter
    @property
    def LI(self):
        return self._LI(self)
    @property
    def liftpercoillength(self): ## CN
        return self.liftrate / self.coillength
    @property
    def maxturns(self): ## MT
        return self.MP / self.torque
    @property
    def meandiameter(self): ## MD
        return self.outerdiameter - self.wirediameter

    @property
    def MP_base(self):
        """ Pregenerated value equal to averagetensile * wirediameter**3 / 10.2. See MP docstring """
        return WIRELOOKUP[self.wireindex]['mp_base']
    @property
    def MP(self): ## MP
        """ Unknown abbreviation
        
        This equation was originally springrating * wirediameter**3 / 10.2;
        spring rating equal averagetensile * cyclecompensation and thus =>
        averagetensile * cyclecompensation * wirediameter**3 / 10.2.
        Since (averagetensile * wirediameter**3 / 10.2) is a constant value
        per Spring, this value can be stored which makes future calculations
        easier
        """
        return self.cyclecompensation * self.MP_base
    @property
    def numberofcoils(self): ## NC
        return self.LI / self.coillength
    @property
    def springrating(self): ## SR
        """ abbreviation is a guess """
        return self.averagetensile * self.cyclecompensation
    @property
    def torque(self): ## TQ
        return self.liftpercoillength / self.numberofcoils
    @property
    def weight(self): ## WS
        return self.LI * self.weightperinch

def setstretch(door,spring):
    """ Sets the spring's required stretch based on door """
    spring.stretch = door.totalturns * spring.wirediameter * 2

def validate_single_spring(door):
    """ Validates the current spring and outputs it if it is completely valid, otherwise validates
    it as the Outer Spring, or iterates if it is completely invalid
    
    L10050
    """
    outerspring = door.pipe.assembly.outerspring
    ## TT: Total Turns, MP: ???, IP: Inch/Pound per Turn
    if door.totalturns >= outerspring.MP / door.torqueperturn * 1.015:
        return False

    ## TQ: Rate Inch/Pound Calculation Holder, MT: Max Turns Calculation Holder
    if outerspring.torque <= door.torqueperturn * 1.01 and outerspring.torque >= door.torqueperturn * .99\
        and outerspring.maxturns >= door.totalturns*.985:
        setstretch(door,outerspring)
        return True

    ## Normally, this line would validate Outer spring to prepare to iterate into a duplex
    ## Since this function is no longer involved in iteration, we're simply returning False
    return False

def validate_outer_inner_spring(door):
    return validate_outer_spring(door) and validate_inner_spring(door)

def validate_outer_spring(door):
    """ Checks the validity of the Outer Spring and sets it if valid, otherwise iterates W/O """
    outerspring = door.pipe.assembly.outerspring
    if (outerspring.MP / door.totalturns) * .99 <= outerspring.torque <= (outerspring.MP / door.totalturns)*1.015:
        setstretch(door,outerspring)
        return True
    return False

def validate_inner_spring(door):
    """ Validates Inner and Outer Spring Calculation and sets if valid, otherwise iterates """
    outerspring = door.pipe.assembly.outerspring
    innerspring = door.pipe.assembly.innerspring
    if door.totalturns >= innerspring.MP / (door.torqueperturn - outerspring.torque) * 1.015:
        return False

    if (door.torqueperturn - outerspring.torque) * .99 <= innerspring.torque <= (door.torqueperturn - outerspring.torque) * 1.015:
        if door.pipe.radius < 3:
            if outerspring.lengthcoiled - 6 >= innerspring.lengthcoiled >= 12:
                setstretch(door,innerspring)
                return True
        else:
            if outerspring.lengthcoiled - 9.600001 > innerspring.lengthcoiled > 16:
                setstretch(door,innerspring)
                return True
    return False

def validate_tandem_spring(door):
    """ Validates calculations for Tandem Springs and sets them if Valid, otherwise iterates
    
    L9830
    """
    outerspring = door.pipe.assembly.outerspring
    if (outerspring.MP / (door.torqueperturn / 2)) * .94 >= door.totalturns >= (outerspring.MP / (door.torqueperturn / 2)) * 1.015:
        return False

    if (door.torqueperturn / 2)*.99 < outerspring.torque < (door.torqueperturn / 2) * 1.015:
        setstretch(door,outerspring)
        return True
    return False