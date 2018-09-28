## Builtin
import collections
import itertools
import math
import re

## Default Bracket Plate Size
BRACKETPLATESIZE = 18

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


def checkendlockalias(value):
    """ Checks if a string value is an alias for the Base Endlock Types ("STAMPED STEEL" and "CAST IRON")
    and return that Base Type if it is; otherwise returns False (even if the value is not a string) """
    if not isinstance(value,str):
        return False
    value = re.sub("\s",  ## replace all whitespace
                   "",
                   value.lower() ## Lower\
                       .replace("endlock","") ## Remove  "endlock" (as it's unnecessary
                       )
    if value not in itertools.chain.from_iterable(ENDLOCKALIASES): return False
    for index,basetype in enumerate(ENDLOCKALIASES):
        if value in basetype: break
    return list(ENDLOCKLOOKUP)[index]
    

## lower(), replace("endlock",""), and sub("\s","")
## checkendlockalias() is the prefered function for interfacing with this list
ENDLOCKALIASES = [
    ["stampedsteel","flatstamped","flstp",],
    ["castiron","flatcast","flatcastwindlock","curvedcast","curvedcastwindlock","flcst","flcwd","crcst","crcwd"],
                  ]

ENDLOCKLOOKUP = collections.OrderedDict([
    ("STAMPED STEEL",dict(endlockweight = .09375)),
    ("CAST IRON",dict(endlockweight = .17)),
    ])

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
    '4 INCH TUBE': dict(size = 4, radius=2.25,    shaft = "1 1/4",   I4 = 5.86,  weight = 8.56*2.5, barrelringsize = 2),
    ## A[42]
    '4 INCH PIPE': dict(size = 4, radius=2.25,    shaft = "1 1/4",   I4 = 7.23,  weight = 10.79*2, barrelringsize = 2),
    ## A[43]
    '6 INCH TUBE': dict(size = 6, radius=3.3125,    shaft = "1 1/2",   I4 = 19.71,  weight =12.93*2.93, barrelringsize = .9375),
    ## A[44]
    '6 INCH PIPE': dict(size = 6, radius=3.3125,    shaft = "1 1/2",   I4 = 28.1,  weight = 18.97*1.75, barrelringsize = .9375), 
    ## A[45]
    '8 INCH PIPE': dict(size = 8, radius=4.3125,  shaft = "1 3/4",   I4 = 72.5,  weight = 28.55*1.7, barrelringsize = 0), 
    ## A[46]
    '10 INCH PIPE': dict(size = 10, radius=5.375,   shaft = "2",       I4 = 161,  weight = 40.48*1.7, barrelringsize = 0), 
    ## A[47]
    '12 INCH PIPE': dict(size = 12, radius=6.375,   shaft= "2 1/2",   I4 = 279,  weight = 49.56*2, barrelringsize = 0), 
    ## A[48]
    '14 INCH <30> PIPE': dict(size = 14, radius=7,       shaft = "3",       I4 = 372,  weight = 54.57+50, barrelringsize = 0), 
    ## A[49]
    '14 INCH <40> PIPE': dict(size = 14, radius=7,       shaft = "3",       I4 = 428,  weight = 63.37+50, barrelringsize = 0), 
    ## A[50]
    '16 INCH <30> PIPE': dict(size = 16, radius=8,       shaft = "3",       I4 = 561,  weight = 62.58+55, barrelringsize = 0), 
    ## A[51]
    '16 INCH <40> PIPE': dict(size = 16, radius=8,       shaft = "3",       I4 = 730,  weight = 82.77+55, barrelringsize = 0), 
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

## Standard Length of the Charge portion of the Shaft 
## (the portion outside the Shell on the Charge side)
CHARGESHAFTLENGTH = 9

RODLOOKUP = {
    "ALUM. LINKS/PLASTIC TUBES": dict(rodweight = .02544),
    "MILL ALUMINUM":dict(rodweight = .0272176),
    "ANODIZED ALUMINUM":dict(rodweight = .0272176),
    "DURANODIC ALUMINUM" : dict(rodweight = .0272176),
    "LEXAN INSERTS":dict(rodweight = .0355171),
    }

def checkslattype(value):
    """ Given a string or integer value, attempts to determine the correct type of slat.
    Returns the slat if found, otherwise False (even for invalid value types). Functions
    very closely to checkendlocktype. """
    if not isinstance(value,(str,int)):
        return False
    if isinstance(value,int):
        if value in SLATINDEXCONVERSION:
            value = SLATINDEXCONVERSION[value]
        else: return False
    value = re.sub("\s",  ## replace all whitespace
                   "",
                   re.sub("slats?", ## replace slat/slats
                          "",
                          value.lower() ## Lower\
                            .replace("endlock","") ## Remove  "endlock" (as it's unnecessary
                            )
                   )
    if value not in itertools.chain.from_iterable(SLATALIASES): return False
    for index,basetype in enumerate(SLATALIASES):
        if value in basetype: break
    return list(SLATLOOKUP)[index]

## The original program used both a numerical index and the slat name
SLATINDEXCONVERSION = {
    1 : "3 5/8 INCH CROWN SLAT",
    2 : "2 7/8 INCH CROWN SLAT",
    3 : "2 1/2 INCH FLAT SLAT",
    4 : "MIDGET CROWN SLAT < 2 INCH >",
    5 : "SOLID SLATS AT BOTTOM OF ROLLING GRILLE",
    6 : "PERFORATED SLATS"
    }

SLATALIASES = [
    ["35/8inchcrown","crown","crn"],
    ["27/8inchcrown",],
    ["21/2inchflat","brd","ny","newyork"],
    ["midgetcrown<2inch>",],
    ["solidatbottomofrollinggrille",],
    ["perforated",],
    ]

SLATLOOKUP =collections.OrderedDict([
    ## <1>
    ("3 5/8 INCH CROWN SLAT",dict(slatheight = 3.625, increaseradius = .5, 
           GAGE={
               "20":dict(SG = "20", slatweight=.058514166),
               "22":dict(SG = "22", slatweight=float("5.78666E-02"))
               })),
    ## <2>
    ("2 7/8 INCH CROWN SLAT",dict(slatheight = 2.875, increaseradius = .6,
           GAGE={
               18:dict(SG = "18", slatweight=.071269154),
               20:dict(SG = "20", slatweight=float("5.485475E-02")),
               })),
    ##  <3>
    ("2 1/2 INCH FLAT SLAT",dict(slatheight = 2.625, increaseradius = .715,
           GAGE={
               18:dict(SG = "18", slatweight=.071269154),
               20:dict(SG = "20", slatweight=float("5.729167E-02"))
               })),
    ##  <4>
    ("MIDGET CROWN SLAT < 2 INCH >",dict(increaseradius = .438)),
    ## <5>
    ("SOLID SLATS AT BOTTOM OF ROLLING GRILLE",dict(RS=2.25,increaseradius=.815)),
    ## <6> 
    ("PERFORATED SLATS",dict(slatheight=2.5,increaseradius=.82,slatweight=.07388854,SG="22/22")),
    ])

## Gap Required between tandem castings
CASTINGGAP = 3.5

##    * All measurements are in inches
##    name: Readable name    type: Casting Type    springs: Number of springs the casting can accomodate    ods: list of spring ods that can be accomodated
##    castingod: OD of the casting    length: Extra length (outside) of the casting    innerloss: space consumed by the casting below each spring
##    innerloss example:
##        2 springs, innerloss 3, 10 inches of space for first/outer spring => The second spring has 3 inches less space (7 inches)
##        3 springs, innerloss 3, 10 inches of space for first/outermost spring => Second spring has 7 inches, Third spring (smallest) has 4 inches of space available 
CASTINGS = [
    dict(name = "Standard 4 Pipe", type = "pipe", springs = 2, ods = [3.75, 2.75], castingod = 3.75, length = 3, innerloss = 3),
    dict(name = "Standard 6 Pipe", type = "pipe", springs = 2, ods = [5.25, 3.75], castingod = 5.75, length = 6, innerloss = 6),
    dict(name = "Standard 4 Spring", type = "spring", springs = 1, ods = [3.75,], castingod = 3.75, length = 3, innerloss = 3),
    dict(name = "Standard 6 Spring", type = "spring", springs = 1, ods = [5.25,], castingod = 5.75, length = 6, innerloss = 3),
    dict(name = "Standard 2 Spring", type = "spring", springs = 1, ods = [2.75,], castingod = 2.75, length = 1, innerloss = 1),
    ]

CASTINGLOOKUP = {casting['name']:casting for casting in CASTINGS}

SPRINGOD = [None, 2.75, 3.75, 5.625, 7.5, 9.5, 11.5]

WIRELOOKUP = [
    ## wirediameter: WD, liftrate: LR, weightperinch:weightperinch, averagetensile:AT (guess)
    None ,
    dict(wirediameter= .1875  , liftrate=   11420 ,   weightperinch= .0078142 ,    averagetensile= 222500  , min_od = 2.75  ),
    dict(wirediameter= .25    , liftrate=   36093 ,   weightperinch= .0138916 ,    averagetensile= 212500  , min_od = 2.75  ),
    dict(wirediameter= .3125  , liftrate=   88119 ,   weightperinch= .0217083 ,    averagetensile= 202500  , min_od = 2.75  ),
    dict(wirediameter= .375   , liftrate=  182724 ,   weightperinch= .0312583 ,    averagetensile= 197500  , min_od = 3.75  ),
    dict(wirediameter= .40625 , liftrate=  251546 ,   weightperinch= .0366833 ,    averagetensile= 191000  , min_od = 3.75  ),
    dict(wirediameter= .4375  , liftrate=  338448 ,   weightperinch= .0425416 ,    averagetensile= 190000  , min_od = 3.75  ),
    dict(wirediameter= .46875 , liftrate=  445807 ,   weightperinch= .0488416 ,    averagetensile= 185000  , min_od = 3.75  ),
    dict(wirediameter= .5     , liftrate=  577500 ,   weightperinch= .0555666 ,    averagetensile= 180000  , min_od = 5.625 ),
    dict(wirediameter= .5625  , liftrate=  925044 ,   weightperinch= .070325  ,    averagetensile= 175000  , min_od = 5.625 ),
    dict(wirediameter= .625   , liftrate= 1409913 ,   weightperinch= .0868335 ,    averagetensile= 172500  , min_od = 5.625 )
    ]

for wire in WIRELOOKUP:
    if wire:
        ## min_id: Minimum Inner Diameter- the Inner Diameter of the spring when wound with the minimum outer diameter.
        wire["min_id"] = wire["min_od"] - 2 * wire['wirediameter']
        ## mp_base: MP before Cycle Adjustment (AT * WD^3 * 10.2)
        wire['mp_base'] = wire['averagetensile'] * wire['wirediameter']**3 / 10.2
del wire

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
WIREODINDEX = sorted([2.75, 3.75, 5.625])

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

## Adjustment to length of Hood to fit around clear opening
HOODEXTENSION = 4

def rounduptofraction(number,fraction):
    """ Rounds a number to a fraction """
    recipricol = 1/fraction
    return math.ceil(number * recipricol) / recipricol

