## Builtin
import re


## Line Number Reader
"""Captures Line number and the rest of the line """
LINENUMBERREADER = re.compile(
    """
    (?P<number>\d+) # Line Number
    \ (?P<line>.*) # Rest of the Line
    """,
    re.VERBOSE)

## Commented Line Number Reader
""" Captures the line number from a comment at the end of the line """
COMMENTLINENUMBERREADER = re.compile(
    """
    (?P<line>.*) # Rest of the Line
    \#\#\ # Comment indicator
    (?P<linenumber>\d+) # Line Number
    """,
    re.VERBOSE)

## DATA Line Reader
""" Captures the rest of the line after the Line Number and DATA """
DATAREADER = re.compile(
    """
    \d+ # Line Number (not captured)
    \ DATA\ # DATA string literal (not captured)
    (?P<data>.*) # Actual Data Variables
    """,
    re.VERBOSE)

## Fork Finder
""" Identifies a "GOTO" statement at the end of the line
Note: GOTO statements should always be at the end of the line, but we'll be explicit
for the heck of it.
This regex also accepts lines that have been reordered with reformatliens()"""
FORKFINDER = re.compile(
    """
    (?P<linenumber>\d+ )? # Optional Line Number
    (?P<line>$.*) # Line Content
    \ GOTO\ # GOTO string literal (not captured)
    (?P<dest>\d+) # Line to GOTO
    (?P<endlinenumber> \(\d+\))? # Optional line-number at end""",
    re.IGNORECASE | re.VERBOSE)

def relocatelinenumbers(code):
    """ Takes Basic code, removes the linenumber from the beginning of the line, and adds it as a comment to the end.

    code should start with a linestring which begins with a line number. It can contain any number of linestrings joined with \n.
    Returns a string of \n-joined linestrings.
    """
    out = []
    for line in code.split('\n'):
        ## See regex above
        linereader = LINENUMBERREADER.match(line.strip()).groupdict()
        ## Add formatted string to output
        out.append(f"{linereader['content']} ## {linereader['number']}")
    return "\n".join(out)

def groupfunctions(code):
    """Finds where the coade forks (GOTO statements) and inserts a newline character.

    code should a string that can be a single line or a number of lines joined with \n.
    This is to help group runs of code into "functions" as GOTO is an implicit return.
    Note that this implementation has the unfortunate side-effect of splitting
    if-then-goto trees.
    """
    out = []
    for line in code.split("\n"):
        ## See regex above
        if FORKFINDER.match(line):
            ## If regex matches, add blank line
            line+="\n"
        out.append(line)
    return "\n".join(out)

def adataparser(datastring):
    """ A quick function I made for parsing a string containing the A$ DATA assignments into a dicitonary with index keys.
    
    datastring is a rawstring copied out of program (it is formatted "DATA blah,blah blah\nDATA blah,[...etc]").
    Returns a dicitonary with each of the data items as the value for their Variable index key (Note: Basic starts at 1, so
    output[0] is not assigned; the first DATA variable is out[1] instead of out[0]).
    In other words, "DIM A$(4):DATA A,B,C,D:FOR X=1 TO 4:READ A$(X):NEXT X" gets converted to A=dict(0=None,1="A",2="B",
    3="C",4="D")
    Obviously, this is DATA agnostic so it can be used with other such DATA-assignment structures
    """
    out = []
    for line in datastring.split("\n"):
        ## See regex above
        data = DATAREADER.match(line).group("data")
        ## Convert to individual values and remove whitespace
        ## We're stripping whitespcae separately instead of just splitting with whitespace in
        ## case of whitespace inconsistency
        data = [value.strip() for value in data.split(",")]
        ## add to output
        out.extend(data)
    return dict(enumerate(out))
        
if __name__ == "__main__":
    #FILE = "DADSDOOR.BAS"
    #lines = reformatlines(FILE)
    #print("\n".join(lines))

    datastring = """310 DATA <1>  CURTAIN TYPE,<2>  GAGE,<3>  ASTRAGAL,<4>  SAFETY EDGE
320 DATA <5>  BOTTOM BAR,<6>  UPSET,<7>  WINDLOCKS,<8>  SPRINGS,<9>  ENDLOCKS
330 DATA <10> SLOPE,<11> PIPE & RINGS,<12> ADJUSTER
340 DATA <13> BRACKET PLATE,PASS DOOR,<15> NO OTHER OPTIONS
350 DATA ALUMINUM T TYPE (BBX-C),1 1/2" x 1 1/2" x 1/8" (STL),2 1/2" x 2" x 3/16" (STL)
360 DATA 3" x 2" x 3/16" (STEEL),2" x 2" x 1/8" (ALUM.),<1> 25000,<2> 50000,<3> 100000
370 DATA <4> MAXIMUM POSSIBLE CYCLES,<1> CONT. STAMPED STEEL,<2> ALT. CAST IRON
380 DATA <3> CONTINUOUS CAST IRON,<1> INSIDE ADJUSTER,<2> THRU-SHAFT
390 DATA <1> 3 5/8 INCH CROWN SLAT,<2> 2 7/8 INCH CROWN SLAT
400 DATA <3> 2 1/2 INCH FLAT SLAT,INSULATED DOUBLE SLAT <2 3/4>
410 DATA <1> SMALLEST POSSIBLE BRACKETS,<2> LARGER THAN STD. BRACKETS
420 DATA <1> 22 GAGE,<2> 20 GAGE,<3> 18 GAGE,<4> 16 GAGE,SLATS
430 DATA 4 INCH TUBE, 4 INCH PIPE, 6 INCH TUBE,6 INCH PIPE,8 INCH PIPE
440 DATA 10 INCH PIPE,12 INCH PIPE,14 INCH <30> PIPE,14 INCH <40> PIPE
450 DATA 16 INCH <30> PIPE,16 INCH <40> PIPE,<5> ALUMINUM GRILLE
460 DATA SERVICE DOOR, WEATHERTITE DOOR,FIRE DOOR,ROLLING GRILLE,COUNTER SHUTTER,FIRE SHUTTER
470 DATA INSULATED DOOR,FACE MOUNTED,EXTERIOR MOUNTED,BETWEEN JAMBS
480 DATA CHAIN OPERATED,MOTOR OPERATED,HAND LIFT,CRANK OPERATED,GALV. STEEL
490 DATA PRIME PAINTED,MILL ALUMINUM,ALUM. LINKS/PLASTIC TUBES
500 DATA ANODIZED ALUMINUM,DURANODIC ALUMINUM,STAINLESS STEEL
510 DATA <4> MIDGET CROWN SLAT < 2 INCH >,EXTERIOR THRU-WALL
520 DATA <7> VISION SECTION <GRILLE>,RETURN TO MAIN MENU,MOTOR (BY OTHERS),PERFORATED SLATS,!!!!!!!!!! PARAMETER OVERIDE !!!!!!!!!!
530 DATA STANDARD TUBULAR ALUMINUM, LARGE TUBULAR ALUMINUM
540 DATA 2" x 2" x 1/8" STEEL, STIFFENER, OVERSIZE, 3" x 2" x 3/16" ALUMINUM
550 DATA 2 1/2" x 2 1/2" x 1/8" (ALUM.) ,ELECTRIC (Miller Edge),PNEAUMATIC (Air)
560 DATA LEXAN INSERTS"""
    print(adataparser(datastring))