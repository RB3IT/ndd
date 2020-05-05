""" NewDadsDoor.calculations

    A collections of low-level formulas for calculating requirements and statistics related to doors.
    See NewDadsDoor.methods for higher-level functions involved in constructing doords,
    or NewDadsDoor.classes for Object-oriented Classes.

    Note that the prefixes used in this module combine Slats and Endlocks into the curtain prefix,
    and Assembly is included in the pipe prefix. Some Door Object attributes are located under other
    prefixes that are more relevant.
"""
## Builtin
import math
import functools

## This Module
from NewDadsDoor.constants import *

def bottombar_feederslatweight(slatweight, slatlength):
    """ Returns the weight of the feeder slat for a bottombar.
        
        slatweight is weight per inch of the slat used as a feeder
        slatlength is the length of the feeder slat
    """
    return slatweight * slatlength * .65

def bottombar_slopeweight(length, slope):
    """ Returns the weight added by the slopped portion of the bottom bar.
        
        length is the length of the bottombar(or slope area, though these should be identical).
        slope is difference between the short and long side of the bottombar.
    """
    slopereach =  slope + 3
    reachsquarearea = slopereach * (length  + 1)
    slopetrianglearea = slope * (length + 1) / 2
    diff_feet = (reachsquarearea - slopetrianglearea) / 144 * 5
    return diff_feet + (length + 1) * .05316

def curtain_finalradius(initialradius, turnstoraise, increaseradius):
    """ Final Lever Arm/Final distance from center of pipe to pipe centerline of curtain
    
        initialradius is distance from the center of the pipe to where the curtain attaches:
        this may be the pipe's shell or barrelrings if present.
        turnstoraise are the number of turns required to take the door from the closed to open
        position.
        increaseradius is how much the radius increases on each turn: often is the depth of the
        slat used.
    """
    return initialradius + (turnstoraise * increaseradius)

def curtain_getendlocks(slats, windlocks = 0):
        """ Returns a tuple of the number of (endlocks,windlocks) to be used on a given number of slats.
        
            slats are the number slats in the curtain.
            windlocks is the rate of windlocks per endlocks (i.e.- windlocks = 3 => 1 windlock every
            3rd slat; or 1 out of 3 endlocks are windlocks)
        """
        if slats == 0: return (0,0)
        if not windlocks:
            return (math.ceil(slats/2)*2,0)
        singleendlocks = math.ceil(slats/2)
        singlewindlocks = singleendlocks // windlocks
        return (singleendlocks * 2, singlewindlocks * 2)

def curtain_getendlockweight(slats, endlockweight, windlocks = False):
    """ Returns the endlock weight given the number of slats that have endlocks.
        
        slats is the number of slats.
        endlockweight is the weight of the endlocks being used.
        windlocks is the rate of windlocks per endlocks (i.e.- windlocks = 3 => 1 windlock every
        3rd slat; or 1 out of 3 endlocks are windlocks).
    """
    if slats == 0: return 0
    ## I dont particularly like this function, but this is how it was originally written in the source
    if windlocks:
        endlockweight = (((slats / windlocks) * .656) / slats ) + .17
    return slats * endlockweight * 2

def curtain_getwraplength(centerlineheight, totalradius, adjustratio = 0):
    """ Gets the calculated distance for the wrap, which is the section of the curtain
        spanning from the stopheight, over the top, and connecting to bottom of the pipe.
        
        centerlineheight is the distance from the stops to the pipe's centerline.
        totalradius is the overall radius of the pipe, including barrelrings; called
        initialradius in other formulae.
        adjustratio is an adjustment to the ratio of the circumference that the wrap
        covers. By default (adjustratio of 0), .66 of the circumference of the pipe is wrapped
        (starting from the pipe's centerline in front, and wrapping around to just past the back
        centerline). The adjustment can be up to .66, which would result in a 0% of the pipe being
        wrapped- ergo, the return will be identical to the centerlineheight supplied.
    """
    if 0 > adjustratio > .66: raise ValueError("adjustratio must be 0.0 .. 0.66 inclusive")

    return  2 * math.pi * totalradius * (.66 - adjustratio) + centerlineheight

def curtain_getwraplength_estimate(slatheight):
    """ Gets the calculated distance for the wrap, which is the section of the curtain
        spanning from the stopheight, over the top, and connecting to the rear centerline.

        This function only returns an estimate based on the WRAPLENGTH default value.
        
        slatheight should be the height of the slat being used for the wrap.
    """
    return WRAPLENGTH*slatheight

def curtain_openheight(pipe_centerline, stopheight, bottomheight):
    """ Returns the distance between the bottom of the curtain and the center of the bracket plates.

    pipe_centerline is the distance from the floor to the centerline of the pipe (generally, also
    height to the center of the shaft).
    stopheight is the height at which the Stops engage the bottom bar (or other stop)
    """
    return pipe_centerline - stopheight + bottomheight

def curtain_perforatedweightloss(slatweight, perforations, slats):
    """ Calculates the amount of weight lost to perforations in a curtain.

        slatweight is the weight of the slat per inch length.
        perforations are the number of perforation in the slat.
        slats are the number of slats with perforations in them.
    """
    ## (Slat Weight per Window-size) * Weight Loss Per Window *  Number of perforations/Slat * Number of Slats
    return (slatweight/5.25) * 4.648175 * perforations * slats

def curtain_perforationsperslat(slatlength):
    """ Determine number of perforation Windows based on Curtain Width
        
        slatlength should be the length of the slat.

        Calculated as 1-Window/8.5 inches, minus 2 windows (one on each end near the guides).
    """
    ## Windows every 8.5 Inches, skip first and last window
    ## This calculation is from the original, but I would probably like it
    ## better written "(slatlength - edgepadding)/8.5" so that the distance
    ## from the edge can be customized (as opposed to being 8.5)
    return max(slatlength/8.5 - 2,0)

def curtain_slatlength(clearopening_width, slattype= None, endlocks = None, windlocks = False, tracks = None):
    """ Calculates the appropriate length of slats with the given specifications covering a given opening.
       
        clearopening_width is the width of the opening being closed.
        slattype is the type of slat being used.
        endlocks is the type of endlock being used (if at all).
        windlocks is a boolean indicating whether windlocks are used.
        tracks is the type of tracks being used.
    """
    clow = clearopening_width


    ## NOTE: Original method is not really followed at this point, so the new method is being used
    length = clow + 4.25
    if endlocks:
        if "CAST" in endlocks:
            length -= .5
            if "WINDLOCKS" in endlocks: length -= 1
    return length

    ## TODO Create FireDoorSection Subclass
    length = clow
    if not endlocks:
        if slattype in ["3 5/8 INCH CROWN SLAT","2 7/8 INCH CROWN SLAT"]: length += 1
        elif slattype == "2 1/2 INCH FLAT SLAT": length += .25
    if endlocks == "CAST IRON" and slattype == "2 1/2 INCH FLAT SLAT":
        length -= .5

    if tracks == "Extruded Guides":
        return length + 2.5
    if slattype in ["3 5/8 INCH CROWN SLAT","2 7/8 INCH CROWN SLAT"]:
        if not endlocks and windlocks:
            if clow < 149: return length + 3.5
            if clow <=221: return length + 3.875
    if slattype == "2 7/8 INCH CROWN SLAT":
        if endlocks and windlocks:
            if clow < 293: return length + 3.875
            return length + 4.875
    if tracks != "Extruded Guides":
        if clow < 149: return length + 3.5
        if clow < 221: return length + 3.875
        if clow < 293: return length + 4.5
        if clow <= 365: return length + 5.5
    if slattype == "2 1/2 INCH FLAT SLAT":
        if not endlocks and windlocks:
            if clow < 149: return length + 4.25
            if clow < 197: return length + 4.625
        else:
            if clow < 293: return length + 4
            return length + 5
    if slattype == "MIDGET CROWN SLAT < 2 INCH >":
        if clow < 149: return length + 3.75
        return length + 4.125
    return length

def curtain_slatlength_perforatedslats(clearopening_width, slattype= None, endlocks = None, windlocks = False, tracks = None):
    """ Calculates the appropriate length of slats with the given specifications covering a given opening specifically for Perforated Slats.
       
        clearopening_width is the width of the opening being closed.
        slattype is the type of slat being used.
        endlocks is the type of endlock being used (if at all).
        windlocks is a boolean indicating whether windlocks are used.
        tracks is the type of tracks being used.

        Uses curtain_slatlength to get a base length.
    """
    ## TODO Create FireDoorSection Subclass
    clow = clearopening_width
    length = curtain_slatlength(clearopening_width, slattype= slattype, endlocks = endlocks, windlocks = windlocks, tracks = tracks)
    if isinstance(tracks,ExtrudedGuides):
        return length
    if not windlocks:
        if clow <= 149: return length + 3.875
        if clow < 264: return length + 4.25
    else:
        if clow <= 293: return length + 4
        return length + 5
    ## This line was added. Reached via No Windlocks and clow >= 264
    ## TODO: double check original code for how this was supposed to be handled
    return length

def door_turnstoraise(stopheight, totalradius, increaseradius): ## TR
    """ Number of Barrel Rotations required to fully raise the door (TR)

    stopheight is the distance from the floor to where the stops engage the bottom of the curtain.
    totalradius is the radius of the pipe, including barrelrings if present.
    increaseradius is how much the radius increases on each turn: often is the depth of the
    slat used.

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
    stopheight = float(stopheight)
    totalradius = float(totalradius)
    increaseradius = float(increaseradius)
    ## A: Extra Circumference each Turn
    A = math.pi * increaseradius
    ## B: Base Circumference each Turn (per Pipe)
    B = 2 * math.pi * totalradius
    ## C: Stop Height
    C = -stopheight
    ## Solve quadratic
    return (-B + math.sqrt(B**2 - 4*A*C)) / (2*A)

def pipe_centerlineheight(stopheight, stopsize, upset, bracketplate_holeheight): ## HC
    """ Height from the floor to the center of the Pipe.
       
        stopheight is the distance from the floor to where the stops engage the bottom of the curtain.
        stopsize is the size of the stops
        upset is additional spacing between the top of the stops and the bracketplates.
        bracketplate_holeheight is the distance from the bottom of the bracketplate to the hole through
        which the shaft is placed. This is almost always center to the bracketplate (and therefore half
        the bracketplate height).
    """
    return stopheight + stopsize + upset + bracketplate_holeheight

def pipe_maxdeflectionweight(I4, pipewidth):
    """ Amount of weight that the pipe can support without bending

    I4 is the I4 rating of the pipe (unknown alias).
    pipewidth is the width of the pipe in inches.

    This equation was taken as-is from the source code; its origins could not
    be found the handbook.
    """
    ## I4 / Width-in-feet^2 * 38667
    return I4 / (pipewidth/12) ** 2 * 38667

def pipe_preturns(requiredtorque_open, torqueperturn): ## PT
    """ Number of turns required in order to achieve requiredtorque_open

        requiredtorque_open is the amount of torque required to hold the curtain open.
        torqueperturn is the torque required for each turn.
    """
    preturns = requiredtorque_open / torqueperturn 
    ## Round to nearest 1/6 turn
    whole = math.floor(preturns)
    deci = preturns - whole
    return whole + round(6*deci) / 6

def pipe_requiredtorque_closed(initialradius, hangingweight_closed): ## TD
    """ Required amount of force required to lift door when closed.
        
        initialradius is distance from the center of the pipe to where the curtain attaches:
        this may be the pipe's shell or barrelrings if present.
        hangingweight_closed is the weight of the curtain in the closed position.
    """
    return initialradius * hangingweight_closed

def pipe_requiredtorque_open(finalradius, hangingweight_open): ## TU
    """ Required amount of force required to hold the door open.
        
        finalradius is distance from the center of the pipe to furthest point of the coil
        (portion of the curtain that is wrapped around the pipe) while in the open position.
        hangingweight_open is the weight of the curtain in the open position.
    """
    return finalradius * hangingweight_open

def pipe_torqueperturn(requiredtorque_closed, requiredtorque_open, turnstoraise): ## IP
    """ The amount of torque (inch/pound) for each turn (IPPT in handbook)
        
    Handbook notes this should be rounded up to nearest 1/8.
    requiredtorque_closed is the required amount of force required to lift door while closed.
    requiredtorque_open is the required amount of force required to hold the door open.
    turnstoraise are the number of Barrel Rotations required to fully raise the door.
    """
    return rounduptofraction(
        (requiredtorque_closed - requiredtorque_open) / turnstoraise,
        1/8)

def pipe_totalturns(turnstoraise, preturns): ## TT
    """ Total number of time the pipe will be turned
    
        turnstoraise are the number of Barrel Rotations required to fully raise the door.
        preturns are the number of turns required in order to achieve requiredtorque_open.
        
        While this equation is extremely simple, it is kept separate simply due to how often
        it is used and in case in needs to be modified (e.g.- with a safety factor)
    """
    return turnstoraise + preturns

def tracks_wall_length(stopheight, upset, bracketplate_size):
    """ Returns the necessary height to cover the openheight, stops, upset, and Bracket Plates.
       
        stopheight is the distance from the floor to where the stops engage the bottom of the curtain.
        upset is additional spacing between the stops and the bracketplates.
        bracketplate_size is the height of the bracketplate (bracketplates are almost always
        square, so this is generally just the bracketplate's size).
    """
    return stopheight + upset + bracketplate_size

def safetyfactor_curtain_hangingweight_open(weight, stopheight = 0):
    """ Weight of the Curtain when the door is Open adjusted for safety
        
        weight is the weight of the hanging portion of the curtain when open (obtained from curtain_hangingweight_open)
        stopheight is the distance between the bottom of the curtain when open and the floor.
    """
    weight = float(weight)
    stopheight = float(stopheight)
    if stopheight >=192: return weight * 1.2
    if stopheight < 50: return weight + 5
    #if 50 < stopheight < 100: return weight + 10
    return weight * 1.1

def validation_pipesize(pipeweight, curtainweight, maxdeflection, safetyfactor = .97):
    """ Validates that the weight of the pipe and curtain does not exceed the deflection of the pipe with added safety factor.

        pipeweight should be the entire weight of the pipe.
        curtainweight should be the weight of the curtain while the door is closed
        (the pipe is supporting the most weight on it's lever arm).
        maxdeflection is the maximum deflection rating of the pipe.
        safetyfactor is a ratio of the maxdeflection. safetyfactor should not be heigher than the default.
    """
    if 0 > safetyfactor > .97: raise ValueError("Invalid safetyfactor")
    return pipeweight + curtainweight <= maxdeflection * safetyfactor