##  FOREGROUND and BACKGROUND COLORS SUB-ROUTINE (140)
COLOR 0,14:RETURN: REM BLACK ON YELLOW (210)
    
    
##  FUNCTION KEY F10 (260)
SYSTEM (280)
    
GOSUB 170:BEEP : print(" NUMBER MUST BE 5 DIGITS ": GOSUB 150:GoTo 740 (750)
input("MARK ";VARIABLES['MK']:print( (760)
input("DOOR MODEL CODE:";VARIABLES['DM']:print( (770)
DM=LEN(VARIABLES['DM']):If DM = 5 or VARIABLES['MID'](VARIABLES['DM'], 3, 3) = "(M)" : return 810 (780)

GOSUB 170:BEEP : print(" INCOMPLETE MODEL CODE ": GOSUB 150:GoTo 770 (790)

GOSUB 170:BEEP : print(" CAPS LOCK MUST BE ON ": GOSUB 150:GoTo 770 (800)

VARIABLES['DT']=VARIABLES['LEFT'](VARIABLES['DM'],1):VARIABLES['MT'] = VARIABLES['MID'](VARIABLES['DM'], 2, 1) : VARIABLES['OP'] = VARIABLES['MID'](VARIABLES['DM'], 3, 1) : VARIABLES['MF'] = VARIABLES['RIGHT'](VARIABLES['DM'], 2) (810)
if DM=7 : VARIABLES['OP']=VARIABLES['MID'](VARIABLES['DM'],3,3) (820)
if ASC(VARIABLES['DT'])>=97 : return 800 (830)

if VARIABLES['DT']="S"Or VARIABLES['DT']="W"Or VARIABLES['DT']="U"Or VARIABLES['DT']="T"Or VARIABLES['DT']="G"Or VARIABLES['DT']="C"Or VARIABLES['DT']="L" : return 860 (840)

return 920 (850)

if VARIABLES['MT']="F" or VARIABLES['MT']="B" or VARIABLES['MT']="X" or VARIABLES['MT']="T" : return 880 (860)

return 920 (870)

if VARIABLES['OP']="M" or VARIABLES['OP']="(M)" or VARIABLES['OP']="C" or VARIABLES['OP']="H" or VARIABLES['OP']="K" : return 900 (880)

return 920 (890)

if VARIABLES['MF']="GS"Or VARIABLES['MF']="PP"Or VARIABLES['MF']="SS"Or VARIABLES['MF']="MA"Or VARIABLES['MF']="AA"Or VARIABLES['MF']="DA" : return 930 (900)

if VARIABLES['MF']="AP" or VARIABLES['MF']="ML" or VARIABLES['MF']="DL" or VARIABLES['MF']="AL" : return 930 (910)

GOSUB 170:BEEP : print(" INCORRECT DOOR MODEL CODE ": GOSUB 150:GoTo 770 (920)

if VARIABLES['DT']="S" : VARIABLES['DT']=A[53]:TS = 2 : HS = 2.875 : IR = 0.6 (930)
if VARIABLES['DT']="W" : VARIABLES['DT']=A[54]:TS = 3 : HS = 2.625 : IR = 0.715 : AS=.5 (940)
if VARIABLES['DT']="G" : VARIABLES['DT']=A[56]:TS = 5 : RS = 2.25 : IR = 0.815 (950)
if VARIABLES['DT']="U" : VARIABLES['DT']=A[55] (960)
if VARIABLES['DT']="T" : VARIABLES['DT']=A[59]:TS = 6 : HS = 2.5 : IR = 0.82 : SW = 0.07388854 : VARIABLES['SG'] = "22/22" (970)
if VARIABLES['DT']="C" or VARIABLES['DT']="L" : return 990 else: return 1020 (980)

if VARIABLES['DT']="C" : VARIABLES['DT']=A[57]:GoTo 1010 (990)

if VARIABLES['DT']="L" : VARIABLES['DT']=A[58]:GoTo 1010 (1000)

GOSUB 170:BEEP : print(" Not PROGRAMMED FOR "VARIABLES['DT']" ": print(" PROGRAME EXECUTION HALTED! ": print(" PRESS <F2> TO START OVER ": GOSUB 150:End (1010)
print( VARIABLES['DT'] (1020)
if VARIABLES['MT']="F" : VARIABLES['MT']=A[60] (1030)
if VARIABLES['MT']="X" : VARIABLES['MT']=A[61] (1040)
if VARIABLES['MT']="B" : VARIABLES['MT']=A[62] (1050)
if VARIABLES['MT']="T" : VARIABLES['MT']=A[75] (1060)
print( VARIABLES['MT'] (1070)
if VARIABLES['OP']="C" : VARIABLES['OP']=A[63] (1080)
if VARIABLES['OP']="M" : VARIABLES['OP']=A[64] (1090)
if VARIABLES['OP']="(M)" : VARIABLES['OP']=A[78] (1100)
if VARIABLES['OP']="H" : VARIABLES['OP']=A[65] (1110)
if VARIABLES['OP']="K" : VARIABLES['OP']=A[66] (1120)
print( VARIABLES['OP'] (1130)
if VARIABLES['MF']="GS" : VARIABLES['MF']=A[67] (1140)
if VARIABLES['MF']="PP" and Not VARIABLES['DT']="INSULATED DOOR" : VARIABLES['MF']=A[68] (1150)
if VARIABLES['MF']="PP" and VARIABLES['DT']="INSULATED DOOR" : VARIABLES['MF']=A[68]:SW = 0.07388854 : VARIABLES['SG'] = "20/24 PP" (1160)
if VARIABLES['MF']="MA" : VARIABLES['MF']=A[69] (1170)
if VARIABLES['MF']="AP" : VARIABLES['MF']=A[70] (1180)
if VARIABLES['MF']="AA" : VARIABLES['MF']=A[71] (1190)
if VARIABLES['MF']="DA" : VARIABLES['MF']=A[72] (1200)
if VARIABLES['MF']="SS" : VARIABLES['MF']=A[73] (1210)
if VARIABLES['MF']="ML" : VARIABLES['MF']=A[69]+" "+A[90]:RS = 3 (1220)
if VARIABLES['MF']="AL" : VARIABLES['MF']=A[71]+" "+A[90]:RS = 3 (1230)
if VARIABLES['MF']="DL" : VARIABLES['MF']=A[72]+" "+A[90]:RS = 3 (1240)
print( VARIABLES['MF']:print( (1250)
input("HAND (RH=RIGHT LH=LEFT) ";VARIABLES['HD']:print( (1260)
if VARIABLES['HD']="LH" or VARIABLES['HD']="RH" : return 1280 else: BEEP:GoTo 1260 (1270)

input("MOUNT ANGLE STYLE (E or Z or F) ";VARIABLES['MA']:print( : if VARIABLES['MA'] = "Z" or VARIABLES['MA'] = "E" or VARIABLES['MA'] = "F" : return 1290 else: BEEP:GoTo 1280 (1280)

input("CUSTOMER ";VARIABLES['C']:print( (1290)
input("PROJECT ";VARIABLES['PJ']:print( (1300)
if TS=5 and VARIABLES['MT']=A[62] : return 1320 else: return 1440 (1310)

CLS:GOSUB 160:print(" ***** SELECT BETWEEN JAMB MOUNT ***** ": GOSUB 150 (1320)
print("<1> MOUNTING BETWEEN SUPPORT TUBES (EXTRUDED ALUMINUM GUIDES)":print( : print("<2> MOUNTING BETWEEN SUPPORT TUBES (STEEL GUIDES)": print( (1330)
print("<3> MOUNTING BETWEEN JAMBS (WALLS)":print( : print( : print( (1340)
input("SELECT BETWEEN JAMB STYLE ";VARIABLES['BJT']:If VAL(VARIABLES['BJT']) <= 3 : return 1360 else: BEEP:GoTo 1350 (1350)

if VAL(VARIABLES['BJT'])<=2 : CLS:GOSUB 160:print(" *** SUPPORT TUBES *** ": GOSUB 150 (1360)
if VARIABLES['BJT']="3" : print(:GoTo 1440 (1370)

print(:print("<1>  3"VARIABLES['I']" x 3"VARIABLES['I']: print( : print("<2>  4"VARIABLES['I']" x 4"VARIABLES['I']: print( : print( : print( : input("SUPPORT TUBES";VARIABLES['STS'] (1380)
if VAL(VARIABLES['STS'])<=2 : return 1400 else: BEEP:GoTo 1360 (1390)

if VARIABLES['STS']="1" : VARIABLES['STS']="3 x 3 SUPPORT TUBES" else: VARIABLES['STS']="4 x 4 SUPPORT TUBES" (1400)
print(:GOSUB 160:print( VARIABLES['STS'] : GOSUB 150 (1410)
if VARIABLES['BJT']="2" : print(:GoTo 1440 (1420)

print(:INPUT"WIDTH BETWEEN SUPPORT TUBES (Feet,Inches)";FF, VARIABLES['FI']: return 1450 (1430)

input("CLEAR WIDTH (FEET,INCHES) ";FF,VARIABLES['FI'] (1440)
if FF<=1 or FF>=99 : return 1530 (1450)

VARIABLES['Q']=VARIABLES['LEFT'](VARIABLES['FI'],2):Q = VAL(VARIABLES['Q']) : if Q >= 12 : return 1530 (1460)

if LEN(VARIABLES['FI'])=3 or LEN(VARIABLES['FI'])=4 or LEN(VARIABLES['FI'])=7 : return 1530 (1470)

if LEN(VARIABLES['FI'])<=2 : IN=VAL(VARIABLES['FI']):GoTo 1500 (1480)

if LEN(VARIABLES['FI'])>=3 : return 1510 (1490)

CW=(FF*12)+DC+IN:GoTo 1540 (1500)

VARIABLES['X']=VARIABLES['RIGHT'](VARIABLES['FI'],3):VARIABLES['Y'] = VARIABLES['LEFT'](VARIABLES['X'], 1) : VARIABLES['Z'] = VARIABLES['RIGHT'](VARIABLES['X'], 1) : D = VAL(VARIABLES['Y']) : C = VAL(VARIABLES['Z']) (1510)
DC=D/C:L1 = LEN(VARIABLES['FI']) : L2 = LEN(VARIABLES['X']) : L = L1 - L2 : VARIABLES['IN'] = VARIABLES['LEFT'](VARIABLES['FI'], L) : IN=VAL(VARIABLES['IN']):GoTo 1500 (1520)

BEEP:If VARIABLES['MT'] =A[62] : return 1430 else: return 1440 (1530)

if VARIABLES['DT']=A[55] and CW>240 : BEEP:print( : GOSUB 170:print(" MAXIMUM WIDTH FOR "A[55]" Is 20 ft. - 0"VARIABLES['I']" ":GOSUB 150:CW = 0 : IN=0:DC = 0 : return 1440 (1540)

if VARIABLES['DT']=A[54] and CW>360 : BEEP:print( : GOSUB 170:print(" MAXIMUM WIDTH FOR "A[54]" Is 30 ft. - 6"VARIABLES['I']" ":GOSUB 150:CW = 0 : IN=0:DC = 0 : return 1440 (1550)

if VARIABLES['MT']=A[62] and VARIABLES['BJT']="1" : print("("CW" INCHES BETWEEN TUBES )":GoTo 1580 (1560)

print("("CW" INCHES CLEAR DOOR WIDTH )" (1570)

def L1580_update_stop_height():
    """ Updates the stop height"""
    print()
    ## Need to parse this input
    sh = input("STOP HEIGHT (FEET,INCHES) ")
    VARIABLES['HF'], VARIABLES['HI'] = sh.split(',')
    VARIABLES['HF'] = int(VARIABLES['HF']) ## 1580
        
    if VARIABLES['HF']<=1 or VARIABLES['HF']>=99:
        "BEEP"
        return L1580_update_stop_height() ## 1590

    if LEN(VARIABLES['HI'])==3 or LEN(VARIABLES['HI'])==4 or LEN(VARIABLES['HI'])>=7:
        "BEEP"
        return L1580_update_stop_height() ## 1600

    VARIABLES['Q'] = VARIABLES['HI'][:2]
    VARIABLES['Q'] = int(VARIABLES['Q'])
    if VARIABLES['Q'] >= 12:
        "BEEP"
        return L1580_update_stop_height() ## 1610

    ## This next part seems to be handling Fractions (5'3-1/2")
    if LEN(VARIABLES['HI'])<=2:
        VARIABLES['IN'] = int(VARIABLES['HI'])
        VARIABLES['DC'] = 0 ## 1620
    if LEN(VARIABLES['HI'])>=3:
        return L1650_parsefraction() ## 1630
    return L1650_parsefraction()

def L1640_set_stopheight():
    """ Sets the stop height variable and validates the result """
    VARIABLES['SH']=VARIABLES['HF']*12+VARIABLES['DC']+VARIABLES['IN']
    return L1680_validate_stopheight() ## 1640

def L1650_parsefraction():
    """ As best as I can figure, this is a function for parsing fractions into decimals """
    VARIABLES['X'] = VARIABLES['HI'][-3:]
    ## Numerator and Denominaor
    ## I'm assuming that we go D/C simply because DC is short for Decimal
    VARIABLES['Y'] = VARIABLES['X'][:1]
    VARIABLES['Z'] = VARIABLES['X'][-1]
    VARIABLES['D'] = int(VARIABLES['Y'])
    VARIABLES['C'] = int(VARIABLES['Z']) ## 1650
    VARIABLES['DC'] = D / C
    VARIABLES['L1'] = len(VARIABLES['HI'])
    VARIABLES['L2'] = len(VARIABLES['X'])
    VARIABLES['L'] = L1 - L2
    ## Whole number from the mixed
    VARIABLES['IN'] = VARIABLES['HI'][L:]
    VARIABLES['IN'] = int(VARIABLES['IN']) ## 1660
    return L1640_set_stopheight() ## 1670

def L1680_validate_stopheight():
    """ Makes sure that the stopheight is below 168 inches for Fire Doors """
    ## DT == FIRE DOOR
    if VARIABLES['DT']==A[55] and VARIABLES['SH']>168:
        "BEEP"
        print()
        L170_brightwhiteonredtext()
        print("""" MAXIMUM HEIGHT FOR A[55] Is 14 ft. - 0" """)
        L150_yellowonblacktext()
        ## Reset Stop Height variables
        ## I don't know why we don't reset HF as well
        VARIABLES['SH'] = 0
        VARIABLES['IN']=0
        VARIABLES['DC'] = 0
        return L1580_update_stop_height() ## 1680

    print("(VARIABLES['SH'] INCHES TO STOPS)") ## 1690
    ## DT != FIRE DOOR
    if VARIABLES['DT']!=A[55]:
        return L1720_validate_stopheight_check_sebb() ## 1700

    if VARIABLES['CW']>144 or VARIABLES['SH']>144 or ((VARIABLES['CW']*VARIABLES['SH'])/144)>120:
        "BEEP"
        L180_yellowonred()
        "LOCATE 23, 40"
        print( " A[85] A[55] ")
        ## OVERSIZE FIRE DOOR
        L150_yellowonblacktext() ## 1710
        ## This function seems to implicitly roll into L1720
        return L1720_validate_stopheight_check_sebb()

def L1720_validate_stopheight_check_sebb():
    """ Checks if the door has a Safety Edge Bottom Bar """
    if VARIABLES['SEBB']=="":
        return L1730_validate_stopheight_check_addsh()
    else:
        return 3100 ## 1720

def L1730_validate_stopheight_check_addsh():
    if VARIABLES['ADDSH']=="":
        return L1740_validate_stopheight_check_SD1()
    else:
        return 3680 ## 1730

def L1740_validate_stopheight_check_SD1():
    if VARIABLES['SD1']==0 :
        return L1750_validate_stopheight_check_TS()
    else:
        return 290 ## 1740

def L1750_validate_stopheight_check_TS():
    if VARIABLES['TS']==5 :
        print()
        VARIABLES['GP'] = input("GRILLE PATTERN (ASL or CSL)")
        return L1770_validate_stopheight_check_gp() ## 1750
    return 1860 ## 1760

def L1770_validate_stopheight_check_gp():
    if VARIABLES['GP'] in ["ASL","CSL"]:
        return L1790_validate_stopheight_check_BJT() ## 1770
    "BEEP"
    return L1720_validate_stopheight_check_sebb() ## 1780

def L1790_validate_stopheight_check_BJT():
    if INT(VARIABLES['BJT'])==2:
        VARIABLES['EG']="N"
        VARIABLES['SM'] = "N"
        return L3140_print_bottombar_intro() ## 1790
    return L1800_validate_stopheight_check_BJT_2() ## Implicit

def L1800_validate_stopheight_check_BJT_2():
    """ Second half of L1790 (due to loop at 1840) """
    if VARIABLES['TS']==5:
        print()
        VARIABLES['EG'] = input("EXTRUDED GUIDES")
        VARIABLES['SM'] = "N" ## 1800
    if VARIABLES['EG']=="Y":
        print()
        L160_whiteonbluetext()
        print(" EXTRUDED ALUMINUM GUIDES ")
        L150_yellowonblacktext() ## 1810
    if VARIABLES['BJT']=="1":
        VARIABLES['CW']=VARIABLES['CW']-5
        return L1850_update_DD_CW() ## 1820

    if VARIABLES['BJT']!="":
        return L1850_update_DD_CW()
    else:
        return L3140_print_bottombar_intro() ## 1830
    "BEEP"
    return L1800_validate_stopheight_check_BJT_2() ## 1840

def L1850_update_DD_CW():
    format_float_as_measurement("CW")
    print()
    L160_whiteonbluetext()
    print(VARIABLES['CW']+" CLEAR WIDTH BETWEEN EXTRUDED GUIDE ")
    L150_yellowonblacktext()
    L110_rundelay()
    return L3140_print_bottombar_intro() ## 1850

def L3040_add_miller_edge_safety():
    """ Adds Miller Edge Safety Edge """
    print()
    L230_redonwhitetext()
    "BEEP"
    print(' REQUIRES A MINIMUM OF 2" UPSET PLUS 2" SHOULD BE ADDED TO STOP HEIGHT ')
    L150_yellowonblacktext()
    VARIABLES['SE']=.6
    VARIABLES['SEBB']=A[88]
    return L3070_ask_update_stop_height() ## 3040

def L3070_ask_update_stop_height():
    print()
    L160_whiteonbluetext()
    VARIABLES['ANS'] = input("DO YOU WISH TO CHANGE STOP HEIGHT")
    L150_yellowonblacktext() ## 3070

    if VARIABLES['ANS']=="Y":
        return L1580_update_stop_height() ## 3080

    if VARIABLES['ANS']=="N":
        return L3110_print_upset_added()
    else:
        "BEEP"
        return L3070_ask_update_stop_height() ## 3090

def L3100_print_safetyedge():
    """ Prints out Safety Edge """
    print()
    L160_whiteonbluetext()
    print("VARIABLES['SEBB'] SAFETY EDGE ")
    L150_yellowonblacktext()
    return L3110_print_upset_added() ## 3100
    
def L3110_print_upset_added():
    """ Prints out Upset Added """
    "BEEP"
    print()
    L170_brightwhiteonredtext()
    print(""" MINIMUM 2" UPSET ADDED """)
    VARIABLES["U"]="2"
    L150_yellowonblacktext() ## 3110
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3120

def L3140_print_bottombar_intro():
    """ Prints the Bottom Bar heading and resets LTBB """
    "CLS"
    print()
    L160_whiteonbluetext()
    print(" ******** SELECT BOTTOM BAR OPTION ******** ")
    L150_yellowonblacktext()
    "LOCATE 2,45"
    print()
    print()
    VARIABLES['LTBB']=0
    return L3160_get_bottombar() ## 3140

def L3150_bottombar_validation_error():
    """ Shows an error when selecting the bottom bar """
    "BEEP"
    VARIABLES['BO']=0
    L170_brightwhiteonredtext()
    print(" NOT AVAILABLE ON VARIABLES['DT'] or OPENING TOO WIDE  ")
    L150_yellowonblacktext()
    L110_rundelay()
    return L3140_print_bottombar_intro() ## 3150

def L3160_get_bottombar():
    """ Displays Bottom Bar options and forks response """
    print("< 1> A[16]")
    print()
    print("< 2> A[17]")
    print()
    print("< 3> A[18]")
    print()
    print("< 4> A[19]")
    print() ## 3160
    ## < 1> ALUMINUM T TYPE (BBX-C)
    ##
    ## < 2> 1 1/2" x 1 1/2" x 1/8" (STL)
    ##
    ## < 3> 2 1/2" x 2" x 3/16" (STL)
    ##
    ## < 4> 3" x 2" x 3/16" (STEEL)
    print("< 5> A[20]")
    print()
    print("< 6> A[87] <<< For Extruded Guides with Slide Bolts") ## 3170
    print()
    print( "< 7> A[81][-16:]")
    print()
    ## < 5> 2" x 2" x 1/8" (ALUM.)
    ## 
    ## < 6> 2 1/2" x 2 1/2" x 1/8" (ALUM.)
    ##
    ## < 7> TUBULAR ALUMINUM
    ##
    print( "< 8> A[86]") ## 3180
    print()
    print( "< 9> OTHER")
    print()
    print( "<10> A[77]")
    print()
    print() ## 3190
    ## < 8> 3" x 2" x 3/16" ALUMINUM
    ##
    ## < 9> OTHER
    ##
    ## <10> RETURN TO MAIN MENU
    ##
    ##
    print()
    VARIABLES['BO'] = input() ## 3200
    ## NOTE: I have no idea why "RETURN TO MAIN MENU" redirects to L3720_handle_extreding_guides
    ##       It seems more likely that it was supposed to redirect to _3730_
    onbo = [None,
            L3230_validate_aluminumttype_bottombar,
            L3310_validate_one_and_onehalf_bottombar_width,
            L3330_validate_two_and_onehalf_two_three_sixteenth_bottombar_width,
            L3370_validate_three_two_three_sixteenth_bottombar_width,
            L3410_validate_two_two_one_eighth,
            L3470_validate_two_onehalf_two_one_half_one_eighth,
            L3520_validate_tubular_aluminium,
            L3440_validate_three_two_three_sixteenth,
            L3490_validate_other_and_set_bottom_bar,
            L3720_handle_extruding_guides] 
    return onbo[VARIABLES['BO']]() ## 3210

def L3220_beep_and_L3140_print_bottombar_intro():
    """ Beeps before going to L3140 (yeah... that's it...) """
    "BEEP"
    return L3140_print_bottombar_intro() ## 3220

def L3230_validate_aluminumttype_bottombar():
    """ Validates Aluminum T Type Bottom Bar selection"""
    ## DT == SERVICE DOOR, TS == (<1> 3 5/8 INCH CROWN SLAT, <2> 2 7/8 INCH CROWN SLAT)
    if VARIABLES['DT']==A[53] and VARIABLES['TS']<=2:
        return L3260_validate_aluminumtype_bottombar_more()  ## 3230

    ## DT == ROLLING GRILLE, EG: Extruded Guides
    if VARIABLES['DT']==A[56] and VARIABLES['EG']=="Y" :
        return L3720_handle_extruding_guides() ## 3240

    ## DT == ROLLING GRILLE, EG: Extruded Guides, SBH: Slat Bottom Height
    if VARIABLES['DT']==A[56] and VARIABLES['EG']=="N" and VARIABLES['SBH']!=0:
        return L3260_validate_aluminumtype_bottombar_more() ## 3250

    ## This function seems to roll into L3260
    ## I have no idea why the above if-statement also directs there
    return L3260_validate_aluminumtype_bottombar_more()

def L3260_validate_aluminumtype_bottombar_more():
    if VARIABLES['CW']>=192.125:
        print("DOOR TOO WIDE FOR A[16] BOT. BAR")
        return L3220_beep_and_L3140_print_bottombar_intro() ## 3260
    VARIABLES['BB']=A[16]
    print()
    print("VARIABLES['BB'] BOTTOM BAR")
    ## DT == SERVICE DOOR
    if VARIABLES['DT']==A[53]:
        VARIABLES['AW']=1.21
        VARIABLES['BBH']=2.5
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3270
    ## DT == ROLLING GRILLE
    if VARIABLES['DT']==A[56] and SBH!=0:
        VARIABLES['AW']=1.21
        VARIABLES['BBH']=2.5
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3280
    ## NOTE!!!! Moving into the next line, we seem to be changing the Bottom Bar to 1-1/2
    ## (specfically 1/8" variant); the code seems to recognize that we're making the switch
    ## at an odd point (L3270 -> L3320), but we don't explicitly communcate the change to
    ## the user for some reason
    if VARIABLES['DT']==A[56]:
        VARIABLES['AW']=1.6383
        VARIABLES['BBH']=4
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3290
    if VARIABLES['DT']==A[53] or VARIABLES['DT']==A[54] or VARIABLES['DT']==A[56] and VARIABLES['EG']=="N":
        return L3310_validate_one_and_onehalf_bottombar_width()
    else:
        return L3150_bottombar_validation_error() ## 3300

def L3310_validate_one_and_onehalf_bottombar_width():
    """ Validates the width for the 1-1/2" bottom bar and sets it """
    if VARIABLES['CW']>=192.125:
        print("TOO WIDE FOR A[17]")
        ## TOO WIDE FOR 1 1/2" x 1 1/2" x 1/8" (STL)
        return L3220_beep_and_L3140_print_bottombar_intro() ## 3310
    print()
    print( "A[17] BOTTOM BAR")
    ## 1 1/2" x 1 1/2" x 1/8" (STL) BOTTOM BAR
    VARIABLES['AW']=2.46
    VARIABLES['BB']=A[17]
    VARIABLES['BBH']=2
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3320

def L3330_validate_two_and_onehalf_two_three_sixteenth_bottombar_width():
    """ Forks validation for 2-1/2 x 2 x 3/16 Steel Bottom Bar"""
    ## DT == ROLLING GRILLE, EG: Extruding Guides
    if VARIABLES['DT']==A[56] and VARIABLES['EG']=="Y" :
        return L3720_handle_extruding_guides() ## 3330
    ## DT in [SERVICE DOOR, WEATHERTITE DOOR, FIRE DOOR], DT = ROLLING GRILLE, EG: Extruding Guides
    if VARIABLES['DT'] in [A[53], A[54], A[55]] or (VARIABLES['DT']==A[56] and VARIABLES['EG']=="N"):
        return L3350_validate_and_set_two_half_two_three_sixteenth_bottombar()
    else:
        return L3150_bottombar_validation_error() ## 3340

def L3350_validate_and_set_two_half_two_three_sixteenth_bottombar():
    ## A[18]: 2 1/2" x 2" x 3/16" (STL)
    if VARIABLES['CW']>=312.125:
        print("TOO WIDE FOR "+A[18])
        return L3220_beep_and_L3140_print_bottombar_intro() ## 3350
    print()
    print(A[18]+" BOTTOM BAR")
    ## AW: Angle Weight???, BBH: Bottom Bar Height
    VARIABLES['AW']=5.5
    VARIABLES['BB']=A[18]
    VARIABLES['BBH']=2.5
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3360

def L3370_validate_three_two_three_sixteenth_bottombar_width():
    """ Fork validation for 3 x 2 x 3/16 Steel Bottom Bar """
    ## DT == ROLLING GRILLE, EG: Extruding Guides
    if VARIABLES['DT']==A[56] and VARIABLES['EG']=="Y":
        return L3720_handle_extruding_guides() ## 3370

    ## DT in [SERVICE DOOR, WEATHERTITE DOOR, FIRE DOOR], DT = ROLLING GRILLE, EG: Extruding Guides
    if VARIABLES['DT'] in [A[53], A[54], A[55]] or (VARIABLES['DT']==A[56] and VARIABLES['EG']=="N"):
        return L3390_update_bottom_bar_angle()
    else:
        return L3150_bottombar_validation_error() ## 3380

def L3390_update_bottom_bar_angle():
    """ Updates the Bottom Bar to 3" x 2" x 3/16" (STEEL) """
    print()
    ## A[19]: 3" x 2" x 3/16" (STEEL)
    print(A[19] + " BOTTOM BAR")
    ## AW: Angle Weight???
    VARIABLES['AW']=6.2
    VARIABLES['BB']=A[19]
    ## BBH: Bottom Bar Height
    VARIABLES['BBH']=2.5
    ## SSEB: Safety Edge on Bottom Bar, A[89]: PNEAUMATIC (Air)
    if VARIABLES['SEBB']==A[89]:
        VARIABLES['BBH']=3.5 ## 3390
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3400

def L3410_validate_two_two_one_eighth():
    """ Forks validation for 2" x 2" x 1/8" Aluminum Bottom Bar """
    ## DT in [SERVICE DOOR, WEATHERTITE DOOR], DT == ROLLING GRILLE, CW: Curtain Width???
    if VARIABLES['DT'] in [A[53], A[54]] or (VARIABLES['DT']==A[56] and VARIABLES['CW']<=192):
        return L3420_set_two_two_one_eighth_bottombar()
    else:
        return L3150_bottombar_validation_error() ## 3410

def L3420_set_two_two_one_eighth_bottombar():
    """ Sets 2" x 2" x 1/8" Aluminum Bottom Bar """
    ## A[20]: 2" x 2" x 1/8" (ALUM.), AW: Angle Weight???, BBH = Bottom Bar Height 
    print()
    print(A[20]+" BOTTOM BAR")
    VARIABLES['AW']=1.14
    VARIABLES['BB']=A[20]
    VARIABLES['BBH']=3
    ## DT == ROLLING GRILLE, SBH = Slat Bottom Height
    if VARIABLES['DT']==A[56] and VARIABLES['SBH']==0:
        VARIABLES['BBH']=3.5
        "LOCATE 23,40"
        print("TWISTED LINK") ## 3420
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3430

def L3440_validate_three_two_three_sixteenth():
    """ Fork validation for 3" x 2" 3/16" Aluminium Bottom Bar """ 
    if VARIABLES['DT'] in [A[53], A[54], A[56]] and VARIABLES['CW']<=294.5:
        return L3450_set_three_two_three_sixteenth_bottombar()
    else:
        return L3150_bottombar_validation_error() ## 3440

def L3450_set_three_two_three_sixteenth_bottombar():
    print()
    ## 3" x 2" x 3/16" ALUMINUM BOTTOM BAR
    print(A[86]+" BOTTOM BAR")
    VARIABLES['AW']=2.14
    VARIABLES['BB']=A[86]
    VARIABLES['BBH']=3
    ## DT == ROLLING GRILLE, SBH: Slot Bottom Height?
    if VARIABLES['DT']==A[56] and SBH==0:
        VARIABLES['BBH']=3.5
        "LOCATE 23,40"
        print("TWISTED LINK") ## 3450
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3460

def L3470_validate_two_onehalf_two_one_half_one_eighth():
    """ Forks validation for 2-1/2" x 2-1/2" x 1/8" Aluminum Bottom Bar """
    ## NOTE: The below logic was reworked
    ## DT == ROLLING GRILLE, EG = Extruded Guides, CW: Curtain Width
    if VARIABLES['DT']==A[56]:
        if (VARIABLES['EG']=="Y" and VARIABLES['CW']<=188.5)\
        or (VARIABLES['EG']=="N" and VARIABLES['CW']<=187.125):
            return L3480_set_two_onehalf_two_onehalf_one_eighth_bottombar()
    return L3150_bottombar_validation_error() ## 3470

def L3480_set_two_onehalf_two_onehalf_one_eighth_bottombar():
    """ Sets the Bottom Bar as 2-1/2" x 2-1/2" x 1/8" Aluminum """
    print()
    ## 2 1/2" x 2 1/2" x 1/8" (ALUM.)
    print(A[87])
    VARIABLES['BB']=A[87]
    ## AW: Angle Weight???, BBH: Bottom Bar Height
    VARIABLES['AW']=1.462
    VARIABLES['BBH']=4
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3480

def L3490_validate_and_set_other_bottom_bar():
    ## NOTE: Tubular Angle must be used with Extruded Guides
    ## DT == ROLLING GRILLE, EG: EXTRUDED GUIDES
    if VARIABLES['DT']==A[56] and VARIABLES['EG']=="Y":
        return L3720_handle_extruding_guides() ## 3490

    ## NOTE: Not sure why we're repeating Grille+Extrude
    if VARIABLES['DT']==A[55] or VARIABLES['DT']==A[56] and VARIABLES['EG']=="Y":
        return L3150_bottombar_validation_error() ## 3500

    print()
    VARIABLES['AW'] = input("ENTER BOT. BAR WEIGHT PER FT. ")
    print()
    VARIABLES['BBH'] = input("ENTER HEIGHT OF BOTTOM BAR")
    VARIABLES['BB']="SPECIAL"
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() #3510

def L3520_validate_tubular_aluminium():
    if TS!=5:
        print()
        print("NOT AVAILABLE ON DOOR")
        return L3220_beep_and_L3140_print_bottombar_intro() ## 3520
    if VARIABLES['EG']=="N":
        print()
        print(A[81]+" NOT AVAILABLE WITHOUT EXTRUDED GUIDES")
        return L3220_beep_and_L3140_print_bottombar_intro() ## 3530
    return L3540_set_tubular_bottombar_type()    ## (Implicit)

def L3540_set_tubular_bottombar_type():
    """ Sets the Tubular Bottom Bar to Standard or Large"""
    ## Tubular Bottom Bar Type???
    VARIABLES['TBBT'] = input("SELECT STANDARD or LARGE TUBULAR BOTTOM BAR (STD=S LRG=L)") ## 3540
    if VARIABLES['TBBT']=="S":
        return L3640_set_standard_tubular_alumninum_bottom_bar() ## 3550
    return L3570_set_tubular_bottombar_large()

def L3570_set_tubular_bottombar_large():
    """ Asks to update stop height on Large Tubular Bottom Bar (Originally runover from L3540) """
    if VARIABLES['TBBT']=="L":
        ## LT? Bottom Bar ???
        VARIABLES['LTBB']=3.5
        print()
        "BEEP" ## 3560
        L170_brightwhiteonredtext()
        VARIABLES['Q'] = input("DID YOU ADD 3 1/2 INCHES (5 INCHES WITH SAFETY EDGE) TO STOP HEIGHT (Y,N)")
        L150_yellowonblacktext() ## 3570

        if VARIABLES['Q']=="Y":
            return L3680_update_tubular_bottombar_by_curtain_width() ## 3580
        return L3590_large_tbbt_ask_add_stopheight()

def L3590_large_tbbt_ask_add_stopheight():
        if VARIABLES['Q']=="N":
            print()
            L160_whiteonbluetext()
            VARIABLES['ADDSH'] = input("DO YOU WISH TO DO SO NOW (Y,N)")
            L150_yellowonblacktext()
            return L3610_fork_update_stop_height() ## 3590
        return L3570_set_tubular_bottombar_large() ## 3600

def L3610_fork_update_stop_height():
    """ Forks for adding stop height based on Large Tubular Bottom Bar """
    if VARIABLES['ADDSH']=="Y":
        return L1580_update_stop_height() ## 3610
    if VARIABLES['ADDSH']=="N":
        return L3140_print_bottombar_intro() ## 3620
    return L3590_large_tbbt_ask_add_stopheight() ## 3630

def L3640_set_standard_tubular_alumninum_bottom_bar():
    """ Sets the Bottom Bar as Standard Tubular Alumnium """
    if CW<=216:
        ## A[81]: STANDARD TUBULAR ALUMINUM
        VARIABLES['BB']=A[81]
        L160_whiteonbluetext()
        print()
        print( VARIABLES['BB'])
        L150_yellowonblacktext()
        VARIABLES['AW']=1.82
        VARIABLES['BBH']=3.5
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3640
    if CW<=300:
        ## STANDARD TUBULAR ALUMINUM WITH (1) 2" x 2" x 1/8" STEEL STIFFENER
        VARIABLES['BB']=A[81]+" WITH (1) "+A[83]+" "+A[84]
        L160_whiteonbluetext()
        print( VARIABLES['BB'])
        L150_yellowonblacktext()
        VARIABLES['AW']=3.47
        VARIABLES['BBH']=3.5
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3650
    if CW<=420:
        ## STANDARD TUBULAR ALUMINUM WITH (1) 3" x 2" x 3/16" (STEEL) STIFFENER
        VARIABLES['BB']=A[81]+" WITH (1) "+A[19]+" "+A[84]
        L160_whiteonbluetext()
        print( VARIABLES['BB'])
        L150_yellowonblacktext()
        VARIABLES['AW']=4.92
        VARIABLES['BBH']=3.5
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3660
    if CW>=420:
        ## STANDARD TUBULAR ALUMINUM WITH (2) 3" x 2" x 3/16" (STEEL) STIFFENER
        VARIABLES['BB']=A[81]+" WITH (2) "+A[19]+" "+A[84]
        L160_whiteonbluetext()
        print( VARIABLES['BB'])
        L150_yellowonblacktext()
        VARIABLES['AW']=8.020002
        VARIABLES['BBH']=3.5
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3670

def L3680_update_tubular_bottombar_by_curtain_width():
    ## CW: Curtain Width ???, AW: Angle Weight???, BBH = Bottom Bar Height 
    if VARIABLES['CW']<=264:
        VARIABLES['BB']=A[82]
        print()
        L160_whiteonbluetext()
        print(VARIABLES['BB'])
        L150_yellowonblacktext()
        VARIABLES['AW']=2.06
        VARIABLES['BBH']=4
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3680
    if VARIABLES['CW']<=360:
        ## LARGE TUBULAR ALUMINUM WITH (2) 3" x 2" x 3/16" ALUMINUM STIFFENER
        VARIABLES['BB']=A[82]+" WITH (2) "+A[86]+" "+A[84]
        L160_whiteonbluetext()
        print(VARIABLES['BB'])
        L150_yellowonblacktext()
        VARIABLES['AW']=4.2
        VARIABLES['BBH']=4
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3690
    if VARIABLES['CW']<=480:
        ## LARGE TUBULAR ALUMINUM WITH (1) 2 1/2" x 2" x 3/16" (STL) STIFFENER
        VARIABLES['BB']=A[82]+" WITH (1) "+A[19]+" "+A[84]
        L160_whiteonbluetext()
        print()
        print(VARIABLES['BB'])
        L150_yellowonblacktext()
        VARIABLES['AW']=5.16
        VARIABLES['BBH']=4
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3700
    if VARIABLES['CW']>=480:
        ## LARGE TUBULAR ALUMINUM WITH (2) 2 1/2" x 2" x 3/16" (STL) STIFFENER
        VARIABLES['BB']=A[82]+" WITH (2) "+A[19]+" "+A[84]
        L160_whiteonbluetext()
        print()
        print( VARIABLES['BB'])
        L150_yellowonblacktext()
        VARIABLES['AW']=8.26
        VARIABLES['BBH']=4
        return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3710

def L3720_handle_extruding_guides():
    """ Checks if selected bottom bar/door combination is illegal because of Extruding Guides """
    ## EG: Extruding Guides
    if VARIABLES['EG']=="Y":
        "BEEP"
        L170_brightwhiteonredtext()
        print()
        print(" YOU MUST USE TUBULAR ALUMINUM WITH EXTRUDED GUIDES ")
        L150_yellowonblacktext()
        return L3540_set_tubular_bottombar_type() ## 3720
    ## BO: Bottom (Bar) Option
    VARIABLES['BO']=0
    return L290_L110_rundelay_and_L590_loadvars_and_main_menu() ## 3730

def L11260_format_float_as_measurement():
    """ Formats a float as a measurement of form "F ft.-IN/D"" """
    ## IDD: Temporary Container for Integer Portion
    ## Get Integer portion
    VARIABLES['IDD']=int(VARIABLES['DD'])
    ## FDD: Temporary Container for Decimal Portion
    ## Get Decimal Portion
    VARIABLES['FDD']=VARIABLES['DD']-VARIABLES['IDD']
    ## EF: Temporary Container for Feet
    ## Get Feet
    VARIABLES['EF']=int(VARIABLES['IDD']/12)
    ## EI: Temporary Container for Inches
    ## Get Inches
    VARIABLES['EI']=VARIABLES['IDD']-(VARIABLES['EF']*12)
    ## SXT: Temporary Container for 1/16ths
    ## Convert Decimal to 1/16 (i.e.- .25 * 16 = 4/16 = 1/4)
    VARIABLES['SXT']=VARIABLES['FDD']*16 ## 11260
    ## NUM: Temporary Container for Numerator, DEN: Temporary Container for Denominator
    if VARIABLES['SXT'] in [1, 3, 5, 7, 9, 11, 13, 15]:
        VARIABLES['NUM']=VARIABLES['SXT']
        VARIABLES['DEN']=16
        return L11310_set_EF() ## 11270
    if VARIABLES['SXT'] in [2,6,10,14]:
        VARIABLES['NUM']=VARIABLES['SXT']/2
        VARIABLES['DEN']=8 ## 11280
    if VARIABLES['SXT'] in [4,12]:
        VARIABLES['NUM']=VARIABLES['SXT']/4
        VARIABLES['DEN']=4 ## 11290
    if VARIABLES['SXT']==8:
        VARIABLES['NUM']=1
        VARIABLES['DEN']=2 ## 11300
    ## This is implicit, though it is odd that the odd numbers
    ## explicitly call it...
    return L11310_set_EF()

def L11310_set_EF():
    """ Combines information from L11260 into the appropriate String """
    ## EI: Temporary Container for Inches, SXT: Temporary Container for 1/16ths
    ## ED: Final String form of DD, EF: Temporary Container for Feet
    if VARIABLES['EI']==0 and VARIABLES['SXT']==0:
        VARIABLES['ED']='VARIABLES["EF"] ft.- 0"'
        return ## 11310
    if VARIABLES['SXT']==0:
        VARIABLES['ED']='VARIABLES["EF"] ft.-VARIABLES["EI"]"'
        return ## 11320
    ## NUM: Temporary Container for Numerator, DEN: Temporary Container for Denominator
    VARIABLES['ED']='VARIABLES["EF"] ft.-VARIABLES["EI"]VARIABLES["NUM"]/VARIABLES["DEN"]"'
    return ## 11330   

def L1860_ask_standard_manufacturer_SM():
    print()
    VARIABLES['SM'] = input("STANDARD MANUFACTURE (Y=Yes N=No) ") ## 1860
    ## DT == FIRE DOOR
    if VARIABLES['DT']==A[55]:
        VARIABLES['SM']="N"
        return 2000 ## 1870
    if VARIABLES['SM']=="Y":
        return 4750 ## 1880
    if VARIABLES['SM']=="N":
        return L1910_print_nonstandardselection_menu() ## 1890
    "BEEP"
    return L1860_ask_standard_manufacturer_SM() ## 1900

    

print(::GOSUB 230:BEEP:print(" REQUIRES A MINIMUM OF 2"VARIABLES['I']" UPSET PLUS 2"VARIABLES['I']" SHOULD BE ADDED TO STOP HEIGHT and ":VARIABLES['SEBB']=A[89]:SE=.6-AS:GOSUB 150 (3050)
GOSUB 230:print(" BOTTOM BAR MUST HAVE A 3"VARIABLES['I']" LEG (FACING UP) ":GOSUB 150 (3060)

BEEP:GOTO 3030 (3130)

    
##  UPSET OPTIONS (3740)
print(:INPUT"ENTER UPSET ";VARIABLES['U'] (3750)
if VAL(VARIABLES['U'])>=1.5 : return 3780 (3760)

if VARIABLES['U']="0" : return 3790 else: return 3810 (3770)

if VARIABLES['DT']=A[55] and (SH+VAL(VARIABLES['U']))>170 : return 3820 else: return 3800 (3780)

if VARIABLES['DT']=A[55] or VARIABLES['EG']="Y" or SH>192 : return 3810 (3790)

print(:GOSUB 160:print( " "VARIABLES['U']" INCHES OF UPSET ":GOSUB 150:GOTO 290 (3800)
if VARIABLES['EG']="Y" : return 3800 else: BEEP:print(:print("MINIMUM UPSET = 1.5"VARIABLES['I']" FOR THIS TYPE or SIZE":GOTO 3740 (3810)

BEEP:print(:print("MAXIMUM UPSET = 2"VARIABLES['I']" FOR THIS TYPE or SIZE":GOTO 3740 (3820)
##  WINDLOCK OPTIONS (3830)
if VARIABLES['DT']=A[55] or VARIABLES['DT']=A[56] return 3900 (3840)

if TS=1 or TS=4 : return 3910 (3850)

print(:INPUT"ENTER WINDLOCK SPACING ";VARIABLES['WL']:IF VARIABLES['OVWL']="Y" : BEEP:GOSUB 170:print(" PARAMETER OVERRIDE!!!! ":GOSUB 150:BEEP:GOTO 3970 (3860)
if VAL(VARIABLES['WL'])=1 or VAL(VARIABLES['WL'])=3 or VAL(VARIABLES['WL'])=5 or VAL(VARIABLES['WL'])>6 : GOSUB 170:BEEP:print(" SPACING MUST BE EVERY 6th, 4th, or 2nd SLAT ":GOSUB 150:GOTO 3860 (3870)
if TS=2 and CW>221 or TS=3 and CW>197 and VAL(VARIABLES['WL'])=0 : return 3920 (3880)

return 3970 (3890)

BEEP:GOSUB 170:print(" WINDLOCKS NOT AVAILABLE ON "VARIABLES['DT']" ":GOSUB 150:GOTO 290 (3900)
BEEP:GOSUB 170:print(" WINDLOCKS NOT AVAILABLE ON SLAT # "TS" ":GOSUB 150:GOTO 290 (3910)
BEEP:GOSUB 170:print(" WINDLOCKS EVERY 6th SLAT REQUIRED FOR 20 P.S.F. WINDLOAD ":GOSUB 150 (3920)
GOSUB 170:INPUT" DO YOU WISH TO OVERRIDE THIS REQUIREMENT ";VARIABLES['OVWL']:GOSUB 150 (3930)
if VARIABLES['OVWL']="Y" : return 3860 (3940)

if VARIABLES['OVWL']="N" : VARIABLES['WL']="":GOTO 290 (3950)
return 3930 (3960)

print(:GOSUB 160:print(" WINDLOCKS EVERY "VARIABLES['WL']"th SLAT ":GOSUB 150:GOTO 290 (3970)
CLS:print(:GOSUB 160:print(" ******** SELECT DESIRED SPRING OPTION ******** ":GOSUB 150 (3980)
print(A[21]:print(:print(A[22]:print(:print(A[23]:print(:print(A[24]:print(:print("<5> PANIC RELEASE DEVICE (AUTOMATIC OPEN)":print(:print("<6> "A[77] (3990)
print(:INPUT"ENTER SPRING OPTION NUMBER ";IT:ON IT return 4010,4020,4030,4040,4050,290,4060 (4000)

print(:GOSUB 160:print(A[21]" CYCLE SPRINGS":GOSUB 150:CY=25000:GOTO 290 (4010)
print(:GOSUB 160:print(A[22]" CYCLE SPRINGS":GOSUB 150:CY=50000!:GOTO 290 (4020)
print(:GOSUB 160:print(A[23]" CYCLE SPRINGS":GOSUB 150:CY=100000!:GOTO 290 (4030)
print(:GOSUB 160:print("MAXIMUM POSSIBLE CYCLES":GOSUB 150:VARIABLES['CY']="MAX":GOTO 290 (4040)
print(:GOSUB 160:print("<5> PANIC RELEASE DEVICE (AUTOMATIC OPEN)":GOSUB 150:VARIABLES['PRD']="Y":GOTO 290 (4050)
BEEP:GOTO 4000 (4060)
CLS:print(:GOSUB 160:print(" ********* SELECT DESIRED ENDLOCK OPTION ********* ":GOSUB 150 (4070)
print(A[25]:print(:print(A[26]:print(:print(A[27]:print(:print( "<4> NO ENDLOCKS":print(:print("<5> "A[77]:print( (4080)
input("ENTER OPTION NUMBER ";OP:IF OP>=6 : BEEP:GOTO 4090 (4090)
ON OP return 4110,4130,4150,4170,4180,4200 (4100)

if NOT TS=1 : return 4190 (4110)

print(:GOSUB 160:print(A[25]" ENDLOCKS":GOSUB 150:EL=.35:GOTO 290 (4120)
if TS=1 : return 4190 (4130)

print(:GOSUB 160:print(A[26]" ENDLOCKS":GOSUB 150:VARIABLES['CIE']="Y":GOTO 290 (4140)
if TS=2 or TS=3 : return 4160 else: return 4190 (4150)

print(:GOSUB 160:print(A[27]" ENDLOCKS":GOSUB 150:EL=.4375:GOTO 290 (4160)
print(:GOSUB 170:BEEP:print( "NO ENDLOCKS":GOSUB 150:VARIABLES['NOEL']="Y":EL=0:GOTO 290 (4170)
return 290 (4180)

BEEP:print(:GOSUB 170:print(" SORRY! NOT AVAILABLE FOR SLAT #"TS" ":GOSUB 150:GOSUB 110:GOTO 4070 (4190)
BEEP:GOTO 4070 (4200)
##  SLOPED BOTTOM BAR (4210)
CLS:GOSUB 160:print(" ***** "VARIABLES['RIGHT'](A[10],5)"D BOTTOM BAR ***** ":GOSUB 150 (4220)
print(:print(:INPUT"ENTER SLOPE DIFFERENTIAL IN INCHES";SD1 (4230)
print(:print(:GOSUB 160:print( " "SD1" INCH SLOPED BOTTOM BAR ":GOSUB 150 (4240)
input("INCREASE UPSET TO ALLOW FOR SLOPE (SLOPE+3) <Y=Yes N=No>";VARIABLES['UTC'] (4250)
if VARIABLES['UTC']="N" : return 4300 (4260)

if VARIABLES['UTC']="Y" : VARIABLES['U']=VARIABLES['STR'](SD1+3):print(:GOSUB 170:print(" ADDED "VARIABLES['U']" UPSET  ":GOSUB 150:GOTO 4290 (4270)
BEEP:GOTO 4250 (4280)
BEEP:GOSUB 170:print(" NOTE: STOP HEIGHT MUST BE FROM LOW POINT OF GRADE ":GOSUB 150:GOTO 4310 (4290)
if VARIABLES['UTC']="N" : print(:BEEP:GOSUB 170:print(" NOTE: STOP HEIGHT MUST BE FROM HIGH POINT OF GRADE":GOSUB 150 (4300)
input("DO YOU WISH TO CHANGE STOP HEIGHT";VARIABLES['ANS'] (4310)
if VARIABLES['ANS']="Y" : return 1580 (4320)

if VARIABLES['ANS']="N" : return 290 (4330)

BEEP:GOTO 4310 (4340)
CLS:print(:GOSUB 160:print(" **** SELECT OVERSIZED PIPE or BARREL RING OPTION **** ":GOSUB 150 (4350)
print("<1> LARGER THAN STANDARD PIPE":print(:print("<2> ELIMINATE PIPE RINGS":print(:print("<3> SPECIAL SIZE PIPE RINGS":print(:print("<4> "A[77]:print( (4360)
input("ENTER OPTION NUMBER ";IT:ON IT return 4380,4450,4460,290,4480 (4370)

CLS:print(" **** SELECT OVERSIZED PIPE **** ":print(:print( (4380)
print("<1> "A[44]:print(:print("<2> "A[45]:print(:print("<3> "A[46]:print(:print("<4> "A[47]:print(:print(:print("<5> "A[77]:print(:print(:print( (4390)
input("ENTER OPTION NUMBER ";IT:ON IT return 4410,4420,4430,4440,290,4480 (4400)

print(:LSP=3:GOSUB 160:print(A[43]:GOSUB 150:GOTO 290 (4410)
print(:LSP=5:GOSUB 160:print(A[45]:GOSUB 150:GOTO 290 (4420)
print(:LSP=6:GOSUB 160:print(A[46]:GOSUB 150:GOTO 290 (4430)
print(:LSP=7:GOSUB 160:print(A[47]:GOSUB 150:GOTO 290 (4440)
print(:PR=1:GOSUB 160:print("PIPE RINGS ELIMINATED":GOSUB 150:GOTO 290 (4450)
print(:INPUT"ENTER RADIUS OF SPECIAL PIPE RING ";VARIABLES['IL'] (4460)
print(:GOSUB 160:print("SPECIAL "VARIABLES['IL']" INCH RADIUS RING":GOSUB 150:GOTO 290 (4470)
BEEP:GOTO 4370 (4480)
CLS:print(:GOSUB 160:print(" ****** SELECT ADJUSTER OPTION ****** ":GOSUB 150 (4490)
print(A[28]:print(:print(A[29]:print(:print("<3> "A[77]:print( (4500)
input("ENTER ADJUSTER OPTION NUMBER ";IT:ON IT return 4520,4530,290,4540 (4510)

AJ=4:print(:GOSUB 160:print(A[28]:GOSUB 150:GOTO 290 (4520)
AJ=4:print(:GOSUB 160:print(A[29]:GOSUB 150:GOTO 290 (4530)
BEEP:GOTO 4510 (4540)
CLS:GOSUB 160:print(" ****** SELECT BRACKET PLATE OPTION ****** ":GOSUB 150 (4550)
print(A[34]:print(:print(A[35]:print(:print("<3> "A[77]:print( (4560)
input("ENTER BRACKET PLATE OPTION NUMBER";IT:ON IT return 4580,4590,290,4610 (4570)

print(:GOSUB 160:print(A[34]:SB=1:GOSUB 150:GOTO 290 (4580)
print(:INPUT"ENTER BRACKET PLATE SIZE";LGBP:print( (4590)
print( LGBP" INCH BRACKET PLATE":GOTO 290 (4600)
BEEP:GOTO 4570 (4610)
if VARIABLES['DT']=A[55] or VARIABLES['DT']=A[56] : BEEP:print(:print(A[14]" NOT AVAILABLE ON "VARIABLES['DT']:GOTO 290 (4620)
CLS:GOSUB 160:print(" ******** SELECT PASS DOOR OPTION ******** ":GOSUB 150 (4630)
print(:print("<1>  2 '- 6  x  7 '- 0  at LEFT JAMB":print( (4640)
print("<2>  2 '- 6  x  7 '- 0  at RIGHT JAMB":print( (4650)
print("<3>  3 '- 0  x  7 '- 0  at LEFT JAMB":print( (4660)
print("<4>  3 '- 0  x  7 '- 0  at RIGHT JAMB":print( (4670)
print("<5>  "A[77]:print(:print(:print( (4680)
input("SELECT PASS DOOR OPTION NUMBER ";PDO:ON PDO return 4710,4720,4730,4740,290 (4690)

BEEP:GOTO 4690 (4700)
VARIABLES['PD']="2L":print(:print("2 '- 6  x  7 '- 0  "A[14]" at LEFT JAMB":GOTO 290 (4710)
VARIABLES['PD']="2R":print(:print("2 '- 6  x  7 '- 0  "A[14]" at RIGHT JAMB":GOTO 290 (4720)
VARIABLES['PD']="3L":print(:print("3 '- 0  x  7 '- 0  "A[14]" at LEFT JAMB":GOTO 290 (4730)
VARIABLES['PD']="3R":print(:print("3 '- 0  x  7 '- 0  "A[14]" at RIGHT JAMB":GOTO 290 (4740)

def L4750_():
    ## TS == , SBH: SlotBottomHeight
    if VARIABLES['TS']==5 and VARIABLES['SBH']==0:
        return 4760
    else:
        return 4830 ## 4750
    
def L4760_print_wrap_slat_type_menu():
    "CLS"
    print()
    L160_whiteonbluetext()
    print(" ******* SELECT TOP WRAP SLAT OPTION ******* ")
    L150_yellowonblacktext()
    print() ## 4760
    print("#1   3 5/8" + VARIABLES['I'] + " CROWN SLATS")
    print()
    print("#2   2 7/8" + VARIABLES['I']+ " CROWN SLATS")
    print()
    print() ## 4770
    return L4780_ask_wrap_slat_type()

def L4780_ask_wrap_slat_type():
    VARIABLES['ST'] = input("ENTER WRAP SLAT OPTION (#1 or #2)") ## 4780
    if VARIABLES['ST']=="#1":
        print()
        print(A[30][:-21] + " WRAP SLATS")
        return 4820 ## 4790
    if VARIABLES['ST']=="#2":
        print()
        print(A[31][:-21] + " WRAP SLATS")
        return 4820 ## 4800
    "BEEP"
    return L4780_ask_wrap_slat_type() ## 4810

def L4820_():
    L110_rundelay() ## 4820
    print()
    L190_blackongreentext()
    print(" ********** REMAINDER STANDARD MANUFACTURE ********** ")
    L150_yellowonblacktext() ## 4830
    L110_rundelay() ## 4840
    ## DT == FIRE DOOR
    if VARIABLES['DT']==A[55]:
        return 5040 ## 4850

    if VARIABLES['WL_S']!="":
        VARIABLES['WL']=int(VARIABLES['WL_S'])
        return 4900 ## 4860
    if VARIABLES['WL']==0 and VARIABLES['TS']==2 and VARIABLES['CW']>=221:
        VARIABLES['WL']=6
        return 4900 ## 4870
    if VARIABLES['WL']==0 and VARIABLES['TS']==3 and VARIABLES['CW']>=197:
        VARIABLES['WL']=6
        return 4900 ## 4880
    if VARIABLES['WL']==0 and VARIABLES['TS']==6 and VARIABLES['CW']>=264:
        VARIABLES['WL']=6 ## 4890
    return L4900_() ## implicit
    
def L4900_():
    if VARIABLES['SG']!="":
        return 5200 ## 4900
    if VARIABLES['TS']==1 and VARIABLES['CW']<=165:
        ## GW accepted scientific notation; I changed to string for python interpretation
        VARIABLES['SW']=float("5.378666E-02")
        VARIABLES['SG']="22" ## 4910
    if VARIABLES['TS']==1 and VARIABLES['CW']>165:
        ## NOTE: This was explicitely stated as double precision
        SW=float(.058514166)
        VARIABLES['SG']="20" ## 4920
    if VARIABLES['TS']==3 and VARIABLES['CW']<=244.75:
        ## GW accepted scientific notation; I changed to string for python interpretation
        VARIABLES['SW']=float("5.729167E-02")
        VARIABLES['SG']="20" ## 4930
    if VARIABLES['TS']==2 and VARIABLES['CW']<=244.75:
        ## GW accepted scientific notation; I changed to string for python interpretation
        VARIABLES['SW']=float("5.485475E-02")
        VARIABLES['SG']="20" ## 4940
    if VARIABLES['TS']==5 and VARIABLES['CW']<=220.75 and VARIABLES['BST']!="#2" and VARIABLES['ST']!="#2":
        VARIABLES['SW']=.0537866
        VARIABLES['SG']="22"
        VARIABLES['EL']=.21875
        VARIABLES['ST']="#1"
        VARIABLES['HS']=3.625
        return 5200 ## 4950
    if VARIABLES['TS']==5 and VARIABLES['CW']>220.75 and VARIABLES['ST']!="#2" and VARIABLES['BST']!="#2":
        ## NOTE: This was explicitely stated as double precision
        VARIABLES['SW']=float(.058514166)
        VARIABLES['SG']="20"
        VARIABLES['EL']=.21875
        VARIABLES['ST']="#1"
        VARIABLES['HS']=3.625
        return 5200 ## 4960
    if VARIABLES['TS']==5 and VARIABLES['BST']!="#1" and VARIABLES['ST']!="#1" and VARIABLES['SG']!="18":
        ## NOTE: This was explicitely stated as double precision
        VARIABLES['SW']=float(.05485475)
        VARIABLES['SG']="20"
        VARIABLES['EL']=.17
        VARIABLES['ST']="#2"
        VARIABLES['HS']=2.875
        return 5200 ## 4970
    if VARIABLES['TS']==5 and VARIABLES['SG']=="18":
        VARIABLES['HS']=2.875
        VARIABLES['EL']=.17
        return 5200 ## 4980
    if VARIABLES['TS']==2 or VARIABLES['TS']==3:
        return 5000
    else:
        return 5020 ## 4990

if SH>=148.875 and CW>=220.875 : SW=.071269154#:VARIABLES['SG']="18":GOTO 5200 (5000)
if CW>=244.875 and NOT TS=6 : SW=.071269154#:VARIABLES['SG']="18":GOTO 5200 (5010)

def L5020_set_slat_properties():
    """ This function seems to determine Slat Properties (for Fire Doors) """
    ## TS == MIDGET CROWN SLAT < 2 INCH >
    if VARIABLES['TS']==4:
        ## SW: ???, SG: Slat Gage
        VARIABLES['SW']=.03917
        VARIABLES['SG']="20"
        return 5200 ## 5020
    ## DT == FIRE DOOR
    if VARIABLES['DT']!=A[55]:
        return 5200 ## 5030

    ## SL: ???, GR: ???, PL: ???, GD: ???

    ## DT == FIRE DOOR, TS == 3 5/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==1 and VARIABLES['CW']<=96:
        VARIABLES['SL']=VARIABLES['CW']+3.625
        VARIABLES['GR']=VARIABLES['CW']+6.5
        VARIABLES['PL']=VARIABLES['GR']-5.5
        VARIABLES['GD']="FD8"
        return 5160 ## 5040
    ## DT == FIRE DOOR, TS == 2 7/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==2 and VARIABLES['CW']<=96:
        VARIABLES['SL']=VARIABLES['CW']+3.75
        VARIABLES['GR']=VARIABLES['CW']+6.5
        VARIABLES['PL']=VARIABLES['GR']-5.5
        VARIABLES['GD']="FD8"
        return 5170 ## 5050
    ## DT == FIRE DOOR, TS == 3 5/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==1 and VARIABLES['CW']<=144:
        VARIABLES['SL']=VARIABLES['CW']+3.5
        VARIABLES['GR']=VARIABLES['CW']+6.875
        VARIABLES['PL']=VARIABLES['GR']-5.5
        VARIABLES['GD']="FD12"
        return 5160 ## 5060
    ## DT == FIRE DOOR, TS == 2 7/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==2 and VARIABLES['CW']<=144:
        VARIABLES['SL']=VARIABLES['CW']+3.625
        VARIABLES['GR']=VARIABLES['CW']+6.875
        VARIABLES['PL']=VARIABLES['GR']-5.5
        VARIABLES['GD']="FD12"
        return 5170 ## 5070
    ## DT == FIRE DOOR, TS == 3 5/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==1 and VARIABLES['CW']<=168:
        VARIABLES['SL']=VARIABLES['CW']+4.25
        VARIABLES['GR']=VARIABLES['CW']+8
        VARIABLES['PL']=VARIABLES['GR']-5.5
        VARIABLES['GD']="FD14"
        return 5160 ## 5080
    ## DT == FIRE DOOR, TS == 2 7/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==2 and VARIABLES['CW']<=168:
        VARIABLES['SL']=VARIABLES['CW']+4.375
        VARIABLES['GR']=VARIABLES['CW']+8
        VARIABLES['PL']=VARIABLES['GR']-5.5
        VARIABLES['GD']="FD14"
        return 5170 ## 5090
    ## DT == FIRE DOOR, TS == 3 5/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==1 and VARIABLES['CW']<=192:
        VARIABLES['SL']=VARIABLES['CW']+4.5
        VARIABLES['GR']=VARIABLES['CW']+8.5
        VARIABLES['PL']=VARIABLES['GR']-5.5
        VARIABLES['GD']="FD16"
        return 5160 ## 5100
    ## DT == FIRE DOOR, TS == 2 7/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==2 and VARIABLES['CW']<=192:
        VARIABLES['SL']=VARIABLES['CW']+4.625
        VARIABLES['GR']=VARIABLES['CW']+8.5
        VARIABLES['PL']=VARIABLES['GR']-5.5
        VARIABLES['GD']="FD16"
        return 5170 ## 5110
    ## DT == FIRE DOOR, TS == 3 5/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==1 and VARIABLES['CW']<=216:
        VARIABLES['SL']=VARIABLES['CW']+4.75
        VARIABLES['GR']=VARIABLES['CW']+9
        VARIABLES['PL']=VARIABLES['GR']-5.5
        VARIABLES['GD']="FD18"
        return 5160 ## 5120
    ## DT == FIRE DOOR, TS == 2 7/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==2 and VARIABLES['CW']<=216:
        VARIABLES['SL']=VARIABLES['CW']+4.875
        VARIABLES['GR']=VARIABLES['CW']+9
        VARIABLES['PL']=VARIABLES['GR']-5.5
        VARIABLES['GD']="FD18"
        return 5170 ## 5130
    ## DT == FIRE DOOR, TS == 3 5/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==1 and VARIABLES['CW']<=240:
        VARIABLES['SL']=VARIABLES['CW']+6
        VARIABLES['GR']=VARIABLES['CW']+10.5
        VARIABLES['PL']=VARIABLES['GR']-5.5
        VARIABLES['GD']="FD20"
        return 5160 ## 5140
    ## DT == FIRE DOOR, TS == 2 7/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==2 and VARIABLES['CW']<=240:
        VARIABLES['SL']=VARIABLES['CW']+6.125
        VARIABLES['GR']=VARIABLES['CW']+10.5
        VARIABLES['PL']=VARIABLES['GR']-5.5
        VARIABLES['GD']="FD20"
        return 5170 ## 5150

    ## SW: ??? Slat Weight, HS: Height Slat???, IR: ???, SG: Slat Gage

    ## DT == FIRE DOOR, TS == 3 5/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==1:
        VARIABLES['SW']=float(.058514166)
        VARIABLES['HS']=3.625
        VARIABLES['IR']=.5
        VARIABLES['SG']="20" ## 5160
        ## DT == FIRE DOOR, TS == 2 7/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==2:
        ## GW accepted scientific notation; I changed to string for python interpretation
        VARIABLES['SW']=float("5.485475E-02")
        VARIABLES['HS']=2.875
        VARIABLES['IR']=.695
        VARIABLES['SG']="20" ## 5170
    if VARIABLES['CW']>216 and VARIABLES['SH']>144 or VARIABLES['SGO']=="18":
        ## NOTE: This was explicitely stated as double precision
        VARIABLES['SW']=float(.071269154)
        VARIABLES['SG']="18"
        return L5530_set_BP() ## 5180
    return L5530_set_BP() ## 5190

if CW>365 or VARIABLES['WL']="0" : VARIABLES['CGR']="Y":GOTO 5400 (5200)
if VARIABLES['EG']="Y" : SL=CW+2.5:GR=SL+2:RL=SL+1:VARIABLES['GD']="EG1":GOTO 5530 (5210)
if TS=6 and CW<=149 and WL=0 : SL=CW+3.875:GR=SL+1.625:VARIABLES['GD']="SN1":GOTO 5480 (5220)
if TS=6 and CW<=293 and NOT WL=0 : SL=CW+4:GR=SL+2.5:VARIABLES['GD']="WL1":GOTO 5480 (5230)
if TS=6 and CW>149 and CW<264 and WL=0 : SL=CW+4.25:GR=SL+1.625:VARIABLES['GD']="SN2":GOTO 5480 (5240)
if TS=6 and CW>293 and NOT WL=0 : SL=CW+5:GR=SL+2.5:VARIABLES['GD']="WL2":GOTO 5480 (5250)
if TS<=2 and CW<149 and WL=0 : SL=CW+3.5:GR=SL+2:VARIABLES['GD']="SN1":GOTO 5530 (5260)
if TS<=2 and CW>=149 and CW<=221 and WL=0 : SL=CW+3.875:GR=SL+2:VARIABLES['GD']="SN2":GOTO 5530 (5270)
if TS=2 and CW<293 and NOT WL=0 : SL=CW+3.875:GR=SL+2.625:VARIABLES['GD']="WL1":GOTO 5530 (5280)
if TS=2 and CW>=293 and NOT WL=0 : SL=CW+4.875:GR=SL+2.625:VARIABLES['GD']="WL2":GOTO 5530 (5290)
if VARIABLES['EG']="N" and CW<149 : SL=CW+3.5:GOTO 5530 (5300)
if VARIABLES['EG']="N" and CW<221 : SL=CW+3.875:GOTO 5530 (5310)
if VARIABLES['EG']="N" and CW<293 : SL=CW+4.5:GOTO 5530 (5320)
if VARIABLES['EG']="N" and CW<=365 : SL=CW+5.5:GOTO 5530 (5330)
if TS=3 and WL=0 and CW<149 : SL=CW+4.25:GR=SL+1.25:VARIABLES['GD']="SN1":GOTO 5530 (5340)
if TS=3 and WL=0 and CW>=149 and CW<197 : SL=CW+4.625:GR=SL+1.25:VARIABLES['GD']="SN2":GOTO 5530 (5350)
if TS=3 and NOT WL=0 and CW<293 : SL=CW+4:GR=SL+2.5:VARIABLES['GD']="WL1":GOTO 5530 (5360)
if TS=3 and NOT WL=0 and CW>=293 : SL=CW+5:GR=SL+2.5:VARIABLES['GD']="WL2":GOTO 5530 (5370)
if TS=4 and CW<149 : SL=CW+3.75:GR=SL+1.75:VARIABLES['GD']="SN1":GOTO 5530 (5380)
if TS=4 and CW>=149 : SL=CW+4.125:GR=SL+1.75:VARIABLES['GD']="SN2":GOTO 5530 (5390)
input("SPECIFY BETWEEN BRACKETS IN INCHES (Assume 1/4 Brackets)";GR (5400)
VARIABLES['GD']="SPECIAL":IF TS<=2 and WL=0 or TS=5 : SL=GR-2 (5410)
if TS=2 and NOT WL=0 : SL=GR-2.625 (5420)
if TS=3 and WL=0 : SL=GR-1.25 (5430)
if TS=3 and NOT WL=0 : SL=GR-2.5 (5440)
if TS=4 and WL=0 : SL=GR-1.75 (5450)
if TS=6 and WL=0 : SL=GR-1.625 (5460)
if TS=6 and NOT WL=0 : SL=GR-2.5 (5470)
if NOT LGBP=0 : BP=LGBP:GOTO 5580 (5475)
if BP=0 and TS=6 and SH<=90 : BP=16:GOTO 5570 (5480)
if BP=0 and TS=6 and SH<=114 : BP=18:GOTO 5570 (5490)
if BP=0 and TS=6 and SH<=168 : BP=20:GOTO 5570 (5500)
if BP=0 and TS=6 and SH<=240 : BP=22:GOTO 5570 (5510)
if BP=0 and TS=6 and SH>240 : BP=24:GOTO 5570 (5520)

def L5530_set_BP():
    """ If BP (???) is not set, sets it, then continues to 5570 """

    ## BP: ???, SH: Stop Height

    if VARIABLES['BP']==0 and VARIABLES['SH']<144:
        VARIABLES['BP']=16
        return 5570 ## 5530
    if VARIABLES['BP']==0 and VARIABLES['SH']<192:
        VARIABLES['BP']=18
        return 5570 ## 5540
    if VARIABLES['BP']==0 and VARIABLES['SH']<240:
        VARIABLES['BP']=20
        return 5570 ## 5550
    if VARIABLES['BP']==0 and VARIABLES['SH']>=240:
        VARIABLES['BP']=22 ## 5560
    return L5570_() ## Implicit
        
def L5570_():
        
    ## WL: ???, BP: ???,
    if VARIABLES['WL']!=0:
        VARIABLES['BP']=VARIABLES['BP']+2 ## 5570
    ## US: ???, U: Upset???
    VARIABLES['US']=2
    if VARIABLES['U']!="":
        VARIABLES['US']=int(VARIABLES['U']) ## 5580
    if VARIABLES['WL']!=0 and VARIABLES['US']<1.5:
        return 3810 ## 5590

    ## HC: ???, SH: Stop Height
    ## Removed parens
    VARIABLES['HC']= VARIABLES['SH'] + VARIABLES['US'] + VARIABLES['BP']/2 ## 5600
        
    ## DT != FIRE DOOR
    if VARIABLES['DT']!=A[55]:
        return 5700 ## 5610

    ## GD: 
    if VARIABLES['GD']=="FD8" and VARIABLES['BP']==16:
        VARIABLES['PO']="3 3/4"
        return 6030 ## 5620
    if VARIABLES['GD']=="FD8" and VARIABLES['BP']==18:
        VARIABLES['PO']="4 5/8"
        return 6030 ## 5630
    if VARIABLES['GD']=="FD12" and VARIABLES['BP']==16:
        VARIABLES['PO']="3 3/4"
        return 6030 ## 5640
    if VARIABLES['GD']=="FD12" and VARIABLES['BP']==18:
        VARIABLES['PO']="4 5/8"
        return 6030 ## 5650
    if VARIABLES['GD']=="FD14" and VARIABLES['BP']==16:
        VARIABLES['PO']="3 3/4"
        return 6030 ## 5660
    if VARIABLES['GD']=="FD14" and VARIABLES['BP']==18:
        VARIABLES['PO']="4 5/8"
        return 6030 ## 5670
    if VARIABLES['GD']=="FD16":
        VARIABLES['PO']="4 3/8"
        return 6030 ## 5680
    if VARIABLES['GD']=="FD18" or VARIABLES['GD']=="FD20":
        VARIABLES['PO']="4 3/4"
        return 6030 ## 5690

    ## TS: Slat Type (as index)
    ## TS == SOLI SLATS AT BOTTOM OF ROLLING GRILLE (???)
    if VARIABLES['TS']==5:
        return 5790 ## 5700

    if VARIABLES['BP']<=16 and VARIABLES['WL']==0:
        VARIABLES['PO']="3 3/4"
        return 6030 ## 5710
    ## Logic rewritten
    if VARIABLES['TS'] in [3,6] and VARIABLES['WL']==0 and VARIABLES['BP']<=18:
        VARIABLES['PO']="3 3/4"
        return 6030 ## 5720
    if VARIABLES['WL']==0 and VARIABLES['BP']<=20:
        VARIABLES['PO']="4 5/8"
        return 6030 ## 5730
    ## Logic rewritten
    if VARIABLES['TS'] in [3,6] and VARIABLES['WL']!=0 and VARIABLES['BP']<=21:
        VARIABLES['PO']="4 11/16"
        return 6030 ## 5740
    if VARIABLES['WL']!=0 and VARIABLES['BP']<=19:
        VARIABLES['PO']="4 11/16"
        return 6030 ## 5750
    if VARIABLES['WL']!=0 and VARIABLES['BP']<=22:
        VARIABLES['PO']="5 7/16"
        return 6030 ## 5760
    if VARIABLES['WL']!=0 and VARIABLES['BP']<=26:
        VARIABLES['PO']="6 1/16"
        return 6030 ## 5770
    VARIABLES['PO']="?"
    VARIABLES['GD']="SPECIAL"
    return 6030 ## 5780

if VARIABLES['EG']="N" : return 5870 (5790)

if BP<=16 : PO=4.5:VARIABLES['PO']="4 1/2":GOTO 5850 (5800)
if BP<=18 : PO=5.5:VARIABLES['PO']="5 1/2":GOTO 5850 (5810)
if BP<=20 : PO=6.5:VARIABLES['PO']="6 1/2":GOTO 5850 (5820)
if BP<=22 : PO=7.5:VARIABLES['PO']="7 1/2":GOTO 5850 (5830)
return 5780 (5840)

if NOT VARIABLES['BJT']="" : PO=PO-.5:VARIABLES['PO']=VARIABLES['STR'](PO):GOTO 6030 (5850)
return 6030 (5860)

if BP<=16 and CW<149 : SL=CW+3.5:VARIABLES['GD']="SN1":VARIABLES['PO']="4 5/8":GOTO 6030 (5870)
if BP<=16 and CW<221 : SL=CW+3.875:VARIABLES['GD']="SN2":VARIABLES['PO']="4 5/8":GOTO 6030 (5880)
if BP<=16 and CW<293 : SL=CW+4.5:VARIABLES['GD']="SG3":VARIABLES['PO']="4 5/8":GOTO 6030 (5890)
if BP<=16 and CW<=365 : SL=CW+5.5:VARIABLES['GD']="SG4":VARIABLES['PO']="4 5/8":GOTO 6030 (5900)
if BP<=16 : VARIABLES['PO']="4 5/8":GOTO 6030 (5910)
if BP<=18 and CW<149 : SL=CW+3.5:VARIABLES['GD']="SG5":VARIABLES['PO']="5 1/2":GOTO 6030 (5920)
if BP<=18 and CW<221 : SL=CW+4:VARIABLES['GD']="SG6":VARIABLES['PO']="5 1/2":GOTO 6030 (5930)
if BP<=18 and CW<293 : SL=CW+4.5:VARIABLES['GD']="SG7":VARIABLES['PO']="5 1/2":GOTO 6030 (5940)
if BP<=18 and CW<365 : SL=CW+5.5:VARIABLES['GD']="SG8":VARIABLES['PO']="5 1/2":GOTO 6030 (5950)
if BP<=18 : VARIABLES['PO']="5 1/2":GOTO 6030 (5960)
if BP<=20 and CW<149 : SL=CW+3.5:VARIABLES['GD']="SG9":VARIABLES['PO']="6 1/2":GOTO 6030 (5970)
if BP<=20 and CW<221 : SL=CW+3.875:VARIABLES['GD']="SG10":VARIABLES['PO']="6 1/2":GOTO 6030 (5980)
if BP<=20 and CW<293 : SL=CW+4.5:VARIABLES['GD']="SG11":VARIABLES['PO']="6 1/2":GOTO 6030 (5990)
if BP<=20 and CW<365 : SL=CW+5.5:VARIABLES['GD']="SG12":VARIABLES['PO']="6 1/2":GOTO 6030 (6000)
if BP<=20 : VARIABLES['PO']="6 1/2":GOTO 6030 (6010)
VARIABLES['PO']="?" (6020)

def L6030_set_ss_handle_solidbottomgrille_and_set_firedoor_hxp():
    """ Sets SS (???), Sets RL (???) and GR (???) for Solid Slats at Bottom of Grille, and Sets HPX (???) for Fire Door """
    ## SS: ???, SL: ???, SW: ???
    VARIABLES['SS']=(VARIABLES['SL']*VARIABLES['SW'])*.65
    ## TS:Type Slat, TS == SOLID SLATS AT BOTTOM OF ROLLING GRILLE
    if VARIABLES['TS']==5:
        VARIABLES['RL']=VARIABLES['SL']+1
        VARIABLES['GR']=VARIABLES['SL']+2 ## 6030
    ## DT == FIRE DOOR
    ## SH: Stop Height, US: Upset
    ## HXP: ???
    if VARIABLES['DT']==A[55] and (VARIABLES['SH']+VARIABLES['US']-.75)<=147:
        VARIABLES['HXP']=.75
        return 6070 ## 6040
    if VARIABLES['DT']==A[55] and (VARIABLES['SH']+VARIABLES['US']-1.75)<=168:
        VARIABLES['HXP']=1.75
        return 6070 ## 6050
    if VARIABLES['DT']==A[55] and (VARIABLES['SH']+VARIABLES['US']-2)>=168:
        VARIABLES['HXP']=2 ## 6060
    return 6070 ## Implicit

def L6070_():
    ## TS: Type Slat == SOLID SLATS AT BOTTOM OF ROLLING GRILLE, SBH: Slat Bottom Height
    ## SS: ??? Slat Weight Subtotal ???
    if VARIABLES['TS']==5 and VARIABLES['SBH']==0:
        VARIABLES['SS']=0 ## 6070
    
    ## BRACKET PLATE & ANGLE THICKNESS, SLAT LENGTH and GAGE ROD ADJUSTMENTS (6080)
    ## TS: Type Slat == 3-5/8 or 2-7/8 CROWN SLAT, NOEL: ???, HW: ???
    ## SL: Slat Length ???, EL: ???
    if VARIABLES['TS']<=2 and VARIABLES['NOEL']=="Y" and VARIABLES['HW']==0:
        VARIABLES['SL']=VARIABLES['SL']+1
        VARIABLES['EL']=0 ## 6090
    if VARIABLES['TS']==3 and VARIABLES['NOEL']=="Y" and VARIABLES['HW']==0:
        VARIABLES['SL']=VARIABLES['SL']+.25
        VARIABLES['EL']=0 ## 6100
    ## DT == FIRE DOOR
    if VARIABLES['DT']==A[55]:
        return 6160 ## 6110

    ## CIE: ???, TS: Type Slat == 2 1/2 INCH FLAT SLAT, WL: ???, HW: ???
    if VARIABLES['CIE']=="Y" and VARIABLES['TS']==3 and VARIABLES['WL']==0 and VARIABLES['HW']==0:
        VARIABLES['SL']=VARIABLES['SL']-.5
        VARIABLES['GR']=VARIABLES['SL']+1.75
        VARIABLES['EL']=.2857 ## 6120
    ## PW: ???, TB: ???, WAT: ???
    ## SL: Slat Length, RL: 
    if VARIABLES['HW']>=2750 or VARIABLES['HW']+VARIABLES['PW']>=4250:
        VARIABLES['TB_S']="1/2"
        VARIABLES['WAT']="3/8"
        VARIABLES['SL']=VARIABLES['SL']-.5
        VARIABLES['RL']=VARIABLES['RL']-.5
        VARIABLES['GR']=VARIABLES['GR']-.5
        return 6160 ## 6130
    if VARIABLES['HW']>1750 or VARIABLES['HW']+VARIABLES['PW']>2750:
        VARIABLES['TB_S']="3/8"
        VARIABLES['WAT']="5/16"
        VARIABLES['SL']=VARIABLES['SL']-.25
        VARIABLES['RL']=VARIABLES['RL']-.25
        VARIABLES['GR']=VARIABLES['GR']-.25
        return 6160 ## 6140
    VARIABLES['TB_S']="1/4"
    VARIABLES['WAT']="3/16"
    if VARIABLES['HW']>=1000 or VARIABLES['HW']+VARIABLES['PW']>=1750:
        VARIABLES['TB_S']="5/16"
        VARIABLES['WAT']="1/4"
        VARIABLES['SL']=VARIABLES['SL']-.125
        VARIABLES['RL']=VARIABLES['RL']-.125
        VARIABLES['GR']=VARIABLES['GR']-.125 ## 6150
    ## DT == FIRE DOOR, CW: Curtain Width?
    if VARIABLES['DT']==A[55] and ((VARIABLES['CW']*VARIABLES['SH'])/144)<=120:
        VARIABLES['TB']=.3125
        VARIABLES['TB_S']="5/16"
        VARIABLES['WAT']="1/4" ## 6160
    if VARIABLES['DT']==A[55] and ((VARIABLES['CW']*VARIABLES['SH'])/144)<=150:
        VARIABLES['TB']=.375
        VARIABLES['TB_S']="3/8"
        VARIABLES['WAT']="1/4" ## 6170
    if VARIABLES['DT']==A[55] and ((VARIABLES['CW']*VARIABLES['SH'])/144)>150:
        VARIABLES['TB']=.5
        VARIABLES['TB_S']="1/2"
        VARIABLES['WAT']="1/4" ## 6180
    ## PO: ???
    if VARIABLES['PO'] in ["4 1/2", "5 1/2", "6 1/2", "7 1/2"]:
        VARIABLES['WAT']="1/4" ## 6190
    if VARIABLES['PO']=="?":
        VARIABLES['WAT']="?" ## 6200
    ## Type Slat == SOLID SLATS AT BOTTOM OF ROLLING GRILLE, SBH: Slat Bottom Height, Bottom Bar != SPECIAL
    ## BBH: Bottom Bar Height?
    if VARIABLES['TS']==5 and VARIABLES['SBH']==0 and VARIABLES['BB']!="SPECIAL":
        VARIABLES['BBH']=3.5 ## 6210
    ## I don't know why we're truncating our precision... or rather why we're doing it __now__
    VARIABLES['RL']=int(VARIABLES['RL']*10000)/10000
    VARIABLES['SL']=int(VARIABLES['SL']*10000)/10000 ## 6220
    
    ## SOLID BOTTOM SLATS ## 6230
    ## SBH: Slat Bottom Height
    if VARIABLES['SBH']==0:
        return 6290 ## 6240

    ## BST: Bottom Slat Type == 3-5/8 INCH CROWN SLAT
    ## HS: Height Slat ???
    if VARIABLES['BST']=="#1":
        VARIABLES['HS']=3.625
        return 6270 ## 6250
    ## BST: Bottom Slat Type == 2-7/8 INCH CROWN SLAT
    if VARIABLES['BST']=="#2":
        VARIABLES['HS']=2.875 ## 6260

    ## NBS: ???, SBS: ???, M:???
    VARIABLES['NBS']=math.ceil((VARIABLES['SBH']-VARIABLES['BBH']-1.5)/VARIABLES['HS'])
    VARIABLES['SBS']=(VARIABLES['NBS']*VARIABLES['HS'])+VARIABLES['BBH']+1.5 ## 6270
    if VARIABLES['M']!=0 and VARIABLES['SBS']!=0:
        VARIABLES['BBH']=0 ## 6280
    ## DT == FIRE DOOR
    if VARIABLES['DT']!=A[55]:
        return 6320 ## 6290

    ## BO: Bottom Bar Option == None/Null, CW: Curtain Width ???
    if VARIABLES['BO']==0 and VARIABLES['CW']<=192:
        VARIABLES['AW']=3.3
        ## BB: Bottom Bar = 2" x 2" x 1/8" STEEL
        VARIABLES['BB']=A[83]
        VARIABLES['BBH']=2.5
        return 6430 ## 6300
    if VARIABLES['BO']==0 and VARIABLES['CW']>192:
        VARIABLES['AW']=5.5
        ## Bottom Bar = 2 1/2" x 2" x 3/16" (STL)
        VARIABLES['BB']=A[18]
        VARIABLES['BBH']=2.5
        return 6430 ## 6310
    if VARIABLES['BO']==0 and VARIABLES['CW']<=235.5:
        VARIABLES['AW']=3.3
        ## Bottom Bar = 2" x 2" x 1/8" STEEL
        VARIABLES['BB']=A[83]
        VARIABLES['BBH']=2.5 ## 6320
    ## TS: Type Slat == PERFORATED SLATS
    if VARIABLES['TS']==6 and VARIABLES['BO']==0 and VARIABLES['CW']<=235.5:
        VARIABLES['AW']=3.72
        ## ????? I have no idea why this isn't a proper variable...
        VARIABLES['BB']="2 1/2 x 2 x 1/8"
        VARIABLES['BBH']=3 ## 6330
    if VARIABLES['BO']==0 and VARIABLES['CW']>235.5 and VARIABLES['CW']<=312.125:
        VARIABLES['AW']=5.5
        ## Bottom Bar = 2 1/2" x 2" x 3/16" (STL)
        VARIABLES['BB']=A[18]
        VARIABLES['BBH']=2.5 ## 6340
    if VARIABLES['BO']==0 and VARIABLES['CW']>312.125:
        VARIABLES['AW']=6.2
        ## Bottom Bar = 3" x 2" x 3/16" (STEEL)
        VARIABLES['BB']=A[19]
        VARIABLES['BBH']=2.5 ## 6350
    ## UTC: ???, SD1: ???
    if VARIABLES['UTC']=="Y":
        VARIABLES['BBH']=VARIABLES['BBH']+(VARIABLES['SD1']+1.5) ## 6360
    if VARIABLES['UTC']=="N":
        VARIABLES['BBH']=VARIABLES['BBH']+1.5 ## 6370
    ## Type Slat != SOLID SLATS AT BOTTOM OF ROLLING GRILLE
    if VARIABLES['TS']!=5:
        return 6480 ## 6380

    if VARIABLES['TS']==5:
        VARIABLES['RW']=.02544
        if VARIABLES['HS']==0:
            VARIABLES['HS']=3.625 ## 6390
    ## NR: ???, SH: Stop Height, US: Upset, RS: ???
    VARIABLES['NR']=math.ceil((
        (VARIABLES['SH']+VARIABLES['US']-VARIABLES['SBS']-VARIABLES['BBH'])/
            VARIABLES['RS'])
                                +1) ## 6400
    ## EG: Extruded Guides
    if VARIABLES['EG']=="Y":
        VARIABLES['NR']=math.ceil((
            (VARIABLES['SH']+VARIABLES['US']+1.25-VARIABLES['BBH'])/
                VARIABLES['RS'])
                                    +1) ## 6410
    if VARIABLES['SBS']!=0:
        return L6440_handle_SBS() ## 6420
    ## NS: ???
    ## Removed a bunch of extraneous parens
    VARIABLES['NS']=(VARIABLES['HC']-VARIABLES['BBH']-1.5-(VARIABLES['NR']-1)*VARIABLES['RS'])/VARIABLES['HS']
    return  6450 ## 6430

def L6440_handle_SBS():
    """ Adjusts NS (???) to account for an SBS (???) """
    ## NS: ???, HC: ???, SBS: ???, NR: ???, HS: Height Slat, NBS: ???
    ## Removed a bunch of extraneous parens
    VARIABLES['NS']=((VARIABLES['HC']-VARIABLES['SBS']-1.5-(VARIABLES['NR']-1)*VARIABLES['RS'])/VARIABLES['HS'])+VARIABLES['NBS'] ## 6440
    return L6450_() ## Implicit

def L6450_():
    ## MF: ??? in (MILL ALUMINUM, ANODIZED ALUMINUM, DURANODIC ALUMINUM), RW: ???
    if VARIABLES['MF'] in (A[69], A[71], A[72]):
        VARIABLES['RW']=.0272176 ## 6450
    ## MF[-13:] == LEXAN INSERTS
    if VARIABLES['MF'][-13:]==A[90]:
            VARIABLES['RW']=.0355171 ## 6460
        
    ## GW: ???, NR: ???, RL: ???
    ## We're removing precision... for some reason...Also, I removed a set of parens
    VARIABLES['GW']=truncate(VARIABLES['NR'] * VARIABLES['RL'] * VARIABLES['RW'])
    return 6630 ## 6470

## VISION SECTION (GRILLE) (6480)
if OGS=0 : return 6510 else: VARIABLES['ST']="#"+VARIABLES['STR'](TS) (6490)

RL=SL+1:NR=CINT(OGS/2.25)+1:GS=(NR-1)*2.25:NBS=CINT(((VCL-(GS/2))-BBH-1.5)/HS):NS=(((HC-GS-BBH-3)-(NBS*HS))/HS)+NBS:GOTO 6630 (6500)
if TS=6 : BBH=3:NS=INT(((HC-BBH)/HS)*100)/100:GOTO 6530 (6510)
NS=INT(((HC-BBH)/HS)*100)/100 (6520)
## PASS DOOR SLATS (6530)
if VARIABLES['PD']="" : return 6630 (6540)

if VARIABLES['PD']="2L" or VARIABLES['PD']="2R" : BSL=SL-37.125 (6550)
if VARIABLES['PD']="3L" or VARIABLES['PD']="3R" : BSL=SL-43.125 (6560)
if TS=1 : NBS=23:NTS=NS-23 (6570)
if TS=2 : NBS=29:NTS=NS-29 (6580)
if TS=3 : NBS=33:NTS=NS-33 (6590)
if TS=4 : NBS=42:NTS=NS-42 (6600)
if TS=6 : NBS=33:NTS=NS-33 (6610)

def L6630_():
    ## SLOPED BOTTOM BAR ## 6620
    ## (Above line assumed to accomany this function)
    ## SD1: ???, SD2: ??? Placeholder for SD1 ???, SL: Slat Length ???
    ## SP1: ???, SP2/3: ??? Placeholder for SP1 ???, SPW: ???
    if  VARIABLES['SD1']!=0:
        VARIABLES['SD2']= VARIABLES['SD1']+3
        VARIABLES['SP1']= VARIABLES['SD2']*( VARIABLES['SL']+1)
        VARIABLES['SP2']= VARIABLES['SD1']*(( VARIABLES['SL']+1)/2)
        VARIABLES['SP3']=(( VARIABLES['SP1']- VARIABLES['SP2'])/144)*5
        VARIABLES['SPW']= VARIABLES['SP3']+(( VARIABLES['SL']+1)*.05316) ## 6630
    ## This line was already commented
    ##  if TS=6 : return 6550 ## 6640

    ## This line was already commented and seems to have possibly been the original equation
    ##  BB=INT(((((CW-3)/12)*(AW+.5))+(SW*SL)+SPW)*100)/100 ## 6660

    ## BB: Bottom Bar, AW: Angle Weigth (/foot), SE: Safety Edge, AS: ???
    ## SL: Slat Length, SS: Slat Weight Subtotal ?
    ## Again, we're truncating precision
    VARIABLES['BB']=truncate(
            (VARIABLES['AW']+VARIABLES['SE']+VARIABLES['AS'])
        * (VARIABLES['SL']/12)+VARIABLES['SPW']+VARIABLES['SS'])
                            
    ## The GOTO/return here seems oddly out of
    ## place given the rest of the way this is coded...
    return 6670 ## 6650
        
def L6670_():
    ## PD: ???, BB: Bottom Bar, SL: Slat length?
    if VARIABLES['PD'] in ("2L", "2R"):
        ## Removed extra parens
        VARIABLES['BB']=VARIABLES['BB']/VARIABLES['SL']*(VARIABLES['SL']-37.125) ## 6670
    if VARIABLES['PD'] in ("3L","3R"):
        VARIABLES['BB']=(VARIABLES['BB']/VARIABLES['SL'])*(VARIABLES['SL']-43.125) ## 6680
    ## EL: Endlocks TS: Type Slat == 3 5/8 INCH CROWN SLAT
    if VARIABLES['EL']==0 and VARIABLES['TS']==1 :
        VARIABLES['EL']=.21875 ## 6690
    ## DT == FIRE DOOR
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==1:
        VARIABLES['EL']=.45
        return 6800 ## 6700
    ## TS == 2 7/8 INCH CROWN SLAT
    if VARIABLES['DT']==A[55] and VARIABLES['TS']==2:
        VARIABLES['EL']=.4375
        return 6800 ## 6710
    ## WL: ???, NS: ???
    if VARIABLES['EL']==0 and VARIABLES['TS']==2:
        VARIABLES['EL']=.17
        if VARIABLES['WL']>0:
            ## Look... I think we can all agree that NS/NS = 1... And literally
            ## all those parens are unnecessary, but because I'm paranoid I'm
            ## going to leave this next line as is...
            VARIABLES['EL']=(((VARIABLES['NS']/VARIABLES['WL'])*.656)/VARIABLES['NS'])+.17 ## 6720
    ## TS == 2 1/2 INCH FLAT SLAT
    if VARIABLES['TS']==3 and VARIABLES['EL']==0:
        VARIABLES['EL']=.09375 ## 6730
    ## TS == MIDGET CROWN SLAT < 2 INCH >
    if VARIABLES['TS']==4 and VARIABLES['EL']==0:
        VARIABLES['EL']=.125 ## 6740
    ## TS == PERFORATED SLATS
    if VARIABLES['TS']==6:
        VARIABLES['EL']=.25
        if VARIABLES['WL']>0:
            ## Float below was in float notation, and- as in L6720- I'm just not going to touch this
            VARIABLES['EL']=((VARIABLES['WL']*float("9.399999E-02"))/VARIABLES['NS'])+.25 ## 6750
    ## GS: ???
    if VARIABLES['GS']!=0:
        ## NS: ???, SL: Slat Length?, SW: Slat Weight ???, BB: Bottom Bar
        ## NR: ???, RL: ???, RW: ???
        VARIABLES['HW']=truncate((VARIABLES['NS']*VARIABLES['SL']*VARIABLES['SW']+VARIABLES['BB'])
                                    +(VARIABLES['NS']*VARIABLES['EL'])
                                    +(VARIABLES['NR']*VARIABLES['RL']*VARIABLES['RW']))
        return 6840 ## 6760
    ## TS == SOLID SLATS AT BOTTOM OF ROLLING GRILLE
    if VARIABLES['TS']==5:
        VARIABLES['HW']=truncate(VARIABLES['NR']*VARIABLES['RL']*VARIABLES['RW']
                                    +(VARIABLES['SL']*VARIABLES['SW']*VARIABLES['NS']
                                    +(VARIABLES['NS']*VARIABLES['EL']))
                                    +VARIABLES['BB'])
        return 6840 ## 6770
    ## TS == PERFORATED SLATS
    if VARIABLES['TS']==6:
        ## NOTE! We're truncating by 4 decimal places instead of 2!
        ## No, I don't know why
        VARIABLES['HW']=truncate(VARIABLES['NS']*VARIABLES['SL']*VARIABLES['SW']+VARIABLES['BB']
                                    +(VARIABLES['NS']*VARIABLES['EL']),
                                    1000)
        return 6840 ## 6780

    if VARIABLES['PD']!="":
        ## NTS: ???, NBS: ???, BSL: Bottom Slat Length???
        ## See above about not touching equations in this area >.>
        VARIABLES['HW']=truncate((((VARIABLES['NTS']*VARIABLES['SL'])+(VARIABLES['NBS']*VARIABLES['BSL']))
                                    *VARIABLES['SW'])
                                    +(VARIABLES['NS']*VARIABLES['EL'])+VARIABLES['BB'])
        return 6840 ## 6790
    ## PSH: Perforated Slat Height, PSCL: Perforated Slat Center Line
    if VARIABLES['PSH']==0 and VARIABLES['PSCL']==0:
        ## OMG! ACTUAL DOCUMENTATION ON WHAT AN ABBREVIATION MEANS!!!
        return 6830 ## REM: PERFORATED SLATS WEIGHT LOSS (PSWL) ## 6800

    ## NPS: ???, HS: Height Slat
    ## smh, these random truncations and rounding
    VARIABLES['NPS']=math.ceil(truncate(VARIABLES['PSH']/VARIABLES['HS']))
    ## NPPS: Number Perferations per Slat?, CW: Curtain Width?
    VARIABLES['NPPS']=math.ceil(truncate((VARIABLES['CW']/8.5)-2))
    ## PSWL: Perforated Slat Weight Loss, SW: ??? 
    ## Alright, screw it, this is actually, literally absurd, I'm destroying these parens
    VARIABLES['PSWL']=VARIABLES['SW']/5.25*4.648175*VARIABLES['NPPS']*VARIABLES['NPS']
    ## FPSFB: ???, BBH: Bottom Bar Height
    ## AND AGAIN! >:D
    VARIABLES['FPSFB']=math.ceil(truncate((VARIABLES['PSCL']-VARIABLES['PSH']/2-VARIABLES['BBH'])/VARIABLES['HS']+1)) ## 6810
    ## FPFE: ???, SL: Slat Length
    ## More parens fell this day
    VARIABLES['FPFE']=(VARIABLES['SL']-VARIABLES['NPPS']*5.5-(VARIABLES['NPPS']-1)*3)/2 ## 6820
    VARIABLES['HW']=truncate(VARIABLES['NS']*VARIABLES['SL']*VARIABLES['SW']+VARIABLES['BB']+(VARIABLES['NS']*VARIABLES['EL'])-VARIABLES['PSWL']) ## 6830
    ## M: Maximum Deflextion Weight
    if VARIABLES['M']==0:
        return 6890 ## 6840

    ## PW: Pipe Weight
    if VARIABLES['HW']+VARIABLES['PW']>=VARIABLES['M']*.97:
        return 6890 ## 6850

    ## SBS: ???
    if VARIABLES['SBS']!=0:
        return 8060 ## 6860

    ## TS: Type Slat == SOLID SLATS AT BOTTOM OF ROLLING GRILLE
    if VARIABLES['TS']==5:
        return 8060 ## 6870

    return 8090 ## 6880

if NOT LSP=0 : X=LSP else: X=1 (6890)
FOR P=X TO 11 (6900)
if P=1 : return 7020 (6910)

if P=2 : return 7030 (6920)

if P=3 : return 7040 (6930)

if P=4 : return 7050 (6940)

if P=5 : return 7060 (6950)

if P=6 : return 7070 (6960)

if P=7 : return 7080 (6970)

if P=8 : return 7090 (6980)

if P=9 : return 7100 (6990)

if P=10 : return 7110 (7000)

if P=11 : return 7120 (7010)

I4=5.86:WT=8.56*2.5:GOTO 7130 (7020)
I4=7.23:WT=10.79*2:GOTO 7130 (7030)
I4=19.71:WT=12.93*2.93:GOTO 7130 (7040)
I4=28.1:WT=18.97*1.75:GOTO 7130 (7050)
I4=72.5:WT=28.55*1.7:GOTO 7130 (7060)
I4=161:WT=40.48*1.7:GOTO 7130 (7070)
I4=279:WT=49.56*2:GOTO 7130 (7080)
I4=372:WT=54.57+50:GOTO 7130 (7090)
I4=428:WT=63.37+50:GOTO 7130 (7100)
I4=561:WT=62.58+55:GOTO 7130 (7110)
I4=730:WT=82.77+55:GOTO 7130 (7120)
WO=CW/12 (7130)
M=(I4/(WO*WO))*38667! (7140)
PW=WT*WO (7150)
MW=HW+PW (7160)
if MW<=M*.97 and P=1 : VARIABLES['P']=A[41]:IL=4.25:VARIABLES['IS']="1 1/4":GOTO 7300 (7170)
if MW<=M*.97 and P=2 : VARIABLES['P']=A[42]:IL=4.25:VARIABLES['IS']="1 1/4":GOTO 7300 (7180)
if MW<=M*.97 and P=3 : VARIABLES['P']=A[43]:IL=4.25:VARIABLES['IS']="1 1/2":GOTO 7310 (7190)
if MW<=M*.97 and P=4 : VARIABLES['P']=A[44]:IL=4.25:VARIABLES['IS']="1 1/2":GOTO 7310 (7200)
if MW<=M*.97 and P=5 : VARIABLES['P']=A[45]:IL=4.3125:VARIABLES['IS']="1 3/4":GOTO 7320 (7210)
if MW<=M*.97 and P=6 : VARIABLES['P']=A[46]:IL=5.375:VARIABLES['IS']="2":GOTO 7320 (7220)
if MW<=M*.97 and P=7 : VARIABLES['P']=A[47]:IL=6.375:VARIABLES['IS']="2 1/2":GOTO 7320 (7230)
if MW<=M*.97 and P=8 : VARIABLES['P']=A[48]:IL=7:VARIABLES['IS']="3":GOTO 7320 (7240)
if MW<=M*.97 and P=9 : VARIABLES['P']=A[49]:IL=7:VARIABLES['IS']="3":GOTO 7320 (7250)
if MW<=M*.97 and P=10 : VARIABLES['P']=A[50]:IL=8:VARIABLES['IS']="3":GOTO 7320 (7260)
if MW<=M*.97 and P=11 : VARIABLES['P']=A[51]:IL=8:VARIABLES['IS']="3":GOTO 7320 (7270)
NEXT P (7280)
print(:BEEP:print("****** WEIGHT & SPAN EXCEED 16 INCH PIPE. CAN NOT CONTINUE PROGRAM ******":END (7290)
if PR=1 : IL=2.25:GOTO 7320 (7300)
if PR=1 : IL=3.3125 (7310)
if NOT VARIABLES['IL']="" : IL=VAL(VARIABLES['IL']) (7320)
T=1:Q=2*3.1416*IL*T:J=IR*T^2*3.1416:Y=(-SH+LTBB) (7330)
C=Q^2-4*J*Y:Q1=(-Q+SQR(C))/(2*J) (7340)
GOSUB 7390 (7350)
if NOT LGBP=0 : BP=LGBP (7360)
if IL=4.25 : GOSUB 7420:GOSUB 7630:GOSUB 7690:GOTO 5600 (7370)
GOSUB 7670:GOSUB 7630:GOSUB 7690:GOTO 5600 (7380)
VARIABLES['Q1']=VARIABLES['STR'](Q1):VARIABLES['Q2']=VARIABLES['LEFT'](VARIABLES['Q1'],6):A=INT(Q1):FOR X=1 TO 4 (7390)
if VARIABLES['MID'](VARIABLES['Q2'],X,1)="."THEN VARIABLES['Q3']=VARIABLES['RIGHT'](VARIABLES['Q2'],7-X):FX=VAL(VARIABLES['Q3']):TR=VAL(VARIABLES['Q2']):RETURN (7400)
NEXT X (7410)
if FX<=.02 : F1=IL+(IR*(A-1)):RETURN (7420)
if FX<=.07 : F1=4.287+(IR*(A-1)):RETURN (7430)
if FX<=.12 : F1=4.325+(IR*(A-1)):RETURN (7440)
if FX<=.17 : F1=4.362+(IR*(A-1)):RETURN (7450)
if FX<=.22 : F1=4.4+(IR*(A-1)):RETURN (7460)
if FX<=.24 : F1=4.437+(IR*(A-1)):RETURN (7470)
if FX<=.27 : F1=3.725+(IR*A):RETURN (7480)
if FX<=.32 : F1=3.725+(IR*A):RETURN (7490)
if FX<=.42 : F1=3.8+(IR*A):RETURN (7500)
if FX<=.47 : F1=3.837+(IR*A):RETURN (7510)
if FX<=.52 : F1=3.875+(IR*A):RETURN (7520)
if FX<=.57 : F1=3.912+(IR*A):RETURN (7530)
if FX<=.62 : F1=3.95+(IR*A):RETURN (7540)
if FX<=.67 : F1=3.987+(IR*A):RETURN (7550)
if FX<=.7200001 : F1=4.025+(IR*A):RETURN (7560)
if FX<=.77 : F1=4.062+(IR*A):RETURN (7570)
if FX<=.82 : F1=4.1+(IR*A):RETURN (7580)
if FX<=.87 : F1=4.137+(IR*A):RETURN (7590)
if FX<=.92 : F1=4.175+(IR*A):RETURN (7600)
if FX<=.97 : F1=4.212+(IR*A):RETURN (7610)
if FX>.97 : F1=4.25+(IR*A):RETURN (7620)
if TS=1 or TS=5 : FL=INT((F1+.5625)*100)/100:RETURN (7630)
if TS=2 : FL=INT((F1+.625)*100)/100:RETURN (7640)
if TS=3 or TS=6 : FL=INT((F1+.75)*100)/100:RETURN (7650)
if TS=4 : FL=INT((F1+.5)*100)/100:RETURN (7660)
if FX<=.24 : F1=IL+(IR*(A-1)):RETURN (7670)
F1=IL+(IR*A):RETURN (7680)
if NOT LGBP=0 : BP=LGBP:RETURN (7690)
if TS=1 : BP=(FL+1)*2:GOTO 7740 (7695)
if TS=2 : BP=(FL+1.1)*2:GOTO 7740 (7700)
if TS=3 : BP=(FL+1.215)*2:GOTO 7740 (7710)
if TS=4 : BP=(FL+.938)*2:GOTO 7740 (7720)
if TS=5 or TS=6 : BP=(FL+1.315)*2:GOTO 7740 (7730)
if WL=6 : BP=BP+1:GOTO 7770 (7740)
if WL=4 : BP=BP+1.5:GOTO 7770 (7750)
if WL=2 : BP=BP+2:GOTO 7770 (7760)
if PR=1 and BP<=12.01 : BP=12:RETURN (7770)
if SB=1 and BP<=12.01 : BP=12:RETURN (7780)
if PR=1 and BP<=13.01 : BP=13:RETURN (7790)
if SB=1 and BP<=13.01 : BP=13:RETURN (7800)
if PR=1 and BP<=14.01 : BP=14:RETURN (7810)
if SB=1 and BP<=14.01 : BP=14:RETURN (7820)
if PR=1 and BP<=15.01 : BP=15:RETURN (7830)
if SB=1 and BP<=15.01 : BP=15:RETURN (7840)
if BP<=16.01 : BP=16:RETURN (7850)
if PR=1 and BP>16.01 and BP<=17.01 : BP=17:RETURN (7860)
if SB=1 and BP>16.01 and BP<=17.01 : BP=17:RETURN (7870)
if BP>=16.01 and BP<=18.01 : BP=18:RETURN (7880)
if PR=1 and BP>18.01 and BP<=19.01 : BP=19:RETURN (7890)
if SB=1 and BP>18.01 and BP<=19.01 : BP=19:RETURN (7900)
if BP>=18.01 and BP<=20.01 : BP=20:RETURN (7910)
if BP>=20.01 and BP<=21.01 : BP=21:RETURN (7920)
if BP>=21.01 and BP<=22.01 : BP=22:RETURN (7930)
if BP>=22.01 and BP<=23.01 : BP=23:RETURN (7940)
if BP>=23.01 and BP<=24.01 : BP=24:RETURN (7950)
if BP>=24.01 and BP<=25.01 : BP=25:RETURN (7960)
if BP>=25.01 and BP<=26.01 : BP=26:RETURN (7970)
if BP>=26.01 and BP<=27.01 : BP=27:RETURN (7980)
if BP>=27.01 and BP<=28.01 : BP=28:RETURN (7990)
if BP>=28.01 and BP<=29.01 : BP=29:RETURN (8000)
if BP>=29.01 and BP<=30.01 : BP=30:RETURN (8010)
if BP>=30.01 and BP<=31.01 : BP=31:RETURN (8020)
if BP>=31.01 and BP<=32.01 : BP=32:RETURN (8030)
if BP>=32.01 and BP<=33.01 : BP=33:RETURN (8040)
BEEP:print(:print("*** DOOR HEIGHT EXCEEDS PROGRAM LIMITS <33 INCH BRACKET>. CAN NOT CONTINUE ***":END (8050)
if NOT SBH=0 and HC-SH>SBS : return 8130 (8060)

if TS=5 and NOT SBH=0 : return 8120 (8070)

if TS=5 and SBH=0 : return 8100 (8080)

def L8090_validate_PD():
    """ A simple fork that checks if PD is set yet """
    if VARIABLES['PD']!="":
        return 8110
    else:
        return 8120 ## 8090

WU=INT((RW*(((HC-SH-BBH)/RS)*RL)+BB)*100)/100:GOTO 8140 (8100)
def L8110_set_WU():
    """ Simply sets WU """
    ## WU: ???, HC: Pipe Center Line, SH: Stop Height, BBH: Bottom Bar Height
    ## HS: Height Slat???, BS: Bottom Slat Length ???, SW: ???
    ## BB: Bottom Bar
    ## Parens removed
    VARIABLES['WU']=truncate((VARIABLES['HC']-VARIABLES['SH']-VARIABLES['BBH'])
                                /VARIABLES['HS']*VARIABLES['BSL']*VARIABLES['SW']
                                +BB)
    return 8140 ## 8110
WU=INT((SW*(((HC-SH-BBH)/HS)*SL)+BB)*100)/100:GOTO 8140 (8120)
WU=INT(((((HC-SH-SBS)/2.25)*RL*RW)+((NBS*SL)*SW)+BB)*100)/100 (8130)

def L8140_update_WU():
    """ Updates WU based on SH and WU """
    ## SH: Stop Height, WU: ???
    if VARIABLES['SH']>=192:
        VARIABLES['WU']=VARIABLES['WU']*1.2
        return 8180 ## 8140
    if VARIABLES['WU']<=50:
        VARIABLES['WU']=VARIABLES['WU']+5
        return 8180 ## 8150
    if VARIABLES['WU']>50 and VARIABLES['WU']<100:
        VARIABLES['WU']=VARIABLES['WU']+10
        return 8180 ## 8160
    if VARIABLES['WU']>=100:
        VARIABLES['WU']=VARIABLES['WU']*1.1 ## 8170
    return L8180 ## Implicit
    
def L8180_():
    ## TD: ???, IL: ???, HW: ???
    VARIABLES['TD']=truncate(VARIABLES['IL']*VARIABLES['HW'])
    ## PRD: ???
    if VARIABLES['PRD']=="Y":
        VARIABLES['TD']=VARIABLES['TD']*1.33 ## 8180
    ## DT: Door Type == FIRE DOOR
    if VARIABLES['DT']==A[55]:
        VARIABLES['TD']=VARIABLES['TD']*1.1 ## 8190
    ## TU: ???, FL: ???, WU: ???
    VARIABLES['TU']=truncate(VARIABLES['FL']*VARIABLES['WU'])
    ## IP: ???, TR: ???
    VARIABLES['IP']=(VARIABLES['TD']-VARIABLES['TU'])/VARIABLES['TR'] ## 8200
    ## PT: ???
    VARIABLES['PT']=truncate(VARIABLES['TU']/VARIABLES['IP'])
    ## X1: Integer Part of PT, X2 Decimal Part of PT
    X1=int(PT)
    X2=truncate(PT-X1,1000) ## 8210
    ## AJ: 
    if VARIABLES['AJ']==0:
        VARIABLES['AJ']=6
        L8240_round_PT()
        return 8380 ## 8220
    if VARIABLES['AJ']==4:
        ## TT: String rep of TR + PT
        VARIABLES['TT']=str(truncate(VARIABLES['TR']+VARIABLES['PT']))
        L8310_roundup_TT()
        return 8440 ## 8230
    ## This function seems to randomly flow into 8240 if AJ != 0 or 4 >.>
    ## This is almost certainly wrong, but I'll do it for completeness sake
    return L8240_round_PT()
    
def L8240_round_PT():
    """ Round PT to nearest 1/6th"""
    ## X2: Decimal Container for PT, PT: ???, X1: Integer Container for PT
    if VARIABLES['X2']<=.07:
        VARIABLES['PT']=VARIABLES['X1']
        return ## 8240
    if VARIABLES['X2']>=.07 and VARIABLES['X2']<=.23:
        VARIABLES['PT']=VARIABLES['X1']+.1666
        return ## 8250
    if VARIABLES['X2']>=.23 and VARIABLES['X2']<=.4:
        VARIABLES['PT']=VARIABLES['X1']+.3333
        return ## 8260
    if VARIABLES['X2']>=.4 and VARIABLES['X2']<=.57:
        VARIABLES['PT']=VARIABLES['X1']+.5
        return ## 8270
    if VARIABLES['X2']>=.57 and VARIABLES['X2']<=.73:
        VARIABLES['PT']=VARIABLES['X1']+.6666
        return ## 8280
    if VARIABLES['X2']>=.73 and VARIABLES['X2']<=.9:
        VARIABLES['PT']=VARIABLES['X1']+.8333
        return ## 8290
    if VARIABLES['X2']>=.9:
        VARIABLES['PT']=VARIABLES['X1']+1
        return ## 8300

def L8310_roundup_TT():
    """ Rounds up TT to nearest 1/4 """
    ## FT: Truncation of TT, TT: String rep of TR + PT
    VARIABLES['FT']=VARIABLES['TT'][-3:]
    ## X3: Decimal Container for FT ???
    if len(VARIABLES['FT'])<3:
        VARIABLES['X3']=0
        return L8370_reassemble_TT_get_PT_IP() ## 8310
    ## X2: Decimal Container for FT???
    VARIABLES['X2']=float(VARIABLES['FT'])
    if VARIABLES['X2']<=.1:
        VARIABLES['X3']=0
        return L8370_reassemble_TT_get_PT_IP() ## 8320
    if VARIABLES['X2']>=.85:
        VARIABLES['X3']=1
        return L8370_reassemble_TT_get_PT_IP() ## 8330
    if VARIABLES['X2']>=.6:
        VARIABLES['X3']=.75
        return L8370_reassemble_TT_get_PT_IP() ## 8340
    if VARIABLES['X2']>=.35:
        VARIABLES['X3]'=.5
        return L8370_reassemble_TT_get_PT_IP() ## 8350
    if VARIABLES['X2']<=.1:
        VARIABLES['X3']=.25 ## 8360
    return L8370_reassemble_TT_get_PT_IP() ## Implicit

def L8370_reassemble_TT_get_PT_IP():
    """Recombine the parts of TT and generate PT and IP """
    ## TT: ??? (TR + PT), X3: Rounding Portion of FT
    ## ... yes, that says to truncate 1... I didn't write the code...
    VARIABLES['TT']=truncate(float(VARIABLES['TT']),1)+VARIABLES['X3']
    ## PT: ??? (TU/IP), TR: ???
    VARIABLES['PT']=trunacate(VARIABLES['TT']-VARIABLES['TR'])
    ## IP: ???, TD: ??? (IL*HW)
    VARIABLES['IP']=VARIABLES['TD']/VARIABLES['TT']
    return ## 8370

TT=INT((TR+PT)*100)/100:IP=INT((TD/TT)*100)/100 (8380)
if VARIABLES['DT']=A[55] : return 8450 (8390)

if VARIABLES['IS']="1 1/4" or VARIABLES['IS']="1 1/2" : PL=GR-6.5 (8400)
if VARIABLES['IS']="1 3/4" : PL=GR-7 (8410)
if VARIABLES['IS']="2" : PL=GR-8 (8420)
if VARIABLES['IS']="2 1/2" or VARIABLES['IS']="3" : PL=GR-13 (8430)

def L8440_():
    ## AJ: ???, PL: ???, GR: ???
    if VARIABLES['AJ']==4:
        VARIABLES['PL']=VARIABLES['GR']-9 ## 8440
    "CLS"
    ## CW: Curtain Width
    format_float_as_measurement("CW")
    ## SH: Stop Height
    format_float_as_measurement("SH")
    print("CLEAR OPENING WIDTH: VARIABLES['CW'] \t HEIGHT TO STOPS: VARIABLES['SH']") ## 8450
    ## TNS: ???, IL: ???, AJF: ???, HS: Height Slat?, NS: ???
    VARIABLES['TNS']=math.ceil((2*3.1416*VARIABLES['IL']*(.6600001-VARIABLES['AJF'])/VARIABLES['HS'])+VARIABLES['NS'])
    ## NTS: ???, TNS: ???, NBS: ???
    VARIABLES['NTS']=math.ceil(VARIABLES['TNS']-VARIABLES['NBS']) ## 8460
    ## PL: ???
    format_float_as_measurement("PL")
    ## P: ???, IS: Inner Shaft
    print('VARIABLES["P"] x VARIABLES["PL"] \t INNER SHAFT: VARIABLES["IS"]"') ## 8470
    ## TS: Type Slat in (3 5/8 INCH CROWN SLAT,2 7/8 INCH CROWN SLAT,2 1/2 INCH FLAT SLAT,MIDGET CROWN SLAT < 2 INCH >)
    ## GS: ???, TS == PERFORATED SLATS
    ## Added Parens
    if (VARIABLES['TS']<=4 and VARIABLES['GS']==0) or VARIABLES['TS']==6:
        return 8690 ## 8480

    ## GP: Vision Section GRILLE PATTERN, TL: ???, LC: 
    if VARIABLES['GP']=="ASL":
        VARIABLES['TL']=4.5
        VARIABLES['LC']=4.625
        return 8520 ## 8490
    if VARIABLES['GP']=="CSL":
        VARIABLES['TL']=9
        VARIABLES['LC']=9.25 ## 8500
    ## MF == LEXAN INSERTS
    if VARIABLES['GP']=="CSL" and VARIABLES['MF'][-13:]==A[90]:
        VARIABLES['TL']=9
        VARIABLES['LC']=9.375
        return 8550 ## 8510
    ## R1: ???, RL: ???
    VARIABLES['R1']=truncate(VARIABLES['RL']-1,10000)
    L8610_() ## 8520
    ## LL: ???, FT: ???, TL: ???
    ## NT: ???, N2: ???
    if VARIABLES['LL']>2:
        VARIABLES['FT']=truncate((VARIABLES['TL']+VARIABLES['LL']-.125)/2,10000)
        VARIABLES['NT']=VARIABLES['N2']-1
        return 8570 ## 8530
    return 8570 ## 8540

R1=INT((RL-.875)*10000)/10000:GOSUB 8610 (8550)
if LL>2 : FT=INT((((TL+LL)-.25)/2)*10000)/10000:NT=N2-1 (8560)

def L8570_():
    ## Bottom Bar ==  STANDARD TUBULAR ALUMINUM, SBH: Slat Bottom Height, VCL: Vertical Center Line?
    ## TST: ???, NR: ???, NT: ???
    ## TNT: ???, TST: ???, NR: ???
    if VARIABLES['BB'][16:]==A[81] or VARIABLES['SBH']!=0 or VARIABLES['VCL']!=0:
        VARIABLES['TST']=(VARIABLES['NR']-2)*VARIABLES['NT']
        VARIABLES['TNT']=VARIABLES['TST']+(VARIABLES['NR']-2)*2
        return L8590_() ## 8570

    VARIABLES['TST']=(VARIABLES['NR']-1)*VARIABLES['NT']
    VARIABLES['TNT']=VARIABLES['TST']+(VARIABLES['NR']-1)*2 ## 8580
    return L8590_() ## Implicit

def L8590_():
    ## GP: Vision Section GRILLE PATTERN
    ## PF: ???, FT: ???, NT: ???, LC: ???
    ## TNL: ???, TNT: ???, NR: ???
    if VARIABLES['GP']=="ASL":
        VARIABLES['PF']=1.25+2*VARIABLES['FT']+VARIABLES['NT']*VARIABLES['LC']
        VARIABLES['TNL']=VARIABLES['TNT']/2+(VARIABLES['NR']-1)*3
        return 8640 ## 8590
    if VARIABLES['GP']=="CSL":
        VARIABLES['PF']=1.375+2*VARIABLES['FT']+VARIABLES['NT']*VARIABLES['LC']
        VARIABLES['TNL']=VARIABLES['TNT']+(VARIABLES['NR']-1)*2
        return 8640 ## 8600
    ## N1: ???, R1: ???, LC: ???
    VARIABLES['N1']=truncate(VARIABLES['R1']/VARIABLES['LC'],10000)
    ## N2: ???
    ## Yeah, truncate(n,1)...
    VARIABLES['N2']=truncate(VARIABLES['N1'],1)
    ## LL: ???
    VARIABLES['LL']=truncate(VARIABLES['R1']-VARIABLES['N2']*VARIABLES['LC'],10000) ## 8610
    if VARIABLES['LL']<=2:
        ## TL: ???
        VARIABLES['FT']=truncate((2*VARIABLES['TL']+VARIABLES['LL'])/2,10000)/10000
        VARIABLES['NT']=VARIABLES['N2']-2 ## 8620
    return ## 8630
    
def L8640_output_curtain_info():
    """ Prints Curtain info to console """
    ## variables are explained in print line
    format_float_as_measurement("GR")
    print('BETWEEN BRACKETS:VARIABLES["GR"] \t BRACKET PLATE: str(VARIABLES["BP"])" x VARIABLES["TB"]"') ## 8640
    print("GRILLE PATTERN: VARIABLES['GP'] \t N0. OF RODS:VARIABLES['NR']")
    format_float_as_measurement("RL")
    print("ROD LENGTH: VARIABLES['RL'] \t ROD WEIGHT: RW ") ## 8650
    print("FIRST TUBE: VARIABLES['FT'] \t STD TUBES: NT \t\t TOTAL LINKS: VARIABLES['TNL']") ## 8660
    print("SLAT TYPE: VARIABLES['ST']  GAGE: VARIABLES['SG'] \t SLAT WEIGHT PER FOOT: truncate(SW*12,1000)")
    return 8710 ## 8670

print("SLAT GAGE: "VARIABLES['SG'] TAB(40)"SLAT WEIGHT PER FOOT:" INT((SW*12)*1000)/1000:GOTO 8710 (8680)
DD=GR:GOSUB 11260:VARIABLES['GR']=VARIABLES['ED']:print("BETWEEN BRACKETS:"VARIABLES['GR'] TAB(40)"BRACKET PLATE:"VARIABLES['STR'](BP)VARIABLES['I']" x "VARIABLES['TB'] VARIABLES['I'] (8690)
print("SLAT N0:"TS"  GAGE: "VARIABLES['SG'] TAB(40)"SLAT WEIGHT PER FOOT:"INT((SW*12)*1000)/1000 (8700)

def L8710_():
    ## SBS: Size Bottom Slats?
    if VARIABLES['SBS']!=0:
        print("SLATS TO CENTER LINE: truncate((VARIABLES['NS'],1000) \t BOTTOM SLATS: VARIABLES['NBS']  (VARIABLES['SBS'] INCHES)")
        return 8740 ## 8710

    ## OGS: Open Grill Section
    if VARIABLES['OGS']==0:
        return 8730
    else:
        print("VISION SECTION (GRILLE) \t N0. OF BOTTOM SLATS:VARIABLES['NBS']") ## 8720

    ## PSH: Preforated Slat Height, PSCL: Preforated Slat Center Line
    if VARIABLES['PSH']==0 and VARIABLES['PSCL']==0:
        return 8740
    else:
        ## A[79]: PREFORATED SLATS
        print('A[79]: VARIABLES["NPS"] @VARIABLES["FPFE"]" \t BEGINNING AT SLAT #VARIABLES["FPSFB"] FROM BOTTOM') ## 8730

    format_float_as_measurement("SL")
    print("TOTAL N0. OF SLATS: VARIABLES['TNS'] \t SLAT LENGTH: VARIABLES['SL']")
    ## SBS: Size of Bottom Slats
    if VARIABLES['SBS']!=0:
        return 8780 ## 8740

    print("SLATS TO CENTER LINE: VARIABLES['NS'] \t WINDLOCKS EVERY VARIABLES['WL'] SLATS") ## 8750
    ##PD: ???
    if VARIABLES['PD']!="":
        format_float_as_measurement("BSL")
        ## A[14]: PASS DOOR
        print("A[14] BOTTOM SLATS:VARIABLES['NBS'] \t BOTTOM SLAT LENGTH:VARIABLES['BSL']") ## 8760
    if VARIABLES['STS']!="":
        print("GUIDE DETAIL: VARIABLES['GD']-VARIABLES['PO']-VARIABLES['MA'] \t VARIABLES['STS']")
        return 8790 ## 8770
    print('GUIDE DETAIL: VARIABLES["GD"]-VARIABLES["PO"]-VARIABLES["MA"] \t WALL ANGLE THICKNESS: VARIABLES["WAT"]"') ##8780
    if VARIABLES['SD1']!=0:
        print('BOT.BAR: VARIABLES["BB_S"] \t SLOPE:VARIABLES["SD1"]" \t BOT.BAR WEIGHT: truncate(VARIABLES["BB"],10)')
        return 8810 ## 8790
    print("BOT.BAR: VARIABLES['BB_S'] \t BOT.BAR WEIGHT: truncate(VARIABLES['BB'],10)  <VARIABLES['AW']>") ## 8800
    print('HEIGHT TO CENTER LINE: VARIABLES["HC"]" \t UPSET: VARIABLES["US"]') ## 8810
    print('HANGING WEIGHT DOWN:VARIABLES["HW"] \t HANGING WEIGHT UP:VARIABLES["WU"] INITIAL LEVER ARM:VARIABLES["IL"]" \t TURNS TO RAISE: VARIABLES["TR"]') ## 8820
    print('FINAL LEVER ARM:truncate(VARIABLES["FL"],1000)" \t PRE-TURNS:truncate(VARIABLES["PT"],100)') ## 8830
    print('TORQUE REQUIRED DOWN: VARIABLES["TD"]"/# \t TORQUE REQUIRED UP: VARIABLES["TU"] "/#') ## 8840
    print('INCH/POUNDS PER TURN:VARIABLES["IP"]"/# \t TOTAL TURNS:VARIABLES["TT"]') ## 8850
    print("MAXIMUM DEFLECTION WEIGHT:math.ceil(VARIABLES['M']) \t CURTAIN & PIPE WEIGHT:math.ceil(VARIABLES['PW']+VARIABLES['HW'])")
    print()
    print() ## 8860
    L190_blackongreentext()
    VARIABLES['RC']= input(" ********** PRESS <ENTER> FOR SPRING SELECTION ********** ")
    L150_yellowonblacktext() ## 8870
    ## CY: Cycles ???
    if VARIABLES['P']>=5 or VARIABLES['CY']=="MAX":
        "BEEP"
        print()
        L180_yellowonred()
        print(" ********** SELECT SPRINGS MANUALLY FROM CHARTS ********** ")
        L150_yellowonblacktext()
        return L10660_ask_printout() ## 8880
    ## TP: ???
    if VARIABLES['CY']==0:
        VARIABLES['CY']=12500
        VARIABLES['TP']=1.055
        return L8930_fork_P_BT_iterate_O() ## 8890
    if VARIABLES['CY']==25000:
        VARIABLES['TP']=.92
        return L8930_fork_P_BT_iterate_O() ## 8900
    if VARIABLES['CY']==50000:
        VARIABLES['TP']=.79
        return L8930_fork_P_BT_iterate_O() ## 8910
    return L8920_check_cycles_p2() ## Implicit

def L8920_check_cycles_p2():
    """ Continue to check Cycles. This intersection is due to L10090 """
    ## CY: Cycles, TP: ???
    if VARIABLES['CY']==100000:
        VARIABLES['TP']=.68
        return L8930_fork_P_BT_iterate_O() ## 8920
    return L8930_fork_P_BT_iterate_O() ## Implicit

#######################
"""
OX: O indeX?- Used in L10120 to iterate the O variable
WX: W indeX?- Used in L10120 to iterate the W variable
O is set first, and then W is iterated after O
W Indidates Wire Type (WD, LR, LW, AT)
O Indicates Wire O.D.
"""
#######################

def L8930_fork_P_BT_iterate_O():
    ## Pipe <= 4 Inch
    if VARIABLES['P']<=2:
        ## BT: Single Spring
        if VARIABLES['BT']==0:
            VARIABLES['OX']=1
            for VARIABLES['O'] in range(1,3):
                set_od() ## 8930
        ## B3: Spring 1 (Outer) or BT 11 (Tandem) or 12/13 (Final Iteration)
        if VARIABLES['B3']>=.01 or VARIABLES['BT']>=11:
            for VARIABLES['O'] in range(2,2):
                VARIABLES['OX']=2
                return set_od() ## 8970 ## 8940
        ## B3: Spring 2 (Inner)
        if VARIABLES['B3']<=.01:
            for VARIABLES['O'] in range(1,1):
                VARIABLES['OX']=3
                return set_od() ## 8950

    ## Pipe <= 6 Inches
    if VARIABLES['P']<=4:
        ## BT: Single Spring
        if VARIABLES['BT']==0:
            for VARIABLES['O'] in range(2,4):
                VARIABLES['OX']=4
                return set_od() ## 8990
        ## BT: Spring 1 (Outer)
        if VARIABLES['B3']>=.01:
            for VARIABLES['O'] in range(3,3):
                VARIABLES['OX']=5
                return set_od() ## 9000
        ## BT: Spring 2 (Inner)
        if VARIABLES['B3']<=.01:
            for VARIABLES['O'] in range(2,2):
                VARIABLES['OX']=6
                return set_od() ## 9040   

    ## Pipe == 8 Inch
    if VARIABLES['P']==5:
        ## BT: Single Spring
        if VARIABLES['BT']==0:
            VARIABLES['OX']=7
            for VARIABLES['O'] in range(2,5):
                set_od() ## 9050
        ## First Iterations Spring 1 (Outer)
        if VARIABLES['BT']==1:
            VARIABLES['OX']=8
            ## The following line was a For loop between 4 and... 4..., so... yeah...
            VARIABLES['O'] = 4
            set_od() ## 9060
        ## BT: First Iteration Spring 2 (Inner)
        if VARIABLES['BT']==2:
            VARIABLES['OX']=9
            ## And this one was 3 to 3...
            VARIABLES['O']=3
            return set_od() ## 9070

    ## Pipe == 10 Inch
    if VARIABLES['P']==6:
        ## BT: Single Spring or Spring 2 (Outer)
        if VARIABLES['BT']==0 or VARIABLES['BT']==2:
            VARIABLES['OX']=11
            for VARIABLES['O'] in range(3,6):
                return set_od() ## 9090
        ## BT: Spring 1 (Inner)
        if VARIABLES['BT']==1:
            VARIABLES['OX']==12
            for VARIABLES['O'] in range(5,2,-1):
                return set_od() ## 9100

    ## Pipe >= 12 Inch
    if VARIABLES['P']>=7:
        ## BT: Single Spring or Spring 2 (Outer)
        if VARIABLES['BT']==0 or VARIABLES['BT']==2:
            VARIABLES['OX']=13
            for VARIABLES['O'] in range(4,7):
                set_od() ## 9110
        ## Pipe >= 12 Inch
        if VARIABLES['BT']==1:
            VARIABLES['OX']=14
            for VARIABLES['O'] in range(6,3,-1):
                set_od() ## 9120

def set_od():
    """ Sets the OD and validates against BT """
    ## Set OD based on Spring index
    VARIABLES['OD']=SPRINGOD[VARIABLES['O']]
    ## O = 2.75 OD Spring
    if VARIABLES['O']==1:
        ## BT: Single Spring
        if VARIABLES['BT']==0:
            if VARIABLES['BT']>=1:
                VARIABLES['WX']=2
                for VARIABLES['W'] in range(1,4):
                    return L9600_calculate_springs() ## 9180
            VARIABLES['WX']=3
            for VARIABLES['W'] in range(1,3):
                return L9600_calculate_springs() ## 9190 ## Implicit
        ## B3: float portion BT/2 == .5 => BT is Outer Spring
        if VARIABLES['B3']>=.01:
            VARIABLES['WX']=4
            for VARIABLES['W'] in range(3,0,-1):
                return L9600_calculate_springs() ## 9200
        ## BT >= 11 == BT is Tandem or Final I/O Pair
        if VARIABLES['BT']>=11:
            VARIABLES['WX']=3
            for VARIABLES['W'] in range(1,3):
                return L9600_calculate_springs() ## 9190 ## 9150
        ## B3: float portion BT/2 == 0 => BT is Inner Spring
        if VARIABLES['B3']<=.01:
            if VARIABLES['BT']>=1:
                VARIABLES['WX']=2
                for VARIABLES['W'] in range(1,4):
                    return L9600_calculate_springs() ## 9180
            VARIABLES['WX']=3
            for VARIABLES['W'] in range(1,3):
                return L9600_calculate_springs() ## 9190
    ## O = 3.75
    if VARIABLES['O']==2:
        ## BT: Single Spring or Tandem/Final Inner/Outer Iteration, Pipe >= 6 Inches
        if VARIABLES['BT']==0 or VARIABLES['BT']>=11 or VARIABLES['P']>=3:
            VARIABLES['WX']=5
            for VARIABLES['W'] in range(3,8):
                L9600_calculate_springs() ## 9210
        ## BT: First Inner/Outer Iteration
        if VARIABLES['BT'] in (1,2):
            VARIABLES['WX']=6
            for VARIABLES['W'] in range(7,2,-1):
                L9600_calculate_springs() ## 9350
        ## BT: Second Inner/Outer Iteration
        if VARIABLES['BT'] in (3,4):
            VARIABLES['WX']=7
            for VARIABLES['W'] in range(6,2,-1):
                L9600_calculate_springs() ## 9360
        ## BT: Third Inner/Outer Iteration
        if VARIABLES['BT'] in (5,6):
            VARIABLES['WX']=8
            for VARIABLES['W'] in range(5,2,-1):
                L9600_calculate_springs() ## 9370
        ## BT: Fourth Inner/Outer Iteration
        if VARIABLES['BT'] in (7,8):
            VARIABLES['WX']=9
            for VARIABLES['W'] in range(4,2,-1):
                L9600_calculate_springs() ## 9380
        ## BT: Fifth Inner/Outer Iteration
        if VARIABLES['BT'] in (9,10):
            VARIABLES['WX']=10
            for VARIABLES['W'] in range(3,3):
                return L9600_calculate_springs() ## 9390() ## 9300
        ## Pipe <= 4 Inches
        if VARIABLES['BT']==11 and VARIABLES['P']<=2:
            return set_od() ## 9320
        if VARIABLES['BT']==12:
            return L10450_iterate_BT() ## 9330
        ## Note: There is no method for BT == 11, P>=3
    ## O = 5.625
    if VARIABLES['O']==3:
        ## BT: Single Spring, P: 8-Inch
        if VARIABLES['BT']==0 or VARIABLES['P']==5:
            VARIABLES['WX']=11
            ## Try Wires 7,8
            for VARIABLES['W'] in range(7,9):
                L9600_calculate_springs() ## 9400
        ## BT in 1,3,5th Inner/Outer Iteration
        if VARIABLES['BT'] in (1,2,5,6,9,10):
            VARIABLES['WX']=12
            ## Try Wires 8,7
            for VARIABLES['W'] in range(8,6,-1):
                L9600_calculate_springs() ## 9520
        ## BT in 2,4th Inner/Outer Iteration
        if VARIABLES['BT'] in (3,4,7,8):
            VARIABLES['WX']=13
            ## Try Wire 7
            for VARIABLES['W'] in range(7,8):
                return L9600_calculate_springs() ## 9530
    ## O = 7.5
    if VARIABLES['O']==4:
        ## BT: Single Spring or First-Iteration Inner Spring
        if VARIABLES['BT']==0 or VARIABLES['BT']==2:
            VARIABLES['WX']=14
            for VARIABLES['W'] in range(4,10):
                L9600_calculate_springs() ## 9540
        ## BT: First-Iteration Outer Spring
        if VARIABLES['BT']==1:
            VARIABLES['WX']=15
            for VARIABLES['W'] in range(9,3,-1):
                L9600_calculate_springs() ## 9550
    ## O = 9.5
    if VARIABLES['O']==5:
        ## BT: Single Spring or First-Iteration Inner Spring
        if VARIABLES['BT']==0 or VARIABLES['BT']==2:
            VARIABLES['WX']=16
            for VARIABLES['W'] in range(9,11):
                L9600_calculate_springs() ## 9560
        ## BT: First-Iteration Outer Spring
        if VARIABLES['BT']==1:
            VARIABLES['WX']=17
            for VARIABLES['W'] in range(10,8,-1):
                L9600_calculate_springs() ## 9570
    ## O = 11.5
    if VARIABLES['O']==6:
        ## BT: Single Spring or First-Iteration Inner Spring
        if VARIABLES['BT']==0 or VARIABLES['BT']==2:
            VARIABLES['WX']=18
            for VARIABLES['W'] in range(9,11):
                L9600_calculate_springs() ## 9580
        ## BT: First-Iteration Outer Spring
        if VARIABLES['BT']==1:
            VARIABLES['WX']=19
            for VARIABLES['W'] in range(10,8-1):
                L9600_calculate_springs() ## 9590
    L9600_calculate_springs()

def L9600_calculate_springs():
    """ Begins the process of iteratively calculating springs """
    ## L10550_set_wire_variables()
    VARIABLES.update(WIRELOOKUP[VARIABLES['W']]) ## 9600
    ## D3: Wired Diameter Cubed (For MP), WD: Wire (Diameter/)Gage
    VARIABLES['D3']=VARIABLES['WD']**3
    ## SR: Spring Rating?, AT: Average Tensile, TP: Torque Percentage (cycles)
    VARIABLES['SR']=VARIABLES['AT']*VARIABLES['TP']
    ## MD: Mean Diameter, OD: Wire O.D.
    VARIABLES['MD']=VARIABLES['OD']-VARIABLES['WD']
    ## CN: Coil Net?, LR: Lift Rate?
    VARIABLES['CN']=VARIABLES['LR']/VARIABLES['MD']*3.1416 ## 9610
    ## Very Obviously, this section should be restructured :-/
    ## BT: Build Type, P: Pipe >= 6 Inches
    if VARIABLES['BT']==11 and VARIABLES['P']>=3:
        return L10670_set_middle_front_angle() ## 9670
    ## LI: Length Uncoiled?
    VARIABLES['LI'] = 0.0
    ## BT: Single Spring, IP: Inch/Pound Per Turn
    if VARIABLES['BT']==0:
        VARIABLES['LI']=VARIABLES['LR']/VARIABLES['IP']
    ## BT: Outer Springs
    if VARIABLES['BT'] in [1,3,5,7,9]:
        VARIABLES['LI']=VARIABLES['LR']/(VARIABLES['MP']/VARIABLES['TT'])
    ## BT: Inner Springs
    if VARIABLES['BT'] in [2,4,6,8,10]:
        VARIABLES['LI']=VARIABLES['LR']/(VARIABLES['IP']-VARIABLES['S1'])
        return L9720_generate_variables() ## 9660
    ## BT: Tandem Spring
    if VARIABLES['BT']==11:
        VARIABLES['LI']=VARIABLES['LR']/(VARIABLES['IP']/2)
    ## BT: Final Iteration Outer Spring
    if VARIABLES['BT']==12:
        VARIABLES['LI']=VARIABLES['LR']/(VARIABLES['IP']*.55)
    ## SV: ???, BT: Final Iteration Inner Spring
    if VARIABLES['BT']==13:
        VARIABLES['LI']=VARIABLES['LR']/(VARIABLES['IP']-VARIABLES['S1'])
    if VARIABLES['LI']:
        return L9720_generate_variables() ## 9700
    ## Adjusts variables and prints job
    return L10670_set_middle_front_angle() ## 9710

def L9720_generate_variables():
    """ Generates Spring Variables and then forks on BT for validation """
    ## NC: Number Coils LI: Length Uncoiled?, MD: Mean Diameter
    VARIABLES['NC']=VARIABLES['LI']/VARIABLES['MD']*3.1416
    ## LC: Length Coiled, WD: Wire Diameter
    VARIABLES['LC']=truncate(VARIABLES['NC']*VARIABLES['WD'],1000)
    ## MP: ???, SR: Spring rating, D3: Wire Diameter Cubed
    VARIABLES['MP']=VARIABLES['SR']*VARIABLES['D3']/10.2 ## 9720
    ## TQ: Torque holder, CN: Coil Net? Torque per coil
    VARIABLES['TQ']=truncate(VARIABLES['CN']/VARIABLES['NC'],100) ## 9730
    ## MT: Max Turns
    VARIABLES['MT']=VARIABLES['MP']/VARIABLES['TQ']
    ## WS: Weight of Spring
    VARIABLES['WS']=truncate(VARIABLES['LI']*VARIABLES['LW'],10) ## 9740
    ## OD: Outer Diameter
    print( VARIABLES['WD'],VARIABLES['OD'],VARIABLES['LC']) ## 9750
    ## BT: Build Type (Single, Compound, Tandem)
    ## Val Cur Spring will print and "exit" if valid, otherwise,
    ## rolls into Val Spring1
    if VARIABLES['BT']==0 :
        return L10050_validate_current_spring() ## 9760
    ## Val Tan Spring prints and "exits" if valid, otherwise
    ## otherwise iterates BT, which returns to pre-loop (L8930)
    if VARIABLES['BT']==11:
        return L9830_validate_tandem_spring() ## 9770
    ## Val Spring1 sets Spring 1 (Outer) if valid and then iterate BT,
    ## Otherwise either iterates WO or Checks Cycles
    if VARIABLES['BT'] in (1,3,5,7,9):
        return L10020_validate_spring1() ## 9780
    ## Val Out In Spring sets Spring 2 (Inner), prints, and "exits" if valid,
    ## otherwise iterates WO
    if VARIABLES['BT'] in (2,4,6,8,10):
        return L9920_validate_outer_inner_spring() ## 9790

    ## P: Pipe <= 4 Inches
    if VARIABLES['BT']==12 and VARIABLES['P']<=2:
        return L10070_validate_spring1() ## 9810
    ## Chk Spring Calcs validates for Outer/Inner, setting/
    ## printing/exiting if valid, otherwise iterating WO
    if VARIABLES['BT']==13 and VARIABLES['P']<=2:
        return L9900_check_spring_calculations() ## 9820

    ## This line is theoretically implicit, but I don't think that
    ## the other possibilities ever occur, however can't prove so
    return L9830_validate_tandem_spring()

def L9830_validate_tandem_spring():
    """ Validates calculations for Tandem Springs and sets them if Valid, otherwise iterates """
    ## TT: Total Turns, MP: 
    ## Removed parens
    if VARIABLES['TT']>=VARIABLES['MP']/((VARIABLES['IP']/2)*1.015)\
        or VARIABLES['MP']/(VARIABLES['IP']/2)>=VARIABLES['TT']*1.06:
        return L10120_iterate_W_O() ## 9830

    if VARIABLES['TQ']>(VARIABLES['IP']/2)*.99 and VARIABLES['TQ']<((VARIABLES['IP']/2)*1.015):
        return L9850_set_print_twin_tandom_springs()
    else:
        return L10120_iterate_W_O() ## 9840

def L9850_set_print_twin_tandom_springs():
    """ Sets variables and outputs Twin Tandom Springs """
    ## S1: Outer Spring Rate
    VARIABLES['S1']=VARIABLES['TQ']
    ## W1: Outer Spring Wire Gage
    VARIABLES['W1']=VARIABLES['WD']
    ## O1: Outer Spring OD
    VARIABLES['O1']=VARIABLES['OD']
    ## L1: Outer Spring Length
    VARIABLES['L1']=VARIABLES['LC']
    ## F1: Outer Spring Weight
    VARIABLES['F1']=VARIABLES['WS']
    ## E1: Outer Spring Stretch, TT: Total Turns
    VARIABLES['E1']=truncate(VARIABLES['WD']*VARIABLES['TT']*2,100)
    ## MT1: Outer Spring Max Turns
    VARIABLES['MT1']=VARIABLES['MT'] ## 9850
    ## S2: Inner Spring Rate
    VARIABLES['S2']=VARIABLES['S1']
    ## CT: Springs Total Inch/Pound
    VARIABLES['CT']=VARIABLES['S1']*2
    ## W2: Inner Spring Wire Gage
    VARIABLES['W2']=VARIABLES['W1']
    ## O2: Inner Spring OD
    VARIABLES['O2']=VARIABLES['O1']
    ## L2: Inner Spring Length
    VARIABLES['L2']=VARIABLES['L1']
    ## F2: Inner Spring weight
    VARIABLES['F2']=VARIABLES['F1']
    ## E2: Inner Spring Stretch
    VARIABLES['E2']=VARIABLES['E1']
    ## F3: Total Spring Weight
    VARIABLES['F3']=VARIABLES['F1']*2
    ## MT2: Inner Spring max Turns
    VARIABLES['MT2']=VARIABLES['MT1'] ## 9860
    print()
    print('TWIN TANDOM: TWO <2> str(VARIABLES["W1"])" WIRE x str(VARIABLES["O1"])" O.D. x str(VARIABLES["L1"])" LONG   STRETCH str(VARIABLES["E1"])"') ## 9870
    print( 'VARIABLES["S1"] VARIABLES["IP"] TORQUE  truncate(VARIABLES["MT1"],100) MAX.TURNS  VARIABLES["F1"] Lbs. SPRING WEIGHT') ## 9880
    print()
    print('VARIABLES["CT"] VARIABLES["IP"] TOTAL TORQUE  ("VARIABLES["IP"]"/# @VARIABLES["TT"])  VARIABLES["F3"] LBS. TOTAL WEIGHT')
    return L10660_ask_printout() ## 9890

def L9900_check_spring_calculations():
    """ Validates Spring calculations, printing if valid or iterating if invalid """
    ## TT: Total Turns, MP: ???, SV: 
    if VARIABLES['TT']>=VARIABLES['MP']/((VARIABLES['IP']-VARIABLES['S1'])*1.015):
        return L10120_iterate_W_O() ## 9900

    ## TQ: ???

    if VARIABLES['TQ']>(VARIABLES['IP']-VARIABLES['S1'])*.99\
        and VARIABLES['TQ']<(VARIABLES['IP']-VARIABLES['S1'])*1.015:
        return L9960_set_print_outer_inner_spring() ## 9910

    return L9920_validate_outer_inner_spring() ## Implicit
    
def L9920_validate_outer_inner_spring():
    """ Validates Inner and Outer Spring Calculation and sets if valid, otherwise iterates """
    ## SZ: ???
    if VARIABLES['TT']>=VARIABLES['MP']/((VARIABLES['IP']-VARIABLES['S1'])*1.015):
        return L10120_iterate_W_O() ## 9920

    ## P: Pipe (Shaft?), LC: ???, L1: Outer Spring Length
    if VARIABLES['TQ']>(VARIABLES['IP']-VARIABLES['S1'])*.99\
        and VARIABLES['TQ']<(VARIABLES['IP']-VARIABLES['S1'])*1.015\
        and VARIABLES['P']<3 and VARIABLES['LC']>=12 and VARIABLES['LC']<=VARIABLES['L1']-6:
        return L9960_set_print_outer_inner_spring() ## 9930

    if VARIABLES['TQ']>(VARIABLES['IP']-VARIABLES['S1'])*.99\
        and VARIABLES['TQ']<(VARIABLES['IP']-VARIABLES['S1'])*1.015\
        and VARIABLES['P']>2 and VARIABLES['LC']>16 and VARIABLES['LC']<VARIABLES['L1']-9.600001:
        return L9960_set_print_outer_inner_spring() ## 9940

    return L10120_iterate_W_O() ## 9950

def L9960_set_print_outer_inner_spring():
    """ sets the values for Outer and Inner Springs and Outputs the information """
    ## S2: Inner Spring Rate Inch/Pound, TQ: Torque Calculation Holder
    VARIABLES['S2']=VARIABLES['TQ']
    ## W2: Inner Spring Wire Gage, WD: Wire (Gage/)Diameter Calculation Holder
    VARIABLES['W2']=VARIABLES['WD']
    ## O2: Inner Spring O.D., OD: Spring O.D. Calculation Holder
    VARIABLES['O2']=VARIABLES['OD']
    ## L2: Inner Spring Length, LC: Spring Length Calculation Holder
    VARIABLES['L2']=VARIABLES['LC']
    ## CT: Spring Total Inch/Pound (Torque), S1: Outer Spring Rate Inch/Pound
    VARIABLES['CT']=VARIABLES['S1']+VARIABLES['S2']
    ## F2: Inner Spring Weight, WS: Weight Spring Calculation Holder
    VARIABLES['F2']=VARIABLES['WS']
    ## E2: Inner Spring Stretch, TT: Total Turns
    VARIABLES['E2']=truncate(VARIABLES['WD']*VARIABLES['TT']*2,100)
    ## F3: Total Spring Weight, F1: Outer Spring Weight
    VARIABLES['F3']=VARIABLES['F1']+VARIABLES['F2']
    ## MT2: Inner Spring Max Turns, MT: Max Turns Calculation Holder
    VARIABLES['MT2']=truncate(VARIABLES['MT'],100) ## 9960
    print()
    return L9970_print_outer_inner_spring() ## Implicit
    
def L9970_print_outer_inner_spring():
    print('OUTER SPRING:str(W1)" WIRE x str(O1)" O.D. x str(L1)" LONG   STRETCH str(E1)"') ## 9970
    print('S1 "/# TORQUE  truncate(MT1,100) MAX.TURNS  F1 Lbs. SPRING WEIGHT') ## 9980
    print()
    print('INNER SPRING: str(W2)" WIRE x str(O2)" O.D. x str(L2)" LONG   STRETCH str(E2)"') ## 9990
    print('S2 "/# TORQUE  MT2 MAX.TURNS  F2 Lbs. SPRING WEIGHT') ## 10000
    print()
    print('CT "/# TOTAL TORQUE  (IP "/# @TT)  F3 Lbs. TOTAL WEIGHT')
    return L10660_ask_printout() ## 10010

def L10020_validate_spring1():
    """ Checks the validity of the Outer Spring and sets it if valid, otherwise iterates W/O """
    ## TQ: Rate Inch/Pound (Torque) Calculation Holder, SX: ???
    if VARIABLES['TQ']>=(VARIABLES['MP']/VARIABLES['TT'])*.99\
       and VARIABLES['TQ']<=(VARIABLES['MP']/VARIABLES['TT'])*1.015:
        return L10040_set_spring1() ## 10020
    return L10120_iterate_W_O() ## 10030

def L10040_set_spring1():
    """ Sets the values for the Outer Spring and then iterates BT
       
    NOTE: This function is identical to 10100
    """
    ## S1: Outer Spring Rate Inch/Pound, TQ: Torque Calculation Holder
    VARIABLES['S1']=VARIABLES['TQ']
    ## W1: Outer Spring Wire Gage, Wire (Diameter/)Gage Calculation Holder
    VARIABLES['W1']=VARIABLES['WD']
    ## O1: Outer Spring Wire OD, OD: Spring O.D. Calculation Holder
    VARIABLES['O1']=VARIABLES['OD']
    ## L1: Outer Spring Length, LC: Spring Length Calculation Holder
    VARIABLES['L1']=VARIABLES['LC']
    ## F1: Outer Spring Weight, WS: Weight Spring Calculation Holder
    VARIABLES['F1']=VARIABLES['WS']
    ## E1: Outer Spring Stretch, TT: Total Turns
    VARIABLES['E1']=truncate(VARIABLES['WD']*VARIABLES['TT']*2,100)
    ## MT1: Outer Spring Max Turns, MT: Max Turns Calculation Holder
    VARIABLES['MT1']=VARIABLES['MT']
    return L10450_iterate_BT() ## 10040

def L10050_validate_current_spring():
    """ Validates the current spring and outputs it if it is completely valid, otherwise validates
    it as the Outer Spring, or iterates if it is completely invalid """
    ## TT: Total Turns, MP: ???, IP: Inch/Pound per Turn
    if VARIABLES['TT']>=VARIABLES['MP']/VARIABLES['IP']*1.015:
        return L10120_iterate_W_O() ## 10050

    ## TQ: Rate Inch/Pound Calculation Holder, MT: Max Turns Calculation Holder
    if VARIABLES['TQ']<=VARIABLES['IP']*1.01 and VARIABLES['TQ']>=VARIABLES['IP']*.99\
        and VARIABLES['MT']>=VARIABLES['TT']*.985:
        ## E1: Outer Spring Stretch, WD: Wire (Diameter/)Gage
        VARIABLES['E1']=VARIABLES['TT']*VARIABLES['WD']*2
        ## F1: Outer Spring Weight, WS: Weight Spring Calculation Holder
        VARIABLES['F1']=VARIABLES['WS']
        ## L1: Outer Spring Length, LC: Spring Length Calculation Holder
        VARIABLES['L1']=VARIABLES['LC']
        ## L2: Inner Spring length
        VARIABLES['L2']=0
        return L10650_print_spring_info() ## 10060

    return L10070_validate_spring1() ## Implicit

def L10070_validate_spring1():
    """" Checks the calculation variables and sets the Outer Spring if valid """
    ## TT: Total Turns, MP: ???, SY: ???
    if VARIABLES['TT']>=VARIABLES['MP']/(VARIABLES['IP']*.55)*1.015\
        or VARIABLES['MP']/(VARIABLES['IP']*.55)>=VARIABLES['TT']*1.06:
        return L10120_iterate_W_O() ## 10070

    ## TQ: Rate Inch/Pound (Torque) Calculation Holder
    if VARIABLES['TQ']<=(VARIABLES['IP']*.55)*1.01 and VARIABLES['TQ']>=(VARIABLES['IP']*.55)*.99:
        return L10100_set_spring1() ## 10080

    if VARIABLES['TQ']<=(VARIABLES['IP']*.55):
        return L8920_check_cycles_p2() ## 10090
    return L10100_set_spring1() ## Implicit

def L10100_set_spring1():
    """ Sets the variables for the Outer Spring
        
    NOTE: This function is identical to 10040
    """
    ## S1: Outer Spring Rate Inch/Pound, TQ: Torque Calculation Holder
    VARIABLES['S1']=VARIABLES['TQ']
    ## W1: Outer Spring Wire Gage, Wire (Diameter/)Gage Calculation Holder
    VARIABLES['W1']=VARIABLES['WD']
    ## O1: Outer Spring Wire OD, OD: Spring O.D. Calculation Holder
    VARIABLES['O1']=VARIABLES['OD']
    ## L1: Outer Spring Length, LC: Spring Length Calculation Holder
    VARIABLES['L1']=VARIABLES['LC']
    ## F1: Outer Spring Weight, WS: Weight Spring Calculation Holder
    VARIABLES['F1']=VARIABLES['WS']
    ## E1: Outer Spring Stretch, TT: Total Turns
    VARIABLES['E1']=VARIABLES['WD']*VARIABLES['TT']*2
    ## MT1: Outer Spring Max Turns, MT: Max Turns Calculation Holder
    VARIABLES['MT1']=VARIABLES['MT']
    return L10450_iterate_BT() ## 10100

def L10110_set_spring2():
    """ Sets the variables for the Inner Spring """
    VARIABLES['S2']=VARIABLES['TQ']
    VARIABLES['W2']=VARIABLES['WD']
    VARIABLES['O2']=VARIABLES['OD']
    VARIABLES['L2']=VARIABLES['LC']
    VARIABLES['F2']=VARIABLES['WS']
    VARIABLES['E2']=VARIABLES['E1']
    return L9970_print_outer_inner_spring() ## 10110

def L10450_iterate_BT():
    """ Iterates BT and fork based on value"""
    ## BT: ???
    VARIABLES['BT']=VARIABLES['BT']+1
    print(VARIABLES['BT'])
    ## B1: Half BT
    VARIABLES['B1']=VARIABLES['BT']/2
    ## B2: Integer portion of B1
    VARIABLES['B2']=int(VARIABLES['B1'])
    ## B3: Float portion of B1
    VARIABLES['B3']=VARIABLES['B1']-VARIABLES['B2']
    ## Pipe (Shaft?)
    return L8930_fork_P_BT_iterate_O() ## 10490

def L10650_print_spring_info():
    """ Prints info for the currently calculated spring """
    L180_yellowonred()
    print(" WD WIRE x OD OD x LC LONG = TQ INCH/LBS. @ MT TURNS ")
    L150_yellowonblacktext() ## 10650
    return L10660_ask_printout() ## Implicit

def L10660_ask_printout():
    """ Asks for user input to display printout """
    print()
    L190_blackongreentext()
    VARIABLES["RC"] = input(" ********** PRESS <ENTER> FOR PRINT OUT ********** ")
    L150_yellowonblacktext() ## 10660
    L10670_set_middle_front_angle() ## Implicit
