"""
FOREWARD
This file is an inbetween point; it seeks to translate the original Basic code just
enough to be readable as Python code without obscuring how the Python code relates
to the original. It is intended to be used as a jumping-off point and requires further
adjustments and refactoring to work properly; running this file as-is makes no garauntees.

The spring calculations section (Lines 8930-10640) was almost completely refactored due
to incompatibilities and poor code structure in.

NOTES
Basic variables are global, so we're using module-level containers to ensure consistency
Arrays start at index 1, so all containers default with array[0] = "" (or None). This
does not appear to be part of GW-Basic, but a convention of the code itself.
Quoted lines are irrelevant to execution (most often, because they are gui-related)
and are therefore unported.
Functions are named L{firstlinenumber}_{description}. I was being particularly verbose for
clarity's sake early on (as this file is intended to be an intermediary and not actually
used in production), but ended up going with shorter names later on.
## [Comments] at end of line is the original Line Number. All uncommented lines above
the line were originally part of that line.
Some parts of logic statements were rewritten for clarity (i.e., parentheses were added
and "X = 1 OR X = 2" structures were changed to "X in [1,2]".

Also, the longer I worked on this, the more often I commentted on the code and the less
serious those comment became.

Example of Translation:
60 CLS:IF X = 1 AND Y = 2 OR X = 1 AND Z = 4 THEN PRINT HELLO WORLD:KEY OFF
Was converted to:
"CLS"
if X = 1 and (Y = 2 or Z = 4):
    print("HELLO WORLD")
    "KEY OFF" ## 60
"""

import math

VARIABLES = dict(
    A = 0, ## Calculation Holder? A = INT(Q1) (L7390)
    ADDSH = "", ## Add Stop Height (Query) (L3590)
    AJ = 0, ## Pipe Adjuster size (4, default 6) (L8220)
    AJF = 0, ## Pipe Adjuster Fraction?; for use in equations (L8460)
    ANS = "", ## Answer? Used to hold input (L3070)
    AS = 0, ## Astragal Weight per Foot (L6650)
    AT = 0, ## Average Tensile; Wire Property (L10550)
    AW = 0, ## Angle Weight (per Foot) (L3510)
    B1 = 0.0, ## Part of BT Calculations, Equals BT/2 (L10450)
    B2 = 0.0, ## Part of BT Calculations, integer portion of B1 (L10450)
    B3 = 0.0, ## Part of BT Calculations, the float portion of B1 (L10450)
    BB = "", ## Bottom Bar Weight
    BB_S = "", ## Bottom Bar Type
    BBH = 0, ## Bottom Bar Height? (L3270)
    BJT = 0, ## ??? atm (L1790)
    BL = ["" for x in range(10)], ## Barrel (Ring) List (L11450)
    BL_S = ["" for x in range(10)], ## Barrel (Ring) List as string (L11450)
    BLL = ["" for x in range(10)], ## Barrel (Ring) Location List? (L11480)
    BO = 0, ## Bottom (Bar) Option (L3200)
    BP = 0, ## Bracket Plate Height? (L5530)
    BRC = 0, ## Barrel Ring Centers (L11480)
    BRL = "", ## Barrel Ring List (L11490)
    BRLL = "", ## Barrel Ring Location List (L11490)
    BS1 = 0.0, ## Barrel (Ring) Spacing, fist calculation (L11370)
    BS2 = 0.0, ## Barrel (Ring) Spacing, second calculation (L11370)
    BS3 = 0.0, ## Barrel (Ring) Spacing, third calculation (L11370)
    BS4 = 0.0, ## Barrel (Ring) Spacing, fourth calculation (L11370)
    BSL = 0, ## Bottom Slat Length??? (L6790)
    BST = None, ## Bottom Slat Type (L2340)
    BT = 0, ## Build Type? 0: Single Spring, 1-10 Outer/Inner Spring; 11: Tandem Springs; 12/13 Final Outer/Inner (Iterate: 10450; Build Types: 9760)
    C = 0, ## Denominator when parsing fractions (L1650); Value Holder? Q^2-4*J*Y (L7340)
    C_S = "", ## Customer
    CGR = "", ## ??? atm, appears to literally only be set on one line and not used anywhere else (L5200)
    CIE = "N", ## Cast Iron Endlocks (Y/N) (L6120)
    CN = 0, ## ??? atm, Equals LR/(MD * 3.1416) (L9610)
    CT = 0, ## Springs Total Inch/Poound
    CW = None, ## Curtain Width ???
    CY = None, ## Spring Cycles ???
    D = 0, ## Numerator when parsing fractions (L1650)
    D3 = 0, ## Wire Diameter Cubed (L9610)
    DC = 0, ## Decimal (used for parsing Mixed fractions) (L1660)
    DD = 0, ## A Temporary Container used to convert Floats to Measurement Strings of form '{Feet} ft.-{Inches}{Fraction}"' (L11260)
    DEN = 0, ## A Temporary Container for the Denominator for use in converting Floats to Measurment Strings (DD) (L11270)
    DM = None, ## Door Model
    DT = None, ## Door Type
    E1 = 0.0, ## Outer Spring Stretch
    E2 = 0.0, ## Inner Spring Stretch
    EAGL = 0.0, ## Alum. Grille Guide (L10680) 
    ED = "", ## String representation of DD in form '{Feet} ft.-{Inches}{Fraction}"'  (L11310)
    EF = 0, ## End Feet, The final Footage Value temporarily stored when Converting DD to ED (L11260)
    EG = "N", ## Extruded Guides (L1800)
    EI = 0, ## End Inches, The final Inces Value temporarily stored when Converting DD to ED (L11260)
    EL = None, ## ??? atm, (L2750)
    F1 = 0, ## Outer Spring Weight 
    F2 = 0, ## Inner Spring Weight
    F3 = 0, ## Total Spring Weight
    FAL = "", ## Front Angle, Copy of MAL? (L10670)
    FBR = 0, ## First Barrel Ring?, Equals BS4/2 (L11480)
    FDD = 0, ## Float/Decimal Component of DD temporarily stored during the conversion of DD to ED (L11260)
    FF = 0, ## Opening Input feet? (L1430-1440)
    FI = 0, ## Opening Input inches? (L1430-1440)
    FL = 0, ## Final Lever Arm
    FPFE = 0, ## First Preforated (slat) From End? [output: PREFORATED SLATS: NPS @FPFE] (L6820)
    FPSFB = 0, ## First Preforated Slat From Bottom (L6810)
    FSH = 0.0, ## First Slot Hole? (Connection to Barrel Rings), Equals truncate( (SL-PL+BS4)/2 ,10000) (L11410)
    FT = "", ## First Tube (Rolling Grille) (L8310)
    GD = "", ## Part of Guide Type with PO and MA (L5040)
    GF = None, ## Grille Finish (L2190)
    GON = None, ## Gage Option Number (L2690)
    GP = None, ## Vision Section GRILLE PATTERN (L2130)
    GR = 0.0, ## Gap (between brackets)?  (Set L6030, L5040,Output:5400,8640)
    GS = None, ## Grille Size (L6500)
    GW = 0, ## Grille Weight, Equals int(NR*RL*RW*100)/100
    HC = 0, ## Height (Pipe) Center line [output: CENTER LINE OF PIPE: HC] (L5600)
    HD = "", ## Hand atm (L11510)
    HF = 0, ## Stop Height Feet
    HI = 0, ## Stop Height Inches
    HL = list(), ## (Slat) Hole List (Connect to Barrel Rings) (L11450)
    HLL = ["" for x in range(10)], ## (Slat) Hole Location List? (Connect to Barrel Rings) (L11480)
    HS = None, ## Height Slat ??? (L2430, L6250)
    HXP = 0.0, ## Heat Expansion (Gap) (L6040)
    HW = 0, ## Hanging Weight Down (L6760)
    IDD = 0, ## Integer Component of DD temporarily stored during the conversion of DD to ED(L11260)
    I4 = 0.0, ## ???, Based on Pipe (L7020)
    IL = 0, ## Initial Lever Arm, based on Pipe-Size (L7300)
    IN = None, ## Integer Holder for HI when < 2 digits (L1610)
    IP = 0.0, ## Inch/Pounds per Turn, Equals (TD-TU)/TR (L8200), or TD/TT (L8370)
    IR = None, ## Increase (Wrap) Radius, Based on Slat Type, essentially the depth of the slat (which increases the circumference of the wrap on each turn) (L250)
    IS = None, ## Inner Shaft (L8470)
    IT = None, ## Item? (L1960)
    JN = "", ## Job Number 
    L1 = 0.0, ## Outer Spring length
    L2 = 0.0, ## Inner Spring length
    LC = 0.0, ## Spring Length Calculation Holder, Equals NC*WD (L9720,L8490)
    LI = 0, ## ??? atm, Equals LR/SVariable (ST,SX,SY,SZ) (L9720)
    LL = 0, ## ??? atm, Equals truncate(R1-N2*LC,10000) (L8530,L8610)
    LR = 0, ## Lift Rate?, Wire Attribute (L10550)
    LTBB = 0, ## Large Tubular Bottom Bar (L3560,L3140)
    LW = 0, ## ??? atm (L9740)
    M = 0.0, ## Maximum Deflection Weight, Equals I4/WO**2*float(38667) (L6280)
    MA = 0.0, ## Part of Guide Type with GD and PO
    MAL = 0.0, ## Middle Angle, Equals SH - .125 when no US (L10670)
    MD = 0, ## Original Mean Diameter, equals OD - WD (L9610)
    MF = "", ## Manufacture ???
    MK = "", ## Mark
    MP = 0, ## ??? atm, Equals SR*D3/10.2 (L9720)
    MT = None, ## Max Turns Calculation holder, Equals MP/TQ (L9740)
    MT1 = 0, ## Outer Spring Max Turns
    MT2 = 0, ## Inner Spring Max Turns
    MT_S = "", ## ??? atm
    MW = 0.0, ## Equals HW + PW (L7160)
    N1 = 0.0, ## ??? atm, Equals truncate(R1/LC,10000) (L8610)
    N2 = 0, ## ??? atm, Equals truncate(N1,1) (L8610)
    NBR = 0, ## Number of Barrel Rings, equals NBS+1 (L11410)
    NBS = 0, ## Number of Bottom Slats, Equals (SBH-BBH-1.5)/HS (L6270)
    NC = 0.0, ## ??? atm, Equals LI/(MD*{Pi}) (L9720)
    NOEL = "N", ## No Endlocks (Y/N) (L6090)
    NPS = 0, ## Number Preforated Slats, Equal to PSH/HS (L6810)
    NPPS = 0, ## Number Perferations Per Slat?, equalt to CW/8.5-2 (L6810)
    NR = 0, ## Number Rods (Rolling Grille), Equals ((SH+US-SBS-BBH)/RS)+1 (L6400,L8650)
    NS = 0, ## Slats to Center line, Equals (HC-BBH-1.5-(NR-1)*RS)/HS (L6430)
    NT = 0, ## ??? atm; Equals N2 - 1 (L8530)
    NTS = 0, ## Number of Top Slats, Equals TNS - NBS (L6790,L8460)
    NUM = 0, ## A Temporary Container for the Numerator for use in converting Floats to Measurment Strings (DD) (L11270)
    O = 0, ## Spring OD Iterator (L8930)
    O1 = 0, ## Outer Spring O.D.
    O2 = 0, ## Inner Spring O.D.
    OD = None, ### Spring O.D. Calculation Holder (Settable Constant) (L9750)
    OGS = "", ## Open Grill Section (L2130)
    OP = None, ## OPeration Method (i.e.- Motor) (L810)
    OVR2 = "", ## Override 2? (L2530)
    P = None, ## Pipe Index (L8470)
    P_S = "", ## String version of Pipe (L7170)
    PD = "", ## Pass Door in form "[2/3][L/R]" (2/3 = Width, L/R = Side) (L4640)
    PF = 0.0, ## ??? atm, Equals 1.25+2*FT+NT*LC (L8590)
    PJ = "", ## Project (Type?)
    PL = 0.0, ## ??? atm, Equals GR-5.5 (L5040)
    PO = "", ## Part of Guide Type with GD and MA (L5620)
    PR = None, ## (No) Pipe Rings: PR = 1 == No Pipe Rings :-/ (L4450)
    PRD = "", ## Panic Release Device (y/n) (L4050)
    PSH = None, ## Perforated Slat Height; This is the combined height of all Perferated Slats, i.e.- 5 Perferated 2-7/8 Flat Slats = 14.375 PSH (L2390)
    PSCL = None, ## Perforated Slat Center Line (L2410)
    PSWL = 0, ## Perferated Slats Weight Loss,Equal to (((( SW / 5.25 ) * 4.648175 ) * NPPS ) * NPS) (L6800)
    PT = 0, ## Pre-Turns, Equals TU/IP(L8210) or TT - TR (L8370)
    PW = 0, ## Pipe Weight, Equals WT * WO (L4250)
    Q = 0, ## Q is used as an integer holder for HI (L1610), as Query holder (L3570, L1460)
    Q1 = 0, ## Turns to Raise? ( -Q + sqrt(c) ) / (2*J) (L7340)
    R1 = 0.0, ## ??? atm, Some kind of container, probably (L8520)
    RC = 0, ## Spring Selection variable (L8870)
    RL = 0.0, ## Rod Length (Rolling Grille) (L6030)
    RS = None, ## ??? atm (L6400)
    RW = 0.0, ## Rod Weight (L6390)
    S1 = 0.0, ## Outer Spring Rate Inch/Pound
    S2 = 0.0, ## Inner Spring Rate Inch/Pound
    SBH = None, ## Solid Bottom Height (L2330)
    SBS = 0.0, ## Size of Bottom Slats? Distance from bottom to Grille, Equals NBS*HS+BBH+1.5
    SD1 = 0.0, ## Bottom Bar Slope (L6360)
    SD2 = 0.0, ## Equals SD1 (Bottom Bar Slope) + 3 (L6630)
    SE = 0, ## Safety Edge Weight per Foot
    SEBB = "", ## Safety Edge on Bottom Bar
    SG = "", ## Slat Gage (L2710)
    SGO = "", ## Slat Gage Option (L2760)
    SH = 0, ## Stop Height (Converted to Inches after input), Input Variable is HF (L1580)
    SL = 0.0, ## Slat Length (L5040)
    SM = "", ## Standard Manufacture (L1860)
    SP1 = 0.0, ## Equals SD2 * (SL + 1) (L6630)
    SP2 = 0.0, ## Equals SD1 * ( (SL + 1) / 2 ) (L6630)
    SP3 = 0.0, ## Equals ( (SP1 - SP2) / 144 ) * 5 (L6630)
    SPW = 0.0, ## Equals SP3  +  ((SL + 1) * .05316) (L6630)
    SR = 0, ## Spring Rating??? atm, = AT * TP (9610)
    SS = 0.0, ## Feeder Slat Weight equals SL * SW * .65
    ST = 0, ## Tandem Spring Variable?, Equals IP/2 (L10500)
    ST_S = "", ## Slat Type, Set based on TS (L4780, L6490)
    STS = "", ## ??? atm (L8770)
    SURE = "", ## Override 2 Double Check... :-/ (L2540)
    SV = 0, ## Inner Spring Variable, Equals IP-S1 (10540)
    SW = 0.0, ## Slat Weight per Inch (L2750)
    SX = 0, ## Outer Spring Variable?, Equals MP/TT (L10520)
    SXT = None, ## Number of 1/16 derived from float remainder of DD during its conversion to ED(L11260)
    SY = 0, ## Outer Spring Variable?, Equals IP*.55 (L10510)
    SZ = 0, ## Inner Spring Variable? Equals IP - S1 (L9660)
    TB = 0.0, ## Bracket Plate Width? (L8640,L6160)
    TB_S = "", ## ??? atm (L6130)
    TD = 0.0, ## Torque (required) Down, Equals IL*HW (L8180)
    TBBT = "", ## Tubular Bottom Bar Type? (L3550)
    TL = 0.0, ## STD Tubes? (Rolling Grille) (L8490)
    TNL = 0.0, ## Total Links (L8660), Equals TNT/2+(NR-1)*3 (L8590)
    TNS = 0, ## Total Number of Slats, Equals math.ceil:(2*3.1416*IL*(.6600001-AJF)/HS)+NS (L8460)
    TNT = 0, ## ??? atm, Equals TST + (NR-2)*2 (L8570)
    TP = 0.0, ## Torque Percentage; cycle adjustment (L8890)
    TQ = 0.0, ## Torque (Inch/Pound Rate) Calculation Holder atm, Equals CN/NC (L9730)
    TR = 0.0, ## Turns to Raise (L8200)
    TS = 0, ## Type Slats. Index of Slat Type.
    TSH = "", ## Top Slat Holes (Conection to Barrel Rings) (L11500)
    TSHH = "", ## Top Slat Holes (locations) (Connection to Barrel Rings) (L11500)
    TST = 0, ## STD Tubes? (Rolling Grille), Equals (NR-2)*NT
    TT = "", ## Total Turns, String representation of TR + PT (L8230)
    TU = 0.0, ## Torgue (required) Up, Equals FL*WU (L8200)
    U = 0, ## Upset (L3110)
    US = 0, ## U (Upset) as numeric (L5580)
    UTC = "", ## ??? atm (L6360)
    VCL = None, ## Vertical Center Line? (L2130)
    W = 0, ## ??? Iterator (L9080)
    W1 = 0, ## Outer Spring Wire Gage?
    W2 = 0, ## Inner Spring Wire Gage?
    WAL = 0.0, ## Wall Angle, Equals SH + US + BP - HXP (L10700)
    WAT = "", ## Wall Angle Thick (L6130)
    WD = 0, ## Wire (Gage/)Diameter Calculation Holder (Settable Constant) (L9720)
    WL = 0, ## Windlocks (Slats/Windlock) (L4860)
    WL_S = "", ## String version of WL (L4860)
    WO = 0.0, ## Width Opening??? in Feet, Equals CW/12 (L7130)
    WR = 0, ## WRap slats, Equals ceil( (2*{Pi}*IL(.75-AJF)+HC-ceil(NS+1)*HS)/HS )(L11200)
    WS = 0.0, ## Weight Spring Calculation Holder, Equals LI*LW (L9740)
    WT = 0.0, ## Based on Pipe size (L7130)
    WU = 0, ## Hanging Weight up (L8110)
    X = "", ## Temporary container used in parsing fractions (L1650), also for iterating L11550
    X1 = 0, ## Integer Container for parsing floats (L8210)
    X2 = 0.0, ## Decimal Container for parsing floats (L8210)
    X3 = 0.0, ## Rounding Container for parsing string (FT) (L8310)
    Y = "", ## Temporary container used in parsing fractions (L1650)
    Z = "", ## Temporary container used in parsing fractions (L1650)
    )

WIRELOOKUP = [
    None,
    dict(WD=.1875,  LR=11420,   LW=.0078142,    AT=222500),
    dict(WD=.25,    LR=36093,   LW=.0138916,    AT=212500),
    dict(WD=.3125,  LR=88119,   LW=.0217083,    AT=202500),
    dict(WD=.375,   LR=182724,  LW=.0312583,    AT=197500),
    dict(WD=.40625, LR=251546,  LW=.0366833,    AT=191000),
    dict(WD=.4375,  LR=338448,  LW=.0425416,    AT=190000),
    dict(WD=.46875, LR=445807,  LW=.0488416,    AT=185000),
    dict(WD=.5,     LR=577500,  LW=.0555666,    AT=180000),
    dict(WD=.5625,  LR=925044,  LW=.070325,     AT=175000),
    dict(WD=.625,   LR=1409913, LW=.0868335,    AT=172500)
    ]

SPRINGOD = [None, 2.75, 3.75, 5.625, 7.5, 9.5, 11.5]

PIPES = [
    None,
    A[41], ## 41: '4 INCH TUBE'
    A[42], ## 42: '4 INCH PIPE'
    A[43], ## 43: '6 INCH TUBE'
    A[44], ## 44: '6 INCH PIPE'
    A[45], ## 45: '8 INCH PIPE'
    A[46], ## 46: '10 INCH PIPE'
    A[47], ## 47: '12 INCH PIPE'
    A[48], ## 48: '14 INCH <30> PIPE'
    A[49], ## 49: '14 INCH <40> PIPE'
    A[50], ## 50: '16 INCH <30> PIPE'
    A[51], ## 51: '16 INCH <40> PIPE'
    ]

## If no Pipe rings, 4 inch Pipe IL = 2.25 and 6 Inch Pipe IL = 3.3125
PIPELOOKUP = {
     ## 41: '4 INCH TUBE'
    A[41]: dict(IL=4.25,    IS = "1 1/4",   I4 = 5.86,  WT = 8.56*2.5),
     ## 42: '4 INCH PIPE'
    A[42]: dict(IL=4.25,    IS = "1 1/4",   I4 = 7.23,  WT = 10.79*2),
    ## 43: '6 INCH TUBE'
    A[43]: dict(IL=4.25,    IS = "1 1/2",   I4 = 19.71,  WT =12.93*2.93),
    ## 44: '6 INCH PIPE'
    A[44]: dict(IL=4.25,    IS = "1 1/2",   I4 = 28.1,  WT = 18.97*1.75), 
    ## 45: '8 INCH PIPE'
    A[45]: dict(IL=4.3125,  IS = "1 3/4",   I4 = 72.5,  WT = 28.55*1.7), 
    ## 46: '10 INCH PIPE'
    A[46]: dict(IL=5.375,   IS = "2",       I4 = 161,  WT = 40.48*1.7), 
    ## 47: '12 INCH PIPE'
    A[47]: dict(IL=6.375,   IS = "2 1/2",   I4 = 279,  WT = 49.56*2), 
    ## 48: '14 INCH <30> PIPE'
    A[48]: dict(IL=7,       IS = "3",       I4 = 372,  WT = 54.57+50), 
    ## 49: '14 INCH <40> PIPE'
    A[49]: dict(IL=7,       IS = "3",       I4 = 428,  WT = 63.37+50), 
    ## 50: '16 INCH <30> PIPE'
    A[50]: dict(IL=8,       IS = "3",       I4 = 561,  WT = 62.58+55), 
    ## 51: '16 INCH <40> PIPE'
    A[51]: dict(IL=8,       IS = "3",       I4 = 730,  WT = 82.77+55), 
    }

SLATLOOKUP ={
    ## <1> 3 5/8 INCH CROWN SLAT
    1:dict(HS = 3.625, IR = .5, 
           GAGE={
               "20":dict(SG = "20", SW=.058514166),
               "22":dict(SG = "22", SW=float("5.78666E-02"))
               }),
    ## <2> 2 7/8 INCH CROWN SLAT
    2:dict(HS = 2.875, IR = .695,
           GAGE={
               "18":dict(SG = "18", SW=.071269154),
               "20":dict(SG = "20", SW=float("5.485475E-02")),
               }),
    ##  <3> 2 1/2 INCH FLAT SLAT
    3:dict(HS = 2.625, IR = .715,
           GAGE={
               "18":dict(SG = "18", SW=.071269154),
               "20":dict(SG = "20", SW=float("5.729167E-02"))
               }),
    ##  <4> MIDGET CROWN SLAT < 2 INCH >
    4:dict(IR = .438),
    ## <5> SOLID SLATS AT BOTTOM OF ROLLING GRILLE
    5:dict(RS=2.25,IR=.815),
    ## <6> PERFORATED SLATS
    6:dict(HS=2.5,IR=.82,SW=.07388854,SG_S="22/22"),
    }

VARIABLES ['TS$'] = None ## Type Slats? (L2000 )
A = list()

def truncate(_float,precision = 100):
    """ Truncates a float or rounds to a fraction.
    
    precision sets the number of decimal places to truncate to: precision>=1
    will truncate the float, 0<precision<1 will round to the given precision.
    Default precision is 100.

    This code is repeated in several places, so I'm taking the liberty to
    spin it off into its own function as-written to improve readability;
    whether it should be replaced with round(n,2) or float(f"{n:.2f}")
    (or even removed altogether) is another matter.
    """
    return int(_float*precision)/precision

def format_float_as_measurment(key):
    """ Converts a float as a measurement in form Feet ft.- Inches-Num/Den"

    This code is repeated in several places, so I'm separating it into its own
    function as-written: obviously this should be reworked significantly
    """
    VARIABLES['DD']=VARIABLES[key]
    L11260_format_float_as_measurement()
    VARIABLES[key]=VARIABLES['ED']

def L0_startup():
    """ The beginning of the program """
    ## Clear Screen
    "CLS"
    ## Disable Function Keys
    "KEY OFF" ## 60
    ## Clear Function Keybar
    "CLEAR" ## 70
    L90_testclock()

def L90_testclock():
    """ Test Clock Routine. DELETE ME """
    "START!=TIMER:For X = 1 To 37750.0! : Next : FINISH! = TIMER" ## 90
    "SPEED!=FINISH!-START!:DELAY=25000000*SPEED!"
    return L130_assignmeasurementvariables() ## 100

def L110_rundelay():
    """ Runs the delay. DELETE ME? """
    "FOR T=1 TO DELAY:NEXT T"
    return None ## 110

def L130_assignmeasurementvariables():
    """ Adds measurement variables to the scope. """
    VARIABLES['I']='"'
    VARIABLES['DV']="/"
    VARIABLES['IP_S']='"/#'
    return L250_clearscreen() ## 130

def L150_yellowonblacktext():
    """ Sets fg to yellow, bg to black. Standard Font. """
    "COLOR 14,0"
    return L240_insertnewline() ## I have no idea why... ##150

def L160_whiteonbluetext():
    """ Sets fg to white, bg to blue. Confirmation Font. """
    "COLOR 15,1"
    return ## 160

def L170_brightwhiteonredtext():
    """ Sets fg to "bright" white, bg to red. Error Font. """
    "COLOR 15,4"
    return ## 170

def L180_yellowonred():
        """ Set fg to Yellow, bg to Red """
        "COLOR 14,4"
        return ## 180

def L190_blackongreentext():
    """ Sets fg to Black, bg to Green. Default Value Alert. """
    "COLOR 0,2"
    return ## 190

def L200_blueonwhitetext():
        "Sets fg to blue, bg to white"
        "COLOR 1,15"
        return ## 200

def L220_brightwhiteongreentext():
    """ Sets fg to "bright" white, bg to green """
    "COLOR 15,2"
    return ## 220

def L230_redonwhitetext():
    """ Sets fg to Red, bg to White. Alert Font. """
    "COLOR 4,7"
    return ## 230

def L240_insertnewline():
    """... Inserts a newline (80 is width of a line). """
    'PRINT"" TAB(80)" "'
    return ## 240

def L250_clearscreen_and_gotoprogram():
    """ Clear Screen and then go to the core program. GUI DELETE ME """
    "CLS"
    return L300_Avars_and_gotoprogram #250

def L290_L110_rundelay_and_L590_loadvars_and_main_menu():
    """ An intermediary function """
    ## L110 is flagged for deletion
    L110_rundelay()
    ## Next execution was originally RESTORE
    ## 590 originally READ the DATA, but that isn't necessary anymore
    return L590_loadvars_and_mainmenu() ## 290

def L300_Avars_and_590_loadvars_and_mainmenu():
    """Both sets up the DATA variables stored in A and begins running the program """
    ## Note: Basic counts 1:inclusive-end (90 in this case)
    A.clear()
    vars = {1: '<1>  CURTAIN TYPE', 2: '<2>  GAGE', 3: '<3>  ASTRAGAL', 4: '<4>  SAFETY EDGE',
            5: '<5>  BOTTOM BAR', 6: '<6>  UPSET', 7: '<7>  WINDLOCKS', 8: '<8>  SPRINGS', 9: '<9>  ENDLOCKS',
            10: '<10> SLOPE', 11: '<11> PIPE & RINGS', 12: '<12> ADJUSTER', 13: '<13> BRACKET PLATE', 14: 'PASS DOOR',
            15: '<15> NO OTHER OPTIONS', 16: 'ALUMINUM T TYPE (BBX-C)', 17: '1 1/2" x 1 1/2" x 1/8" (STL)', 18: '2 1/2" x 2" x 3/16" (STL)', 19: '3" x 2" x 3/16" (STEEL)',
            20: '2" x 2" x 1/8" (ALUM.)', 21: '<1> 25000', 22: '<2> 50000', 23: '<3> 100000', 24: '<4> MAXIMUM POSSIBLE CYCLES',
            25: '<1> CONT. STAMPED STEEL', 26: '<2> ALT. CAST IRON', 27: '<3> CONTINUOUS CAST IRON', 28: '<1> INSIDE ADJUSTER', 29: '<2> THRU-SHAFT',
            30: '<1> 3 5/8 INCH CROWN SLAT', 31: '<2> 2 7/8 INCH CROWN SLAT', 32: '<3> 2 1/2 INCH FLAT SLAT', 33: 'INSULATED DOUBLE SLAT <2 3/4>', 34: '<1> SMALLEST POSSIBLE BRACKETS', 
            35: '<2> LARGER THAN STD. BRACKETS', 36: '<1> 22 GAGE', 37: '<2> 20 GAGE', 38: '<3> 18 GAGE', 39: '<4> 16 GAGE',
            40: 'SLATS', 41: '4 INCH TUBE', 42: '4 INCH PIPE', 43: '6 INCH TUBE', 44: '6 INCH PIPE',
            45: '8 INCH PIPE', 46: '10 INCH PIPE', 47: '12 INCH PIPE', 48: '14 INCH <30> PIPE', 49: '14 INCH <40> PIPE',
            50: '16 INCH <30> PIPE', 51: '16 INCH <40> PIPE', 52: '<5> ALUMINUM GRILLE', 53: 'SERVICE DOOR', 54: 'WEATHERTITE DOOR',
            55: 'FIRE DOOR', 56: 'ROLLING GRILLE', 57: 'COUNTER SHUTTER', 58: 'FIRE SHUTTER', 59: 'INSULATED DOOR',
            60: 'FACE MOUNTED', 61: 'EXTERIOR MOUNTED', 62: 'BETWEEN JAMBS', 63: 'CHAIN OPERATED', 64: 'MOTOR OPERATED',
            65: 'HAND LIFT', 66: 'CRANK OPERATED', 67: 'GALV. STEEL', 68: 'PRIME PAINTED', 69: 'MILL ALUMINUM',
            70: 'ALUM. LINKS/PLASTIC TUBES', 71: 'ANODIZED ALUMINUM', 72: 'DURANODIC ALUMINUM', 73: 'STAINLESS STEEL', 74: '<4> MIDGET CROWN SLAT < 2 INCH >',
            75: 'EXTERIOR THRU-WALL', 76: '<7> VISION SECTION <GRILLE>', 77: 'RETURN TO MAIN MENU', 78: 'MOTOR (BY OTHERS)', 79: 'PERFORATED SLATS',
            80: '!!!!!!!!!! PARAMETER OVERIDE !!!!!!!!!!', 81: 'STANDARD TUBULAR ALUMINUM', 82: 'LARGE TUBULAR ALUMINUM', 83: '2" x 2" x 1/8" STEEL', 84: 'STIFFENER',
            85: 'OVERSIZE', 86: '3" x 2" x 3/16" ALUMINUM', 87: '2 1/2" x 2 1/2" x 1/8" (ALUM.)', 88: 'ELECTRIC (Miller Edge)', 89: 'PNEAUMATIC (Air)',
            90: 'LEXAN INSERTS'}
    ## The Above represents lines 300-560
    ## Theoretically, this line happens at the beginning of 590, but can't happen in the python
    A.update(vars) ## 590
    ## This line is implicit in the original code
    return L590_loadvars_and_mainmenu()

def L590_loadvars_and_mainmenu():
    """ In the original version, converting DATA to A$(x) was part of this routine """
    ## Theortically, the last line of 300_Avars_and_590_loadvars_and_mainmenu happens on this line (590)
    if VARIABLES["SM"]=="N":
        return L1910_print_nonstandardselection_menu() ##600 
    
    ## TODO (after done 1910 branch)
    #GOSUB 160:CLS : SCREEN 0: LOCATE 10, 1 (610)
    #PRINT TAB(12)"ENGINEERING & SPRING BALANCE FOR ROLL-UP DOORS & GRILLES" (620)
    #PRINT:PRINT TAB(13)"Written by Alan Hall using Microsoft GWBasic Ver. 3.20" (640)
    #PRINT TAB(28)"Copyright 1985 - 2003" (650)
    #LOCATE 24,1,0:GOSUB 110:COLOR 15, 0: CLS : LOCATE 4, 1 (660)
    #GOSUB 160:PRINT TAB(17)"ENGINEERING & SPRING BALANCE FOR ROLL-UP DOORS"TAB(79)"" (670)
    #KEY 1,"":KEY 2, "": KEY 3, "": KEY 4, "": KEY 6, "": KEY 7, "": KEY 8, "": KEY 9, "" (680)
    #KEY 2,"GOTO 70"+CHR$(13):KEY(2) On (690)
    #KEY 10,"SYSTEM"+CHR$(13):KEY(10) On (700)
    #LOCATE 25,1:PRINT" <F2>=RE-START"TAB(21)"<Ctrl + C>= STOP"TAB(42)"<F5>=CONTINUE"TAB(60)"<F10>=EXIT TO MENU " (710)
    #LOCATE 24,1:GOSUB 150 (720)
    #LOCATE 3,1:INPUT"NAME:";NM$: PRINT (730)
    #INPUT"JOB NUMBER ";JN$:PRINT : If LEN(JN$) = 5 Then GoTo 760 (740)

def L1910_print_nonstandardselection_menu():
    """ Select Non-Standard SM """
    "CLS"
    L160_whiteonbluetext()
    print(" ******** SELECT NON-STANDARD OPTION ******** ")
    "LOCATE 1, 63"
    print()
    L150_yellowonblack() ## 1910
    "LOCATE 3,8"
    L190_blackongreentext()
    print(" (Starting with Lowest Number First, Select Options Sequentially) ")
    L150_yellowonblacktext()
    "LOCATE 3, 76"
    print()
    print() ## 1920
    print()
    print("A[1]     A[8]")
    print("A[2]     A[9]")
    print("A[3]     A[10]")
    print("A[4]     A[11]") ## 1930
    ## "<1> CURTAIN TYPE    <8> SPRINGS
    ##  <2> GAGE            <9> ENDLOCKS
    ##  <3> ASTRAGAL        <10> SLOPE
    ##  <4> SAFETY EDGE     <11> PIPE & RINGS"
    "LOCATE 8,1"
    print("A[2]    A[9]")
    print("A[3]    A[10]")
    print("A[4]    A[11]") ## 1940
    ## "<2> GAGE        <9> ENDLOCKS
    ##  <3> ASTRAGAL    <10> SLOPE
    ##  <4> SAFETY EDGE <11> PIPE & RINGS"
    print("A[5]    A[12]")
    print("A[6]    A[13]")
    print("A[7]    <14> A[14]")
    ## "<5> BOTTOM BAR  <12> ADJUSTER
    ##  <6>  UPSET      <13> BRACKET PLATE
    ##  <7>  WINDLOCKS  <14> PASS DOOR
    "LOCATE 13, 52"
    L230_redonwhitetext()
    print(" A[15] ")
    ## " <15> NO OTHER OPTIONS "
    L150_yellowonblack() ## 1950
    return L1960_ask_nonstandard_item()

def L1960_ask_nonstandard_item():
    """Asks for input on NonStandard item (L1910 displays Menu) """
    VARIABLES['IT'] = input("ENTER NON-STANDARD ITEM NUMBER ") ## 1960
    ## Note, Basic arrays start at index 1
    onits = [None,L2000_curtainoptions,L2670_nonstandard_gage,L3000_add_astragal,L3010_add_safety_edge,3140,3740,3840,3980,4070,4220,4350,4490,4550,4620,4750]
    if VARIABLES['IT'] in onits:
        return onits[VARIABLES['IT']] ## 1970
    "BEEP"
    return L1960_ask_nonstandard_item() ## 1980

def L1990_beep_and_L110_rundelay_and_L2000_curtainoptions():
    """ Beeps the machine, runs delay, and then implicitely runs curtain options"""
    "BEEP"
    L110_rundelay() ## 1990
    return L2000_curtianoptions() ## This line is implicit

def L2000_curtainoptions():
    """ Screen for Selecting Curtain Options """
    "CLS"
    print()
    L160_whiteonbluetext()
    print(" *********** SELECT CURTAIN OPTION *********** ")
    L150_yellowonblacktext() ## 2000
    print("A$(30)")
    print()
    print("A$(31)")
    print()
    print("A$(32)")
    print()
    print("A$(74)")
    print() ## 2010
    ## "<1> 3 5/8 INCH CROWN SLAT
    ##
    ##  <2> 2 7/8 INCH CROWN SLAT
    ##
    ##  <3> 2 1/2 INCH FLAT SLAT
    ##
    ##  <4> MIDGET CROWN SLAT < 2 INCH >
    ## "
    print("<5> SOLID SLATS AT BOTTOM OF A$(56)")
    print()
    print("<6> A$(79)")
    print() ## 2020
    ## "<5> SOLID SLATS AT BOTTOM OF ROLLING GRILLE
    ##
    ##  <6> PERFORATED SLATS
    ## "
    print("A$(76)")
    print()
    print("(8) A$(77)")
    print()
    print() ## 2030
    ## "<7> VISION SECTION <GRILLE>
    ##
    ## (8) RETURN TO MAIN MENU
    ##
    
    ## NOTE!!! There is both a TS and TS$ Variable!!!!
    ## I dunno why...
    VARIABLES['TS$'] = input("ENTER OPTION NUMBER ")
    print() ## 2040
    ## Note: this line was originally "VAL(TS$)=>9..."; according to the docs
    ## => is not a valid operator and I could find no such operator otherwise,
    ## so I rewrote it.
    if int(VARIABLES['TS$'])>=9 or int(VARIABLES['TS$'])==0:
        "BEEP"
        return L2000_curtainoptions ## 2050

    ## If Main Menu and DT != FIRE DOOR
    if VARIABLES['TS$']=="8" and VARIABLES['DT']!=A[55]:
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu()
    else: 
        return L2070_more_curtainoptions() ## 2060

def L2070_more_curtainoptions():
    """ Handle the rest of the Curtain Options """
    ## If DT != FIRE DOOR
    if VARIABLES['DT']!=A[55]:
        return L2090_more_more_curtainoptions() ## 2070
    ## Note, the original logic did not use parens; I made an educated guess on the implicit execution
    ## and reworked it.
    if VARIABLES['DT']==A[55] and VARIABLES['TS$'] in ["1","2"]:
        return L2430_validate_and_record_slat_stats()
    else:
        print()
        L170_brightwhiteonredtext()
        print(" ONLY # 1  or  # 2 ALLOWED FOR A DT$")
        L150_yellowonblacktext()
        return L1990_beep_and_L110_rundelay_and_L2000_curtainoptions() ## 2080
    ## Note: yes, EVERYTHING between ## 2070 and ## 2080 was on one line...

def L2090_more_more_curtainoptions():
    """ Further Handling of curtain options """
    ## Certain DT ("WEATHERTITE DOOR","INSULATED DOOR") do not have Curtain Options
    if VARIABLES['DT'] in (A[54],A[59]):
        "BEEP"
        print()
        L170_brightwhiteonredtext()
        print(" NO CURTAIN OPTIONS ARE AVAILABLE ON DT")
        VARIABLES['TS$']= ""
        L150_yellowonblacktext()
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2090

    ## If TS == "VISION SECTION <GRILLE>"
    if VARIABLES['TS$']=="7":
        return L2110_servicedoor_options_or_failreturntooptions()
    else:
        return L2270_validate_dt_against_ts() ## 2100
    
def L2110_servicedoor_options_or_failreturntooptions():
    """ Check if the curtain is a service door, otherwise fail and return to curtain options"""
    ## If DT == 'SERVICE DOOR'
    if VARIABLES['DT']==A[53]:
        return L2120_crownslat_visionsection_or_failreturntooptions()
    else:
        print()
        L170_brightwhiteonredtext()
        print("A[76][:-23] Not AVAILABLE ON DT")
        L150_yellowonblacktext()
        return L1990_beep_and_L110_rundelay_and_L2000_curtainoptions ## 2110

def L2120_crownslat_visionsection_or_failreturntooptions():
    """ Check if the curtain has the correct slats, otherwise fail and return to curtain options"""
    ## TS <2 MAY BE ["3 5/8 INCH CROWN SLAT","2 7/8 INCH CROWN SLAT"] (atm I don't know where 'TS' came from [again, not 'TS$')
    if VARIABLES['TS']<=2 or VARIABLES['TS$'] in ["1","2"]:
        return L2130_visionsection_grill_options()
    else:
        print()
        L170_brightwhiteonredtext()
        print("VISION SECTION AVAILABLE ONLY WITH CROWN SLAT SERVICE DOORS")
        L150_yellowonblacktext
        return L1990_beep_and_L110_rundelay_and_L2000_curtainoptions() ## 2120

def L2130_visionsection_grill_options():
        """ Gathers the options for the Vision Section <Grille> """
        print()
        L200_blueonwhitetext()
        ## The following was originally a print->insert combo
        VARIABLES['OGS'] = INPUT(" Enter AMOUNT OF OPEN GRILLE SECTION in INCHES (STD = 11.25) ")
        L150_yellowonblacktext()
        "LOCATE 21, 66"
        ## input statement was here
        ## 2130
        print()
        print()
        L200_blueonwhitetext()
        ## The following was originally a print->insert combo
        VARIABLES['VCL'] = input(" Enter CENTER LINE of Section FROM SILL in INCHES (STD = 62 INCHES) ")
        L150_yellowonblacktext()
        "LOCATE 21, 70"
        ## input statement was here
        print() ## 2140
        print()
        L200_blueonwhitetext()
        ## The following was originally a print->insert combo
        VARIABLES['GP'] = input(" Enter Vision Section GRILLE PATTERN (ASL Or CSL) ")
        L150_yellowonblacktext()
        ## input statement was here
        "LOCATE 21, 52"
        print() ## 2150
        "LOCATE 23,1"
        L190_blackongreentext()
        ## A76 = <7> VISION SECTION <GRILLE>
        print('VARIABLES["OGS"]" A[76][:23] CENTERED AT VARIABLES["VCL"]" ABOVE FLOOR')
        L150_yellowonblacktext()
        print()
        L110_rundelay() ## 2160
        if VARIABLES['GP']=="ASL" or VARIABLES['GP']=="CSL":
            return L2180_get_grille_finish_and_2190_ask_grille_finish()
        ## Note: This was an explicit endless Loop O.o?
        ## Original: Beep: GoTo 2160
        ## Which would result in no changes... Rewritten to avooid loop
        ## and explain why the GP selection is Wrong
        else:
            "BEEP"
            print("Invalid Vision Section GRILLE PATTERN") ## Added Line
            return L2130_visionsection_grill_options() ## Modified ## 2170

def L2180_get_grille_finish_and_2190_ask_grille_finish():
    """ Shows the Grille Finish Options before asking for input via 2190.

    These two functions are technically one group of lines in basic which loops over 2190
    on invalid input.
    """
    "CLS"
    print()
    L160_whiteonbluetext()
    print(" ***** SELECT GRILLE FINISH ***** ")
    L150_yellowonblacktext()
    print()
    print("<1> A[69]")
    print()
    print("<2> A[70] (BROWN)")
    print()
    print("<3> A[70] (GREY)")
    print()
    print("<4> A[71]")
    print()
    print("<5> A[72]")
    print()
    print() ## 2180
    ## "<1> MILL ALUMINUM
    ##
    ##  <2> ALUM. LINKS/PLASTIC TUBES (BROWN)
    ##
    ##  <3> ALUM. LINKS/PLASTIC TUBES (GREY)
    ##
    ##  <4> ANODIZED ALUMINUM
    ##
    ##  <5> DURANODIC ALUMINUM
    ##
    ##
    return L2190_ask_grille_finish()

def L2190_ask_grille_finish():
    """ Asks the Grille Finish; either called by 2180_get_grille_finish or functions as a loop """
    VARIABLES['GF']=INPUT("SELECT GRILLE FINISH")
    if int(VARIABLES['GF']) <= 5:
        return L2200_set_rw_and_convert_gf_and_L2260_print_grillfinish_and_L290_L110_rundelay_and_L590_loadvars_and_main_menu()
    else:
        "BEEP"
        return L2190_ask_grille_finish() #2190

def L2200_set_rw_and_convert_gf_and_L2260_print_grillfinish_and_L290_L110_rundelay_and_L590_loadvars_and_main_menu():
    """ Sets the RW Variable, converts the grille finish index to it's name, and then retuns 2260 """
    if VARIABLES['GF'] in ["2","3"]:
        VARIABLES['RW']=.02544
    else:
        VARIABLES['RW']=.0272176 ## 2200
    if VARIABLES['GF']=="1":
        VARIABLES['GF']=A[69]
        return L2260_print_grillfinish_and_L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2210
    if VARIABLES['GF']=="2":
        VARIABLES['GF']=A[70]+" (BROWN)"
        return L2260_print_grillfinish_and_L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2220
    if VARIABLES['GF']=="3":
        VARIABLES['GF']=A[70]+" (GREY)"
        return L2260_print_grillfinish_and_L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2230
    if VARIABLES['GF']=="4":
        VARIABLES['GF']=A[71]
        return L2260_print_grillfinish_and_L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2240
    if VARIABLES['GF']=="5":
        VARIABLES['GF']=A[72]
        return L2260_print_grillfinish_and_L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2250
    ## There is no catch here for invalid variables
    ## because it's supposed to have been caught in L2190

def L2260_print_grillfinish_and_L290_L110_rundelay_and_L590_loadvars_and_main_menu():
    """ Prints the resulting grille finish and then returns to the main menu... I don't know why we bother, but whatever"""
    print()
    L160_whiteonbluetext()
    print("VARIABLES['GF']")
    L150_yellowonblacktext()
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2260

def L2270_validate_dt_against_ts():
    ## DT == 'SERVICE DOOR', TS == 
    if VARIABLES['DT']==A[53] and VARIABLES['TS$']=="5":
        print()
        L170_brightwhiteonredtext()
        print(" Not AVAILABLE ON VARIABLES['DT$'] ")
        VARIABLES['TS$'] = ""
        L150_yellowonblacktext()
        return L1990_beep_and_L110_rundelay_and_L2000_curtainoptions() ## 2270

    ## DT == 'ROLLING GRILLE', TS == <1> 3 5/8 INCH CROWN SLAT/<2> 2 7/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[56] and VARIABLES['TS$'] in ["1","2"]:
        ## <5> SOLID SLATS AT BOTTOM OF ROLLING GRILLE
        VARIABLES['TS$']="5"
        return L2330_get_height_of_bottom() ## 2280

    ## DT == 'ROLLING GRILLE', TS == <5> SOLID SLATS AT BOTTOM OF ROLLING GRILLE
    if VARIABLES['DT']==A[56] and VARIABLES['TS$'] != "5":
        print()
        print("Not AVAILABLE ON VARIABLES['DT']")
        VARIABLES['TS'] = 5
        VARIABLES['TS$'] = ""
        return L1990_beep_and_L110_rundelay_and_L2000_curtainoptions() ## 2290

    if VARIABLES['TS']==5:
        return L2310_validate_type5_slat()
    else:
        return L2370_slattype6_fork() ## 2300

def L2310_validate_type5_slat():
    """ Validates options for slat type 5 (SOLID SLATS AT BOTTOM OF ROLLING GRILLE?) """
    ## atm EG hasn't been assign for me to know for sure, but assumably it stands for Extruded [Aluminum Grille] Guides
    if VARIABLES['EG']=="Y":
        "BEEP"
        print()
        print("Not AVAILABLE WITH EXTRUDED ALUMINUM GRILLE GUIDES")
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2310
    ## atm BB hasn't been assigned, but assumably it's the type of Bottom Bar == STANDARD TUBULAR ALUMINUM
    if VARIABLES['BB']==A[81]:
        "BEEP"
        print()
        print("Not AVAILABLE WITH A[81] BOTTOM BAR")
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2320
    ## This function implicitly rolls into L2330, which is also called by other forks
    return L2330_get_height_of_bottom()

def L2330_get_height_of_bottom():
    """ Gets the height of the bottom slats and bottom bar """
    if VARIABLES['TS$']=="5":
        print()
        VARIABLES['SBH'] = input("ENTER HEIGHT OF SOLID BOTTOM SLATS (INCLUDING BOTTOM BAR - IN INCHES)")
        print() ## 2330
    ## This function implicitly rolls into L2340, which is also called by other forks
    return L2340_get_bottom_slat_type()

def L2340_get_bottom_slat_type():
    """ Gets the bottom slat type and validates it """
    VARIABLES['BST'] = input("SLAT TYPE (#1 or #2)")
    if VARIABLES['BST']=="#1":
        print()
        print("VARIABLES['SBH'] INCHES A[30][-21:] AT BOTTOM (INCLUDING BOTTOM BAR)")
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2340

    if VARIABLES['BST']=="#2":
        print()
        print("VARIABLES['SBH'] INCHES A[31][-21:] AT BOTTOM (INCLUDING BOTTOM BAR)")
    else:
        "BEEP"
        return L2340_get_bottom_slat_type() ## 2350

    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2360

def L2370_slattype6_fork():
    """ Forks based on whether slattype is PERFORATED SLATS """
    if VARIABLES['TS$']=="6":
        return L2380_validate_preforated_slats()
    else:
        return L2430_validate_and_record_slat_stats() ## 2370

def L2380_validate_preforated_slats():
    """ Checks if DT is service door, proceeding or failing """
    ## DT == 'SERVICE DOOR'
    if VARIABLES['DT']==A[53]:
        return L2390_get_preforated_slat_options()
    else:
        print()
        print("A[79] Not AVAILABLE ON VARIABLES['DT']")
        VARIABLES['TS$'] = ""
        return L1990_beep_and_L110_rundelay_and_L2000_curtainoptions() ## 2380

def L2390_get_preforated_slat_options():
    """ Gets the preforated slat options before returning to main menu """
    print()
    print()
    L200_blueonwhitetext()
    ## The following was originally a print->insert combo
    VARIABLES['PSH'] = input(" ENTER HEIGHT OF A[79] SECTION (IN INCHES) ")
    L150_yellowonblacktext()
    "LOCATE 21, 58"
    ## input was here ## 2390
    if VARIABLES['PSH']>VARIABLES['SH']:
        "BEEP"
        L170_brightwhiteonredtext()
        print()
        print("EXCEEDS STOP HEIGHT ")
        L150_yellowonblacktext()
        return L1990_beep_and_L110_rundelay_and_L2000_curtainoptions() ## 2400
    print()
    print()
    L200_blueonwhitetext()
    ## The following was originally a print->insert combo
    VARIABLES['PSCL'] = input(" Enter CENTER LINE of Section FROM SILL in INCHES (STD = 62 INCHES) ")
    L150_yellowonblacktext()
    "LOCATE 21, 70"
    ## input was here
    print() ## 2410
    "LOCATE 23,1"
    L190_blackongreentext()
    print('VARIABLES["PSH"]" OF A[79] CENTERED AT VARIABLES["PSCL"]" ABOVE FLOOR ')
    L150_yellowonblacktext()
    print()
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2420

def L2430_validate_and_record_slat_stats():
    ## TS == 3 5/8 INCH CROWN SLAT; DT == 'FIRE DOOR'
    if VARIABLES['TS$']=="1" and VARIABLES['DT']==A[55] and VARIABLES['CW']>216 and VARIABLES['SH']>144:
        "BEEP"
        print()
        print("MUST USE 18 GAGE 2 7/8 CROWN SLAT FOR THIS SIZE A[55]")
        ## Set to 2 7/8 INCH CROWN SLAT
        VARIABLES['TS'] = 2
        return L1990_beep_and_L110_rundelay_and_L2000_curtainoptions() ## 2430

    if VARIABLES['TS$']=="1" and VARIABLES['CW']>216:
        print()
        print("TOO WIDE FOR 3 5/8 SLAT")
        return L1990_beep_and_L110_rundelay_and_L2000_curtainoptions() ## 2440
        
    if VARIABLES['TS$']=="1":
        VARIABLES['TS']=1
        VARIABLES['IR'] = 0.5
        VARIABLES['HS'] = 3.625
        L160_whiteonbluetext()
        print(A[30][-21:])
        ## 3 5/8 INCH CROWN SLAT
        L150_yellowonblacktext()
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2450

    ## Added in logic parens
    ## TS/TS$ == 2 7/8 INCH CROWN SLAT; DT == 'FIRE DOOR'
    if (VARIABLES['TS$']=="2" and VARIABLES['DT']==A[55]) or (VARIABLES['TS']==2 and VARIABLES['DT']==A[55]):
        VARIABLES['TS']=2
        VARIABLES['IR'] = 0.695
        VARIABLES['HS'] = 2.875
        L160_whiteonbluetext()
        print(A[31][-21:])
        ## 2 7/8 INCH CROWN SLAT
        L150_yellowonblacktext()
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2460

    ## TS == 2 7/8 INCH CROWN SLAT; DT == 'SERVICE DOOR'
    if VARIABLES['TS$']=="2" and VARIABLES['DT']==A[53]:
        VARIABLES['TS']=2
        print()
        L220_brightwhiteongreentext()
        print(" A[31] Is STANDARD SLAT ON VARIABLES['DT'] ")
        L150_yellowonblacktext()
        ## Note, I don't know why we error beep here and don't assing IR/HS...
        "BEEP"
        return L1990_beep_and_L110_rundelay_and_L2000_curtainoptions() ## 2470

    ## TS == 2 1/2 INCH FLAT SLAT
    if VARIABLES['TS$']=="3" and VARIABLES['CW']>=366:
        print("DOOR TOO WIDE FOR A[32][-20:]")
        ## Convert to 2 7/8 Crown
        VARIABLES['TS']=2
        return L1990_beep_and_L110_rundelay_and_L2000_curtainoptions() ## 2480

    ## TS == 2 1/2 INCH FLAT SLAT
    if VARIABLES['TS$']=="3":
        VARIABLES['TS']=3
        VARIABLES['IR']=.715
        VARIABLES['HS']=2.54
        L160_whiteonbluetext()
        print("A[32][-20:]")
        ## 2 1/2 INCH FLAT SLAT
        L150_yellowonblacktext()
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2490

    ## TS == MIDGET CROWN SLAT < 2 INCH >
    if VARAIBLES['TS$']=="4":
        VARIABLES['TS']=4
        VARIABLES['IR']=.438
        VARIABLES['HS']=2
        L160_whiteonbluetext()
        print("A[74][-28:]")
        ## MIDGET CROWN SLAT < 2 INCH >
        L150_yellowonblacktext()
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2500

    ## NOTE: I do not believe that this function rolls into the next line (this is very much
    ## exemplary of why this form of programming is so fubar). In case it does, next line is
    ## L2520

def L2510_override_slat_gage_options():
        """ Asks to override slat gage options for gages that are too light """
        ##  SLAT GAGE OPTIONS ## 2510
        VARIABLES['OVR']=""
        "BEEP"
        print()
        print("""VARIABLES['SGO'] GAGE TOO LIGHT FOR VARIABLES['FF']'-VARIABLES['FI']" x VARIABLES['HF']'-VARIABLES['HI']" DOOR USING SLAT #VARIABLES['TS']""") ## 2520
        print()
        VARIABLES['OVR2'] = input("DO YOU WISH TO OVERIDE PARAMETERS")
        if VARIABLES['OVR2']=="Y":
            return L2540_double_check_sgo_override()
        else:
            return L2670_nonstandard_gage() ## 2530

def L2540_double_check_sgo_override():
    """ Double Checks SGO Override (OVR2) """
    print()
    VARIABLES['SURE'] = input("ARE YOU ABSOLUTLY SURE")
    if VARIABLES['SURE']=="Y":
        L2990_parameter_override()
        return L2730_more_validate_sgo22() ## 2540

    if VARIABLES['SURE']=="N":
        ## The following was originally GOTO 2570, but that seems to be an error;
        ## I've changed it to 2560
        return L2560_abort_override()
    else:
        return L2540_double_check_sgo_override() ## 2550

def L2560_abort_override():
    """ Confirms that SGO Override was aborted """
    "BEEP"
    print("ABORTED")
    return L2660_L110_rundelay_and_L2670_nonstandard_gage() ## 2560

def L2570_check_pipe_only():
    """ Checks if PJ ends with PIPE ONLY and forks """
    if VARIABLES['PJ'][-10:]=="PIPE ONLY)":
        return L2590_pipe_slat_type_fork() ## 2570
    return L2630_invalid_gages() ## 2580

def L2590_pipe_slat_type_fork():
    """ For Pipe Jobs, checks the slat type and forks """
    ## REM: FOR RELACEMENT PIPE SHAFT SPRING CALCULATIONS ONLY (2590)
    ## TS == [2 7/8 INCH CROWN SLAT, 2 1/2 INCH FLAT SLAT]
    if VARIABLES['TS'] in [2,3]:
        return L2610_set_sg22_gage()
    else:
        return L2620_sg22_check_midgetcrown() ## 2600

def L2610_set_sg22_gage():
    """ Sets the stats for SG22 """
    VARIABLES['SG']="22"
    VARIABLES['SW']=.05
    print()
    L160_whiteonbluetext()
    print("VARIABLES['SGO'] GAGE SLATS")
    L150_yellowonblacktext()
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2610

def L2620_sg22_check_midgetcrown():
    """ Checks if Slat Type is Midget Crown; if so set SG22"""
    if VARIABLES['TS']==4:
        VARIABLES['SG']="22"
        VARIABLES['SW']=.033
        print()
        L160_whiteonbluetext()
        print("VARIABLES['SGO'] GAGE MIDGET SLATS")
        L150_yellowonblacktext()
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2620
    ## This function seems to roll over into L2630
    return L2630_invalid_gages()
    
def L2630_invalid_gages():
    """ Posts Error Messages for inapproprate Gages """
    ## DT == 'FIRE DOOR'; TS == 3 5/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==1:
        "BEEP"
        print()
        L170_brightwhiteonredtext()
        print("VARIABLES['SGO$'] GAGE NOT AVAIABLE FOR A[30][-21:] ON VARIABLES['DT']")
        L150_yellowonblacktext()
        return L2660_L110_rundelay_and_L2670_nonstandard_gage() ## 2630

    ## DT == 'FIRE DOOR'; TS == 2 7/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==2:
        "BEEP"
        print()
        L170_brightwhiteonredtext()
        print("VARIABLES['SGO'] GAGE NOT AVAIABLE FOR A[31][-21:] ON VARIABLES['DT']")
        L150_yellowonblacktext()
        return L2660_L110_rundelay_and_L2670_nonstandard_gage() ## 2640

    "BEEP"
    L170_brightwhiteonredtext()
    print("SLAT #VARIABLES['TS'] NOT MADE IN VARIABLES['SGO$'] GAGE")
    L150_yellowonblacktext()
    return L2660_L110_rundelay_and_L2670_nonstandard_gage() ## 2650

def L2660_L110_rundelay_and_L2670_nonstandard_gage():
    """ This function runs a delay for the previous error message before returning to L2670 """
    L110_rundelay() ## 2660
    ## This function seems to roll over into L2670
    return L2670_nonstandard_gage()
    
def L2670_nonstandard_gage():
    ## DT == 'INSULATED DOOR'
    if VARIABLES['DT']==A[59]:
        return L2960_invalid_gage_options() ## 2670

    ## SGO Override Variable
    VARIABLES['OVR2']=""
    "CLS"
    L160_whiteonbluetext()
    print(" ******** SELECT SLAT GAGE OPTION ******** ")
    L150_yellowonblacktext()
    print() ## 2680
    print()
    print("<1> 22 GAGE")
    print()
    print("<2> 20 GAGE")
    print()
    print("<3> 18 GAGE")
    print()
    print("<4> A[77]")
    ## 'RETURN TO MAIN MENU'
    print()
    print()
    VARIABLES['GON'] = input("ENTER GAGE OPTION NUMBER:") ## 2690
    ongon = [None,
                L2710_validate_sgo22,
                L2760_validate_sgo20,
                L2900_validate_sgo18,
                L290_L110_rundelay_and_L590_loadvars_and_main_menu]
    return ongon[int(VARIABLES['GON'])]() ## 2700

def L2710_validate_sgo22():
    """ Validates SGO22 """
    VARIABLES['SGO']="22"
    ## TS == [2 7/8 INCH CROWN SLAT, 2 1/2 INCH FLAT SLAT, MIDGET CROWN SLAT < 2 INCH >]
    if VARIABLES['TS'] in [2,3,4]:
        return L2570_check_pipe_only() ## 2710

    ## DT == 'FIRE DOOR' or TS == PREFORATED SLATS
    if VARIABLES['DT']==A[55] or VARIABLES['TS']==6:
        return L2630_invalid_gages() ## 2720
        
    ## This function rolls over into L2730
    return L2730_more_validate_sgo22()

def L2730_more_validate_sgo22():
    """ More validations for SG022 """
    ## Logic Parens added
    ## TS1 == 3 5/8 INCH CROWN SLAT; TS5 == SOLID SLATS AT BOTTOM OF ROLLING GRILLE
    if (VARIABLES['TS']==1 and VARIABLES['CW']<=165) or (VARIABLES['TS']==5 and VARIABLES['CW']<=220.75):
        return L2980_default_selected() ## 2730

    ## Logic Parens added
    ## TS1 == 3 5/8 INCH CROWN SLAT; TS5 == SOLID SLATS AT BOTTOM OF ROLLING GRILLE
    if (VARIABLES['TS']==1 and VARIABLES['CW']>165 and VARIABLES['OVR2']=="") or (VARIABLES['TS']==5 and VARIABLES['CW']>220.75 and VARIABLES['OVR2']==""):
        return L2510_override_slat_gage_options() ## 2740

    ## Logic Parens added
    ## TS1 == 3 5/8 INCH CROWN SLAT; TS5 == SOLID SLATS AT BOTTOM OF ROLLING GRILLE
    if (VARIABLES['TS']==1 and VARIABLES['OVR2']=="Y") or (VARIABLES['TS']==5 and VARIABLES['OVR2']=="Y"):
        VARIABLES['SG']="22"
        print("22 GAGE A[30][-21:] A[80]")
        VARIABLES['SW']=5.378666E-02
        VARIABLES['EL']=.21875
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2750
        
    ## It is highly unlikely, but I will note that this function is clearly wide open
    ## and could have potentially rolled into L2760 (SGO20, which means it really
    ## should not have been left open)

def L2760_validate_sgo20():
    """ Validates SGO20 """
    VARIABLES['SGO']="20"
    ## TS == 3 5/8 INCH CROWN SLAT
    if VARIABLES['TS']==1 and VARIABLES['CW']>216 and VARIABLES['OVR2']=="":
        return L2510_override_slat_gage_options() ## 2760

    ## TS1 == 3 5/8 INCH CROWN SLAT; DT == 'FIRE DOOR'; TS5 == SOLID SLATS AT BOTTOM OF ROLLING GRILLE
    if (VARIABLES['TS']==1 and VARIABLES['CW']>165 and VARIABLES['OVR2']=="") or (VARIABLES['DT']==A[55] and VARIABLES['SH']<=144) or (VARIABLES['TS']==5 and VARIABLES['CW']>220.75 and VARIABLES['OVR2']==""):
        return L2980_default_selected() ## 2770

    ## TS == 3 5/8 INCH CROWN SLAT
    if VARIABLES['TS']==1:
        print()
        print("20 GAGE A[30][-21:]")
        VARIABLES['SW']=.058514166
        VARIABLES['SG']="20"
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2780

    ## TS == 2 7/8 INCH CROWN SLAT; DT == 'FIRE DOOR'
    if VARIABLES['TS']==2 and VARIABLES['DT']==A[55] and VARIABLES['CW']>216 and VARIABLES['SH']>144:
        "BEEP"
        print("""SLAT MUST BE 18 GAGE FOR VARIABLES['FF']'-VARIABLES['FI']" x VARIABLES['HF']'-VARIABLES['HI']" A[55]""")
        VARIABLES['SG']="18"
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2790

    ## TS == 2 7/8 INCH CROWN SLAT; DT == 'FIRE DOOR'
    if VARIABLES['TS']==2 and VARIABLES['DT']==A[55] and VARIABLES['SH']<=144:
        return L2980_default_selected() ## 2800

    ## TS == 2 7/8 INCH CROWN SLAT
    if VARIABLES['TS']==2 and VARIABLES['CW']<=220.75:
        return L2980_default_selected() ## 2810

    ## TS == 2 7/8 INCH CROWN SLAT; DT != 'FIRE DOOR'
    if VARIABLES['TS']==2 and VARIABLES['DT']!=A[55] and VARIABLES['CW']<=244.75 and VARIABLES['SH']<=160.75:
        return L2980_default_selected() ## 2820

    ## TS == 2 7/8 INCH CROWN SLAT
    if (VARIABLES['TS']==2 and VARIABLES['CW']>244.75 and VARIABLES['OVR2']=="") or (VARIABLES['TS']==2 and VARIABLES['CW']>220.75 and VARIABLES['SH']>160.75 and VARIABLES['OVR2']==""):
        return L2510_override_slat_gage_options() ## 2830

    ## TS == 2 7/8 INCH CROWN SLAT
    if VARIABLES['TS']==2 and VARIABLES['SURE']=="Y":
        print()
        print("20 GAGE A[31][-21:]")
        VARIABLES['SW']=5.485475E-02
        VARIABLES['SG']="20"
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2840
    
    ## TS == 2 1/2 INCH FLAT SLAT; GON == 20 GAGE
    if VARIABLES['TS']==3 and VARIABLES['GON']==2 and VARIABLES['CW']<=220.75:
        return L2980_default_selected() ## 2850

    ## TS == 2 1/2 INCH FLAT SLAT; GON == 20 GAGE
    if VARIABLES['TS']==3 and VARIABLES['GON']==2 and VARIABLES['CW']<=244.75 and VARIABLES['SH']<=160.75:
        return L2980_default_selected() ## 2860

    ## TS == 2 1/2 INCH FLAT SLAT
    if (VARIABLES['TS']==3 and VARIABLES['CW']>244.75 and VARIABLES['OVR2']=="") or (VARIABLES['TS']==3 and VARIABLES['CW']>220.75 and VARIABLES['SH']>160.75 and VARIABLES['OVR2']==""):
        return L2510_override_slat_gage_options() ## 2870

    ## TS == 2 1/2 INCH FLAT SLAT
    if VARIABLES['TS']==3 and VARIABLES['OVR2']=="Y":
        print()
        print("20 GAGE A[32][-20:]")
        VARIABLES['SW']=5.485475E-02
        VARIABLES['SG']="20"
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2880
    
    ## TS == MIDGET CROWN SLAT < 2 INCH >
    if VARIABLES['TS']==4:
        return L2980_default_selected() ## 2890

def L2900_validate_sgo18():
    VARIABLES['SGO']="18"
    ## TS1/ST/BST == 3 5/8 INCH CROWN SLAT; TS4 == MIDGET CROWN SLAT < 2 INCH >; TS6 == PREFORATED SLATS
    if VARIABLES['TS']==1 or VARIABLES['TS']==4 or VARIABLES['BST']=="#1" or VARIABLES['ST_S']=="#1" or VARIABLES['TS']==6:
        return L2630_invalid_gages() ## 2900

    ## TS/BST == 2 7/8 INCH CROWN SLAT
    if VARIABLES['ST_S']=="#2" or VARIABLES['BST']=="#2":
        print()
        print("18 GAGE TOP and/or BOTTOM SLATS")
        VARIABLES['SW']=.071269154
        VARIABLES['SG']="18"
        VARIABLES['ST_S']="#2"
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2910

    ## DT == 'FIRE DOOR'
    if VARIABLES['DT']==A[55] and VARIABLES['CW']>216 and VARIABLES['SH']>=144:
        return L2980_default_selected() ## 2920

    if VARIABLES['CW']>220.75 and VARIABLES['SH']>160.75 or VARIABLES['CW']>244.75:
        return L2980_default_selected() ## 2930

    ## TS == 2 7/8 INCH CROWN SLAT
    if VARIABLES['TS']==2:
        print()
        L160_whiteonbluetext()
        print("18 GAGE A[31][-21:]")
        L150_yellowonblacktext()
        VARIABLES['SW']=.071269154
        VARIABLES['SG']="18"
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2940

    ## TS == 2 1/2 INCH FLAT SLAT
    if VARIABLES['TS']==3:
        print()
        print("18 GAGE A[32][-20:]")
        VARIABLES['SW']=.071269154
        VARIABLES['SG']="18"
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2950
        
    ## This function maybe/might/possibly roll implicitly over into L2960
    return L2960_invalid_gage_options()

def L2960_invalid_gage_options():
    """ Runs through some invalid gage options """
    ## TS == MIDGET CROWN SLAT < 2 INCH >
    if VARIABLES['TS']==4:
        return L2970_midgetcrown_invalid_gage()
    else:
        "BEEP"
        print()
        print()
        print()
        L170_brightwhiteonredtext()
        print("NO GAGE OPTIONS ARE AVAILABLE ON VARIABLES['DT']")
        L150_yellowonblacktext()
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2960

def L2970_midgetcrown_invalid_gage():
    """ Informs the user that midget chrown is only available in SG20 """
    "BEEP"
    print()
    print()
    print()
    print("MIDGET CROWN SLAT (#4) AVAILABLE ONLY IN 20 GAGE")
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 2970

def L2980_default_selected():
    """ User has selected the default Slat Gage under Non-Standard Gage Option """
    "BEEP"
    print()
    L190_blackongreentext()
    print(""" VARIABLES['SGO'] GAGE IS STANDARD FOR SLAT #VARIABLES['TS'] WHEN DOOR IS VARIABLES['FF']'-VARIABLES['FI']" x VARIABLES['HF']'-VARIABLES['HI']" """)
    VARIABLES['SG']=VARIABLES['SGO']
    L150_yellowonblacktext()
    return L2660_L110_rundelay_and_L2670_nonstandard_gage() ## 2980
        
def L2990_parameter_override():
    """ Displays '!!!!!!!!!! PARAMETER OVERIDE !!!!!!!!!!' 3 times """
    for X in range(1,4):
        "BEEP"
        print("A[80]")
        print()
    print()
    return ## 2990

def L3000_add_astragal():
    """ Adds Astragal """
    print()
    L160_whiteonbluetext()
    print(" ASTRAGAL ON BOTTOM BAR ")
    L150_yellowonblacktext()
    VARIABLES['AS']=.5
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3000

def L3010_add_safety_edge():
    """ Safety Edge Selection menu """
    "CLS"
    L160_whiteonbluetext()
    print(" ***** SELECT SAFETY EDGE TYPE *****")
    L150_yellowonblacktext() ## 3010
    
    print()
    print("<1> A[88]")
    print()
    print("<2> A[89]") ## 3020
    ##
    ## <1> ELECTRIC (Miller Edge)
    ##
    ## <2> PNEAUMATIC (Air)

    print()
    VARIABLES['SEBB'] = input("SELECT SAFETY EDGE TYPE")
    ## Note! The Menu only displays 2 Options, but ON SEBB lists 3 Options
    onsebb = [None,L3040_add_miller_edge_safety,
              3050,
              3130]
    return onsebb[int(VARIABLES['SEBB'])]() ## 3030

























def L10670_set_middle_front_angle():
    """ Sets the sizes for Middle and Front Angles (or Extruded Angles, if present) """
    ## US: Upset
    ## MAL: Middle Angle, SH: Stop height
    ## FAL: Front Angle
    if VARIABLES['US']==0:
        VARIABLES['MAL'] = VARIABLES['SH']-.125
        format_float_as_measurement("MAL")
        ## This line was originally FAL = ED, but it makes more sense to just set it to MAL
        VARIABLES['FAL']=VARIABLES['MAL']
        return L10700_print_job() ## 10670
    ## EG: Extruded Guides
    ## EAGL: Alum Grille Guide
    if VARIABLES['EG']=="Y":
        VARIABLES['EAGL']=VARIABLES['SH']+VARIABLES['US']+2.5
        format_float_as_measurement("EAGL")
        return L10700_print_job() ## 10680
    ## US: Upset, HXP: Heat Expansion Gap
    VARIABLES['MAL']=VARIABLES['SH']+VARIABLES['US']+2.5-VARIABLES['HXP']
    format_float_as_measurement("MAL")
    VARIABLES['FAL']=VARIABLES['SH']+VARIABLES['US']+1-VARIABLES['HXP']
    format_float_as_measurement("FAL") ## 10690
    return L10700_print_job() ## Implicit
    
def L10700_print_job():
    """ Begin outputting the results of the job """
    ## WAL: Wall Angle, SH: Stop Height, US: Upset, BP: Bracket Plate Height, HXP: Heat Expansion Gap
    VARIABLES['WAL']=VARIABLES['SH']+VARIABLES['US']+VARIABLES['BP']-VARIABLES['HXP']
    format_float_as_measurement("WAL") ## 10700
    print()
    print()
    ## Since the variables in the output are clearly defined, I won't comment them
    print("ENGINEERING and SPRING CALCULATIONS") ## 10710
    print("CUSTOMER: VARIABLES['C_S'] PROJECT:  VARIABLES['PJ']") ## 10720
    print("JOB N0: VARIABLES['JN'] \t MARK: VARIABLES['MK'] \t HAND: VARIABLES['HD'] \t\t MODEL: VARIABLES['DM']") ## 10730
    print("VARIABLES['DT'] \t VARIABLES['MT'] \t VARIABLES['OP'] \t\t VARIABLES['MF']") ## 10740
    print("CLEAR OPENING WIDTH: VARIABLES['CW'] \t HEIGHT TO STOPS: VARIABLES['SH']") ## 10750
    print('BETWEEN BRACKETS: VARIABLES["GR"] \t BRACKET PLATE: str(VARIABLES["BP"])" x VARIABLES["TB"]"') ## 10760
    print('VARIABLES["P"]" x VARIABLES["PL"] \t INNER SHAFT: VARIABLES["IS"]"') ## 10770
    ## STS: ???
    if VARIABLES['STS']!="":
        print('VARIABLES["STS"] \t UPSET: str(VARIABLES["US"])" \t\t GUIDE TYPE: VARIABLES["GD"]-VARIABLES["PO"]-VARIABLES["MA"]')
        return L10820_print_pipe_center_plus() ## 10780
    print('WALL ANGLE: VARIABLES["WAL"]  <VARIABLES["WAT"]">" \t UPSET: str(VARIABLES["US"])" \t\t GUIDE TYPE: VARIABLES["GD"]-VARIABLES["PO"]-VARIABLES["MA"]') ## 10790
    ## EG: Extruded Gudies
    if VARIABLES['EG']=="Y":
        print("ALUM. GRILLE GUIDE: VARIABLES['EAGL']")
        return L10820_print_pipe_center_plus() ## 10800
    print("MIDDLE ANGLE: VARIABLES['MAL'] \t FRONT ANGLE: VARIABLES['FAL']") ## 10810
    return L10820_print_pipe_center_plus() ## Implicit

def L10820_print_pipe_center_plus():
    """ Outputs Pipe's Center Line and more info depending if DT is Fire Door """
    ## DT == FIRE DOOR
    if VARIABLES['DT']==A[55]:
        print('CENTER LINE OF PIPE: str(VARIABLES["HC"])" \t HEAT EXPANSION GAP: str(VARIABLES["HXP"])"')
        return L10840_print_curtain_lift_info() ## 10820
    print('CENTER LINE OF PIPE: str(VARIABLES["HC"])" \t WINDLOCK SPACING: EVERY VARIABLES["WL"]th SLAT') ## 10830
    return L10840_print_curtain_lift_info() ## Implicit

def L10840_print_curtain_lift_info():
    """ Outputs info about the curtain's weight and related stats """
    print("HANGING WEIGHT CLOSED: math.ceil(VARIABLES['HW'])# \t HANGING WEIGHT OPEN: math.ceil(VARIABLES['WU'])#") ## 10840
    print('INITIAL LEVER ARM: str(VARIABLES["IL"])" \t TURNS TO RAISE: VARIABLES["TR"]') ## 10850
    print('FINAL LEVER ARM: VARIABLES["FL"] \t TORQUE REQUIRED CLOSED: math.ceil(VARIABLES["TD"])"/#') ## 10860
    print('TORQUE REQUIRED OPEN: math.ceil(VARIABLES["TU"]) "/# \t PRE-TURNS TO HOLD: VARIABLES["PT"]') ## 10870
    print('REQUIRED "/# PER TURN: math.ceil(VARIABLES["IP"]) "/# \t TOTAL APPLIED TURNS: VARIABLES["TT"]') ## 10880
    ## OGS: Open Grille Section
    if VARIABLES["OGS"]==0:
        return L10910_fork_grille_output()
    else:
        print("E\tVISION SECTION (GRILLE) \t VARIABLES['GF'] \t F") ## 10890

    print('AMOUNT OF OPEN GRILLE: VARIABLES["GS"]" \t CENTERED AT trunacte(VARIABLES["GS"]/2+VARIABLES["NBS"]*VARIABLES["HS"]+VARIABLES["BBH"],1000)" FROM BOTTOM')
    return L10930_print_grille_info() ## 10900

def L10910_fork_grille_output():
    """ Forks between Rolling Grille and Other Door Output """
    ## DT != ROLLING GRILLE
    if VARIABLES['DT']!=A[56]:
        return L10960_print_slat_info_non_grille() ## 10910
    print("CURTAIN TYPE: ALUMINUM GRILLE \t GRILLE PATTERN: VARIABLES['GP']") ## 10920
    return L10930_print_grille_info() ## Implicit

def L10930_print_grille_info():
    """ Outputs a stats for Rolling Grilles """
    print('FIRST TUBE: str(VARIABLES["FT"])" \t STD. TUBES: VARIABLES["TST"] str(VARIABLES["TL"])" \t\t TOTAL LINKS:VARIABLES["TNL"]') ## 10930
    print("N0. OF RODS: VARIABLES['NR'] \t ROD LENGTH: VARIABLES['RL']") ## 10940
    print("SLAT TYPE: VARIABLES['ST_S'] \t SLAT GAGE:  VARIABLES['SG']")
    return L10970_calculate_print_special_slats() ## 10950

def L10960_print_slat_info_non_grille():
    """ Outputs the slat info for Non-Rolling Grille Doors """
    print('SLAT TYPE: #VARIABLES["TS"] \t SLAT GAGE: VARIABLES["SG"]" GA.') ## 10960
    return L10970_calculate_print_special_slats() ## Implicit

def L10970_calculate_print_special_slats():
    """ Calculates some special slat info and outputs it """
    ## AJ: ???, AJF: ???
    if VARIABLES['AJ']==4:
        VARIABLES['AJF']=.42 ## 10970
    ## TS: Type Slat == PERFORATED SLATS
    if VARIABLES['TS']==6:
        return L11200_calculate_wrap() ## 10980
    ## SBS: SOLID BOTTOM HEIGHT
    if VARIABLES['SBS']!=0:
        print("E\tN0. OF TOP SLATS: VARIABLES['NTS'] \t N0. OF BOTTOM SLATS: VARIABLES['NBS']\tF\tSOLID BOTTOM HEIGHT: VARIABLES['SBS'] \t SLAT LENGTH: VARIABLES['SL']")
        return L11040_print_bottom_bar() ## 10990
    ## PD: ???
    if VARIABLES['PD']!="":
        print("# OF TOP SLATS:VARIABLES['NTS'] \t TOP SLAT LENGTH: VARIABLES['SL'] # OF BOTTOM SLATS:VARIABLES['NBS'] (VARIABLES['NTS']+VARIABLES['NBS']) \t BOTTOM SLAT LENGTH: VARIABLES['BSL']\tF")
        return L11040_print_bottom_bar() ## 11000
    ## PSH: Perforated Slat Height, PSCL: Perforated Slat Center Line
    if VARIABLES['PSH']!=0 and VARIABLES['PSCL']!=0:
        print('A[79]:VARIABLES["NPS"] @VARIABLES["FPFE"]" \t BEGINNING AT SLAT #VARIABLES["FPSFB"] FROM BOTTOM \t F') ## 11010
    print("TOTAL N0. OF SLATS: VARIABLES['TNS'] \t SLAT LENGTH: VARIABLES['SL']")
    if VARIABLES['OGS']==0:
        return L11040_print_bottom_bar() ## 11020

    print("N0. OF TOP SLATS:VARIABLES['NTS]' \t N0. OF BOTTOM SLATS:VARIABLES['NBS']") ## 11030
    return L11040_print_bottom_bar() ## Implicit

def L11040_print_bottom_bar():
    """ Outputs Bottom Bar information """
    ## SD1: Bottom Bar Slope
    if VARIABLES['SD1']!=0 :
        print('BOT.BAR: VARIABLES["BB_S"] \t SLOPE:VARIABLES["SD1"]" \t BOT.BAR WEIGHT: truncate(VARIABLES["BB"],10)')
        return L11060_calculate_print_pipe_spring_info() ## 11040
    print('BOT.BAR: VARIABLES["BB_S"] \t BOT.BAR WEIGHT:truncate(VARIABLES["BB"],10)   <VARIABLES["AW"]>') ## 11050
    return L11060_calculate_print_pipe_spring_info() ## Implicit

def L11060_calculate_print_pipe_spring_info():
    """ Runs Calculations and ouptuts Pipe and Spring info """
    ## Branches off to Calculating and Outputting Barrel Rings as well
    L11340_prepare_for_barrel_ring_calculations() ## 11060
    ## CY: Spring Cycles
    if VARIABLES['CY']=="MAX":
        L11550_print_manual_springs()
        return L11180_output_misc() ## 11070
    ## BT: ???, P: Pipe ???
    ## ??? I don't know why we are doing "not P>=5"...
    if VARIABLES["BT"]==0 and not VARIABLES['P']>=5:
        return L11160_print_spring_info() ## 11080

    if VARIABLES['BT']==11 and VARIABLES['P']>=3:
        L11550_print_manual_springs()
        return L11180_output_misc() ## 11090
    if VARIABLES['P']>=5 or VARIABLES['BT']>=14:
        L11550_print_manual_springs()
        return L11180_output_misc() ## 11100
    print('OUTER SPRING: str(VARIABLES["W1"])" WIRE x str(VARIABLES["O1"])" O.D. x str(math.ceil(VARIABLES["L1"]/.125)*.125)" LONG    STRETCH: str(math.ceil(VARIABLES["E1"]/.125)*.125)"') ## 11110
    print('RATE: str(VARIABLES["S1"])"/# \t MAX. TURNS FOR VARIABLES["CY"] CYCLES: truncate(VARIABLES["MT1"],100) \t\t SPRING WEIGHT: str(math.ceil(VARIABLES["f1"]))#') ## 11120
    print('INNER SPRING: str(VARIABLES["W2"])" WIRE x str(VARIABLES["O2"])" O.D. x str(math.ceil(VARIABLES["L2"]/.125)*.125)" LONG    STRETCH: str(math.ceil(VARIABLES["E2"]/.125)*.125)"') ## 11130
    print('RATE: str(VARIABLES["S2"])"/# \t MAX. TURNS FOR VARIABLES["CY"] CYCLES: truncate(VARIABLES["MT2"],100) \t\t SPRING WEIGHT: str(math.ceil(VARIABLES["F2"]))#') ## 11140
    print('TOTAL "/#: VARIABLES["CT"] \t TOTAL SPRING WEIGHT: str(float(VARIABLES["F3"]))#')
    return L11180_output_misc() ## 11150

def L11160_print_spring_info():
    """ Outputs Spring Information"""
    print('SPRING: str(VARIABLES["WD"])" WIRE x str(VARIABLES["OD"])" O.D. x str(math.ceil(VARIABLES["LC"]/.125)*.125)" LONG    STRETCH: truncate(VARIABLES["E1"],.125)"') ## 11160
    print('RATE: str(VARIABLES["TQ"])"/# \t MAX. TURNS FOR VARIABLES["CY"] CYCLES: truncate(VARIABLES["MT"],100) \t\t SPRING WEIGHT: str(float(VARIABLES["WS"]))#')
    print()
    print() ## 11170
    return L11180_output_misc()

def L11180_output_misc():
    """ Prints some more information before displaying the restart program menu """
    print()
    print('CURTAIN & PIPE WEIGHT: math.ceil(VARIABLES["HW"]+VARIABLES["PW"])# \t MAX. PIPE DEFLECTION LIMIT: math.ceil(VARIABLES["M"])#') ## 11180
    print("DATE: VARIABLES['DATE'] \t ENTERED BY: VARIABLES['NM']")
    return L11600_show_restart_menu() ## 11190

def L11550_print_manual_springs():
    """ Print message telling user to calculate springs manually """
    print("\t**** SELECT SPRINGS MANUALLY FROM CHARTS ****")
    print() ## 11550
    print('  QTY    WIRE     O.D.     LENGTH    "/# PER TURN    TURNS   STRETCH   WEIGHT')
    VARIABLES['X']=0
    print() ## 11560
    L11570_print_manual_spring_lines() ## Implicit

def L11570_print_manual_spring_lines():
    """ Prints lines to fill in for the manual spring input """
    print()
    print('  ___   ______   ______   ________   _________ "/#   _______  _______   ______')
    VARIABLES['X']=VARIABLES['X']+1
    if VARIABLES['X']<=2:
        return L11570_print_manual_spring_lines() ## 11570

    print()
    print('\tTOTAL "/# _________ \t\t TOTAL # ______')
    print()
    return ## 11580

def L11600_show_restart_menu():
    """ Displays the menu to restart the application """
    "KEY 9"
    """ "STOP"+VARIABLES['CHR'](13)"""
    "KEY (9) ON" ## 11600
    "KEY 10"
    """ "GOTO 280"+VARIABLES['CHR'](13)"""
    "KEY (10) ON"
    "LOCATE 25,1 " ## 11610
    L160_whiteonbluetext()
    print(" <F2> RE-RUN\t\t<F10> EXIT PROGRAM ") ## 11620
    "COLOR 14,0"
    "LOCATE 24, 1"
    print("\t\t\t\t") ## 11630
        
def L11200_calculate_wrap():
    ## WR: WRap Slats, IL:Initial Lever Arm, AJF: ???, HC: Height Center Line, NS: Slats to Center line, HS: Height Slat?
    VARIABLES["WR"]=math.ceil((2*3.1416*VARIABLES["IL"]*(.75-VARIABLES["AJF"])+VARIABLES["HC"]-math.ceil(VARIABLES["NS"]+1)*VARIABLES["HS"])/VARIABLES["HS"]) ## 11200
    ## PD: ???
    if VARIABLES['PD']!="":
        return L11220_print_insulated_slats()
    else:
        return L11240_print_slat_totals() ## 11210

def L11220_print_insulated_slats():
    """ Outputs information about insolated slats """
    print("N0. OF NON-INSULATED WRAP SLATS:VARIABLES['WR'] \t WRAP SLAT LENGTH: VARIABLES['SL']")
    print('N0. OF INSULATED TOP SLATS: math.ceil(VARIABLES["NS"]-VARIABLES["NBS"]) \t TOP SLAT LENGTH: VARIABLES["SL"]') ## 11220
    print('N0. OF BOTTOM INSULATED SLATS: VARIABLES["NBS"] \t BOTTOM SLAT LENGTH: VARIABLES["BSL"]')
    print('TOTAL N0. OF SLATS: math.ceil(VARIABLES["NS"]+VARIABLES["WR"])')
    return L11040_print_bottom_bar() ## 11230

def L11240_print_slat_totals():
    """ Outputs overview of slats """
    print("N0. OF SLATS: math.ceil(VARIABLES['NS']) PLUS VARIABLES['WR'] WRAP SLATS \t\t SLAT LENGTH: VARIABLES['SL']") ## 11240
    return L11040_print_bottom_bar() ## 11250

def L11340_prepare_for_barrel_ring_calculations():
    """ Prepares to calculate the spacing on the Barrel Rings """
    ## A Wild Documentation Appears! :O
    ## BARREL RING & TOP SLAT HOLE SPACING ## 11340
    ## DT == FIRE DOOR
    ## X: Container? Iterator?
    if VARIABLES['DT']==A[55]:
        VARIABLES['X']=24
        return L11370_barrel_ring_calculations() ## 11350
    ## HW: Hanging Weight Down
    if VARIABLES['HW']<1000:
        VARIABLES['X']=48
    else:
        VARIABLES['X']=36 ## 11360
    return L11370_barrel_ring_calculations() ## Implicit

def L11370_barrel_ring_calculations():
    """ The actual calculations for the Barrel Spings 
        
    This Function seems to form a recursive loop with L11390 in order to get X
    low enough that BS4 falls within the range 11...19 inclusive. BS4 appears
    to be the spacing of the rings: so we're ensuring that they aren't too close
    and not too far away.
    """
    ## BS1-4: Barrel (Ring) Spacing Calculations, PL: ???, X: Container from L11340?
    VARIABLES['BS1']=VARIABLES['PL']/VARIABLES['X']
    VARIABLES['BS2']=float(VARIABLES['BS1'])
    VARIABLES['BS3']=VARIABLES['BS1']-VARIABLES['BS2']
    VARIABLES['BS3']=str(VARIABLES['BS3'])
    VARIABLES['BS3']=float(VARIABLES['BS3'])
    VARIABLES['BS4']=truncate(VARIABLES['X']*VARIABLES['BS3'],10000)
    VARIABLES['BS4']=str(VARIABLES['BS4'])
    if VARIABLES['BS4'][-1:] in ("4","9"):
        VARIABLES['BS4']=float(VARIABLES['BS4'])+.0001
        return L11390_barrel_ring_calculations_part_2() ## 11370
    VARIABLES['BS4']=float(VARIABLES['BS4']) ## 11380
    return L11390_barrel_ring_calculations_part_2() ## Implicit

def L11390_barrel_ring_calculations_part_2():
    """ More Calculations for the Barrel Ring Calculations"""
    if VARIABLES['BS4']>=11 and VARIABLES['BS4']<=19:
        return L11410_calculate_output_barrel_rings() # 11390
    VARIABLES['X']=VARIABLES['X']-.5
    return L11370_barrel_ring_calculations() ## 11400

def L11410_calculate_output_barrel_rings():
    """ Calculates Barrel Ring stats and does some outputing """
    ## NOTE: The use of NBS here as a variable seems WRONG
    ## NBS: Number of Bottom Slats, BS2:Barrel (Ring) Spacing, second calculation
    VARIABLES['NBS']=VARIABLES['BS2']
    ## BRC: Barrel Ring Centers X: Container?
    VARIABLES['BRC']=VARIABLES['X']
    ## FBR: First Barrel Ring?, BS4: Barrel (Ring) Spacing, fourth calculation
    VARIABLES['FBR']=VARIABLES['BS4']/2
    ## NBR: Number of Barrel Rings, NBS: Number of Bottom Slats
    VARIABLES['NBR']=VARIABLES['NBS']+1
    ## FSH: ???, SL: Slat Length, PL: ???, BS4: Barrel (Ring) Spacing, fourth calculation
    VARIABLES['FSH']=truncate((VARIABLES['SL']-VARIABLES['PL']+VARIABLES['BS4'])/2,10000) ## 11410
    ## AJ: ???, DT == FIRE DOOR, GR = Gap Between Brackets?
    if VARIABLES['AJ']==4 or VARIABLES['DT']==A[55]:
        VARIABLES['FSH']=truncate(VARIABLES['FBR']+3.25-(VARIABLES['GR']-VARIABLES['SL'])/2,10000) ## 11420
    print( "N0. OF BARREL RINGS: VARIABLES['NBR'] \t RING CENTERS: VARIABLES['BRC']") ## 11430
    for N in range(1,VARIABLES['NBS']+1): ## 11440
        VARIABLES['N'] = N
        VARIABLES['BL'][N]=VARIABLES['FBR']+(N*VARIABLES['BRC'])
        VARIABLES['HL'][N]=VARIABLES['FSH']+(N*VARIABLES['BRC'])
        VARIABLES['BL_S'][N]=" "+str(VARIABLES['BL'][N])+" "
        VARIABLES['HL'][N]=" "+str(VARIABLES['HL'][N])+" "
        if N==6:
            return L11470_construct_barrelrings_and_topslatholes_output() ## 11450
    ## NEXT N ## 11460

def L11470_construct_barrelrings_and_topslatholes_output():
    """ Builds the strings for Outputing Barrel Rings and Top Slat Holes (and does some outputting) """
    ## Added 1 for python while retaining original intent
    ## NBS: Number of Bottom Slats
    ## BLL: Barrel Ring Location List?, FBR: ???, BRC: ???
    ## HLL: (Slat) Hole Location List?, 
    for NN in range(1,VARIABLES['NBS']-6+1): ## 11470
        VARIABLES['NN'] = NN
        ## This section was slightly reordered to read easier
        VARIABLES['BLL'][NN]=VARIABLES['FBR']+((VARIABLES['N']+NN)*VARIABLES['BRC'])
        VARIABLES['BLL'][NN]=" "+str(VARIABLES['BLL'][NN])+" "
        VARIABLES['HLL'][NN]=VARIABLES['FSH']+((VARIABLES['N']+NN)*VARIABLES['BRC'])
        VARIABLES['HLL'][NN]=" "+str(VARIABLES['HLL'][NN])+" "
        "NEXT NN" ## 11480
    ## BRL: Barrel Ring List
    VARIABLES['BRL']=str(VARIABLES['FBR'])+VARIABLES['BL'][1]+VARIABLES['BL'][2]\
        +VARIABLES['BL'][3]+VARIABLES['BL'][4]+VARIABLES['BL'][5]+VARIABLES['BL'][6]
    ## BRLL: Barrel Ring Location List
    VARIABLES['BRLL']=VARIABLES['BLL'][1]+VARIABLES['BLL'][2]+VARIABLES['BLL'][3]\
        +VARIABLES['BLL'][4]+VARIABLES['BLL'][5]+VARIABLES['BLL'][6]+VARIABLES['BLL'][7]\
        +VARIABLES['BLL'][8]+VARIABLES['BLL'][9] ## 11490
    ## TSH: Top Slat Holes
    VARIABLES['TSH']=str(VARIABLES['FSH'])+VARIABLES['HL'][1]+VARIABLES['HL'][2]\
        +VARIABLES['HL'][3]+VARIABLES['HL'][4]+VARIABLES['HL'][5]+VARIABLES['HL'][6]
    VARIABLES['TSHH']=VARIABLES['HLL'][1]+VARIABLES['HLL'][2]+VARIABLES['HLL'][3]\
        +VARIABLES['HLL'][4]+VARIABLES['HLL'][5]+VARIABLES['HLL'][6]+VARIABLES['HLL'][7]\
        +VARIABLES['HLL'][8]+VARIABLES['HLL'][9] ## 11500
    ## AJ: ???, HD: ???, DT == FIRE DOOR
    if (VARIABLES['AJ']==4 and VARIABLES['HD']=="LH") or\
        (VARIABLES['DT']==A[55] and VARIABLES['HD']=="LH"):
        print()
        print("SLAT HOLES FROM LEFT:VARIABLES['TSH'] VARIABLES['TSHH']")
        print()
        print()
        return L11540_print_barrel_rings() ## 11510
    if (VARIABLES['AJ']==4 and VARIABLES['HD']=="RH") or\
        VARIABLES['DT']==A[55] and VARIABLES['HD']=="RH":
        print()
        print("SLAT HOLES FROM RIGHT: VARIABLES['TSH'] VARIABLES['TSHH']")
        print()
        print()
        return L11540_print_barrel_rings() ## 11520
    print("TOP SLAT HOLE LOCATIONS: VARIABLES['TSH'] VARIABLES['TSHH']")
    print() ## 11530
    return L11540_print_barrel_rings() ## Implicit

def L11540_print_barrel_rings():
    """ Outputs Barrel Ring Locations """
    print("BARREL RING LOCATIONS: VARIABLES['BRL'] VARIABLES['BRLL']")
    print()
    return ## 11540







def Main():
    L0_startup()