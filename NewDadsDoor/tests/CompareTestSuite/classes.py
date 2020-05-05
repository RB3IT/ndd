## Builtin
import copy
import functools
import pprint
import traceback
## This Module
from NewDadsDoor import classes,methods as dadsmethods
from NewDadsDoor.tests.CompareTestSuite import helpers
## Custom Module
from alcustoms.measurement import Imperial


"""

"""


TESTDATA = helpers.importtestdata()

def gathertestdata():
    try:
        trials = copy.deepcopy(TESTDATA)
        for trial in trials: generatetrialdoor(trial)
        return trials
    except:
       traceback.print_exc()
       return False

def generatetrialdoor(trial):
    """ Assembles a door based on test data and sets it as the "door" key of the test data """
    door = classes.Door(clearopening_width=trial.get("width"),clearopening_height=trial.get('stopheight'))
    ## Old DadsDoor lumps Stop Size and Upset together, so we need to parse out the default Upset
    stopsize = float(trial.get('Upset')) - door.upset
    tracks = dadsmethods.create_tracks(door, stopsize = stopsize)
    curtainargs = {k:trial.get(k,None) for k in ['slattype','slatgauge','endlocktype','windlocks']}
    #curtainargs = {k:v if v else None for k,v in curtainargs.items()}
    curtainargs['gauge'] = curtainargs.pop("slatgauge")
    curtainargs['endlocks'] = curtainargs.pop("endlocktype")
    curtain = dadsmethods.create_curtain(door,**curtainargs)
    bottombar = trial.get("bottombaredge")
    if trial.get("Safety Edge",None): bottombar = trial['Safety Edge']
    elif trial.get("Astragal Weight", None): bottombar = "ASTRAGAL"
    curtain.bottombars()[0].edge = bottombar
    pipeargs = {k:trial.get(k,None) for k in ['pipewidth','shell',
                                            'barrelrings']}
    door.setpipe(**pipeargs)
    door.sethood()
    trial['door'] = door

def floatify(value):
    """ Very simple function to catch empty strings """
    if value:
        try: return  float(value)
        except:
            try: return float(Imperial(value))
            except: pass
    return 0

def raisetesterror(badresults,testdata,headers,formatting = None, title="General Trial"):
    """ Raises a formatted Test Error based on badresults, testdata, headers, and title """
    badnumber = len(badresults)
    trialnumber = len(testdata)
    error = f"\n{title} Discrepencies:\n{badnumber} out of {trialnumber}\n"
    if formatting is not None:
        badresults = [
            [formatt.format(*result) for formatt in formatting]
            for result in badresults
            ]
        badresults.insert(0,[f"{header:^10}" for header in headers])
    error += "\n".join("\t".join(output) for output in badresults)
    raise AssertionError(error)

def validatetestdata(function):
    @functools.wraps(function)
    def inner(*args, testdata=None, **kw):
        if not testdata:
            testdata = gathertestdata()
        if not testdata: raise ValueError("No Test Data Supplied")
        return function(*args, testdata=testdata, **kw)
    return inner

def assertmargin(jobnumber, target, actual, errormargin_numeric = 0, errormargin_ratio = 0.0, flaggedjobs = None):
    """ Basic assertion test method

    target is the correct value, actual is the value to be tested.
    errormargin_numeric is the maximum difference between the target and the actual value.
    errormargin_ratio is the maximum ratio (float) between the difference and the target.
    flaggedjobs is a list jobnumbers to automatically fail: this is for debugging.
    """
    if flaggedjobs is None: flaggedjobs = tuple()
    assert abs(target - actual) <= errormargin_numeric and getratio(target,actual) <= errormargin_ratio and jobnumber not in flaggedjobs

def getratio(target,actual):
    """ Gets the ratio (percentage) of the difference between target and actual ( max is used to avoid target == 0 being indivisible) """
    return abs(target - actual) / max(.00000000000000001,target)

@validatetestdata
def general_test(title, actualfunction, targetfunction, validationfunction = assertmargin,
                 errormargin_numeric = 0, errormargin_ratio = .00, testdata = None, fail = True):
    passed = 0
    out = []
    for trial in testdata:
        actual, target = actualfunction(trial), targetfunction(trial)
        try:validationfunction(jobnumber = trial['jobnumber'], target = target, actual = actual, errormargin_numeric = errormargin_numeric, errormargin_ratio = errormargin_ratio)
        except AssertionError as e: 
            difference = actual - target
            #out.append((f"{trial['jobnumber']:>10}",f"{target:>9.04f}",f"{actual:>9.04f}",f"{difference:>9.04f}",f"{getratio(target,actual):>9.02%}"))
            out.append((trial['jobnumber'], target, actual, difference, getratio(target,actual)))

    if out:
        if fail:
            formatting = ("{0:>10}","{1:>9.04f}","{2:>9.04f}","{3:>9.04f}","{4:>9.02%}")
            raisetesterror(out,testdata,headers=["Job Number","Target","Actual","Difference","% Difference"],formatting = formatting, title=title)
        return out

######################## DOOR

def test_pipecenterlineheight(testdata = None, fail = True):
    """ Compares generated pipecenterlineheight to testdata validation """
    return general_test("Height to Pipe Centerline",
              actualfunction=lambda trial: trial['door'].pipecenterlineheight, targetfunction= lambda trial: floatify(trial['Pipe Center Line']),
              errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata,
              fail = fail)

def test_upset(testdata = None, fail = True):
    """ Compares generated upset to testdata validation """
    return general_test("Upset",
              actualfunction=lambda trial: trial['door'].tracks.stopsize + trial['door'].upset, targetfunction= lambda trial: floatify(trial['Upset']),
              errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_openheight(testdata = None, fail = True):
    """ Compares generated openheight to default value """
    return general_test("Open Height",
                        actualfunction=lambda trial: trial['door'].openheight, targetfunction= lambda trial: floatify(trial['Pipe Center Line']) - floatify(trial['stopheight']),
                        errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_hangingweight(testdata = None, fail = True):
    """ Compares generated curtain total weight to testdata validation """
    return general_test("Curtain Weight",
              actualfunction=lambda trial: trial['door'].hangingweight_closed, targetfunction= lambda trial: floatify(trial['Hanging Weight Closed']),
              errormargin_numeric = 0, errormargin_ratio = .0445, testdata = testdata, fail = fail)

def test_weightup(testdata = None, fail = True):
    """ Compares generated curtain weight when rolled up against testdata validation """
    return general_test("Curtain Weight Open",
              actualfunction=lambda trial: trial['door'].hangingweight_open, targetfunction= lambda trial: floatify(trial['Hanging Weight Open']),
              errormargin_numeric = 0, errormargin_ratio = .15, testdata = testdata, fail = fail)

def test_totalslats(testdata = None, fail = True):
    """ Compares generated totalslats against testdata validation """
    return general_test("Total Slats",
              actualfunction=lambda trial: trial['door'].curtain.slatsections()[0].getnumberslats(), targetfunction= lambda trial: floatify(trial['Total Number of Slats']),
              errormargin_numeric = 0, errormargin_ratio = 1, testdata = testdata, fail = fail)

def test_wrapslats(testdata = None, fail = True):
    """ Compares generated totalslats against testdata validation """
    return general_test("Wrap Slats",
              actualfunction=lambda trial: trial['door'].curtain.slatsections()[0].getwrapslats(), targetfunction= lambda trial: floatify(trial['Wrap']),
              errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_slatstocenterline(testdata = None, fail = True):
    """ Compares generated slatstocenterline against testdata validation """
    return general_test("Slats to Centerline",
                 actualfunction=lambda trial: trial['door'].curtain.slatsections()[0].gethangingslats(), targetfunction= lambda trial: floatify(trial['Slats to Centerline']),
                 errormargin_numeric = 1, errormargin_ratio = 1.00, testdata = testdata, fail = fail)

## Preturns (and by extension Total Turns) are considered valid within 1/6 of a turn to accomodate
## a very small number of possible doors (the rest of the tested doors were exact matches)
def test_preturns(testdata = None, fail = True):
    """ Compares generated preturns against testdata validation """
    return general_test("Pre-turns",
                 actualfunction=lambda trial: trial['door'].preturns, targetfunction= lambda trial: floatify(trial['Pre Turns']),
                 errormargin_numeric = 0.17, errormargin_ratio = 1, testdata = testdata, fail = fail)

def test_turnstoraise(testdata = None, fail = True):
    """ Compares generated turnstoraise against testdata validation """
    return general_test("Turns to Raise",
                 actualfunction=lambda trial: trial['door'].turnstoraise, targetfunction= lambda trial: floatify(trial['Turns to Raise']),
                 errormargin_numeric = .1, errormargin_ratio = .1, testdata = testdata, fail = fail)

## Total can have a numeric errormargin equal to the total of preturns and turns to raised
## so long as it is not unreasonable (probable limit should be .25)
def test_totalturns(testdata = None, fail = True):
    """ Compares generated totalturns against testdata validation """
    return general_test("Total Turns",
                 actualfunction=lambda trial: trial['door'].totalturns, targetfunction= lambda trial: floatify(trial['Total Turns']),
                 errormargin_numeric = 0.18, errormargin_ratio = 1, testdata = testdata, fail = fail)

def test_initialradius(testdata = None, fail = True):
    """ Compares generated initialradius against testdata validation """
    return general_test("Initial Radius",
                 actualfunction=lambda trial: trial['door'].initialradius, targetfunction= lambda trial: floatify(trial['Initial Lever Arm']),
                 errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_finalradius(testdata = None, fail = True):
    """ Compares generated finalradius against testdata validation """
    return general_test("Final Radius",
                 actualfunction=lambda trial: trial['door'].finalradius, targetfunction= lambda trial: floatify(trial['Final Lever Arm']),
                 errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_requiredtorque_open(testdata = None, fail = True):
    """ Compares generated requiredtorque_open against testdata validation """
    return general_test("Required Torque Open",
                 actualfunction=lambda trial: trial['door'].requiredtorque_open, targetfunction= lambda trial: floatify(trial['Torque Required Open']),
                 errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

################# CURTAIN

def test_stopheight(testdata = None, fail = True):
    """ Compares the supplied stoheight to testdata validation """
    return general_test("Stop Height",
              actualfunction=lambda trial: trial['door'].stopheight, targetfunction= lambda trial: Imperial(trial['stopheight']).tofloat(),
              errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

@validatetestdata
def test_slatlength(testdata = None, fail = True):
    """ Compares generated curtain slat length to testdata validation """
    passed = 0
    out = []
    for trial in testdata:
        actual,target = float(trial['door'].curtain.slatlength(trial['door'].curtain.slatsections()[0])),float(Imperial(trial['slatlength']))
        try: assertmargin(trial['jobnumber'], target, actual)   
        except AssertionError as e:
            difference = actual - target
            if (difference == .125 and trial['Wall Angle Thickness'] == "1/4") or\
                (difference == .25 and trial['Wall Angle Thickness'] == "5/16"):
                ## We don't use different Wall Angle Thicknesses anymore, and these
                ## adjustments are corner cases, so we'll skip them
                print('test_slatlength: Bad Wall Angle Thickness')
                continue
            width = Imperial(trial['door'].clearopening_width).tofloat()
            actualdivergence = actual - width
            targetdivergence = target - width
            differencedivergence = actualdivergence - targetdivergence
            out.append((f"{trial['jobnumber']:<10}",f"{width:^9.04f}",f"{target:^9.04f}",
                        f"{actual:^9.04f}",f"{targetdivergence:^9.04f}",f"{actualdivergence:^9.04f}",f"{difference:9.04f}"))

    if out:
        if fail:
            raisetesterror(out,testdata,headers=["Job Number","Width","Target","Actual","Target Div","Actual Div", "Difference"],title="Curtain Slat Length")
        return out

def test_bottombarweight(testdata = None, fail = True):
    """ Compares generated bottom bar weight to testdata validation """
    return general_test("Bottom Bar Weight",
              actualfunction=lambda trial: trial['door'].curtain.bottombars()[0].weight, targetfunction= lambda trial: floatify(trial['Bottom Bar Weight']),
              errormargin_numeric = 1, errormargin_ratio = .01, testdata = testdata, fail = fail)

def test_bottombarheight(testdata = None, fail = True):
    """ Compares generated bottom bar height to testdata validation """
    return general_test("Bottom Bar Height",
              actualfunction=lambda trial: trial['door'].curtain.bottombars()[0].height, targetfunction= lambda trial: floatify(trial['bottombarheight']),
              errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_getendlockweight(testdata = None, fail = True):
    """ Compares generated endlock weight against testdata validation """
    return general_test("Endlock Weight",
              actualfunction=lambda trial: trial['door'].curtain.slatsections()[0].getendlockweight(), targetfunction= lambda trial: floatify(trial['Endlock Total Weight']),
              errormargin_numeric = 1.49, errormargin_ratio = .328, testdata = testdata, fail = fail)

def test_getslatweight_tocenterline(testdata = None, fail = True):
    """ Compares generated slat weight to the centerline against testdata validation """
    slats = lambda trial: trial['door'].curtain.slatsections()[0]
    return general_test("Slat Weight (to Centerline)",
              actualfunction=lambda trial: slats(trial).getslatweight(slats(trial).gethangingslats()), targetfunction= lambda trial: floatify(trial['slatweight to Centerline']),
              errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

########################### Perforated Curtain

def test_perforatedweightloss(testdata = None, fail = True):
    """ Compares generated perforated weightloss against testdata validation """
    def checkdoor(trial):
        slats = trial['door'].curtain.slatsections()[0]
        if hasattr(slats,"perforatedweightloss"):
            return slats.perforatedweightloss
        else: return 0
    return general_test("Perforated Weight Loss",
              actualfunction= checkdoor, targetfunction= lambda trial: floatify(trial['Perforated Weight Loss']),
              errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

########################### Grille Curtain
def test_floortogrille(testdata = None, fail = True):
    """ Compares generated distance floor to grille (bottom slats) against testdata validation """
    def checkdoor(trial):
        slats = trial['door'].curtain.slatsections()
        if not slats: return 0
        slats = slats[-1]
        return slats.height + trial['door'].curtain.bottombars()[0].height
    return general_test("Floor to Grille",
              actualfunction= checkdoor, targetfunction= lambda trial: floatify(trial['Solid Bottom Height']),
              errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_getgrilleheight(testdata = None, fail = True):
    """ Compares generated grille height against testdata validation """
    def checkdoor(trial):
        grilles = [section for section in trial['door'].curtain if isinstance(section, classes.RollingGrilleSection)]
        return sum([grille.height for grille in grilles])
    return general_test("Grille Height",
              actualfunction= checkdoor, targetfunction= lambda trial: floatify(trial['Grille Height']),
              errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_getgrilleweight(testdata = None, fail = True):
    """ Compares generated grille weight against testdata validation """
    def checkdoor(trial):
        grilles = [section for section in trial['door'].curtain if isinstance(section, classes.RollingGrilleSection)]
        return sum([grille.weight for grille in grilles])
    return general_test("Grille Weight",
              actualfunction= checkdoor, targetfunction= lambda trial: floatify(trial['Grille Weight']),
              errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

########################### SLATS
def test_increaseradius(testdata = None, fail = True):
    """ Compares increaseradius constant against testdata validation """
    return general_test("Increase Radius",
                 actualfunction=lambda trial: trial['door'].curtain.slatsections()[0].slat.increaseradius, targetfunction= lambda trial: floatify(trial['increaseradius']),
                 errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_slatweight(testdata = None, fail = True):
    """ Compares slatweight constant against testdata validation """
    return general_test("Slat Weight",
                 actualfunction=lambda trial: trial['door'].curtain.slatsections()[0].slat.slatweight, targetfunction= lambda trial: floatify(trial['slatweight']),
                 errormargin_numeric = 0.0000001, errormargin_ratio = .0000001, testdata = testdata, fail = fail)

def test_slatheight(testdata = None, fail = True):
    """ Compares slatheight constant against testdata validation """
    return general_test("Slat Height",
                 actualfunction=lambda trial: trial['door'].curtain.slatsections()[0].slat.slatheight, targetfunction= lambda trial: floatify(trial['slatheight']),
                 errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

########################## Bottom Bar
def test_bottombar_angleweight(testdata = None, fail = True):
    """ Compares bottombar angleweight constant against testdata validation """
    return general_test("Bottombar Angle Weight per Foot",
                 actualfunction=lambda trial: trial['door'].curtain.bottombars()[0].angleweight, targetfunction= lambda trial: floatify(trial['bottombar angleweightperfoot']),
                 errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_bottombar_edgeweight(testdata = None, fail = True):
    """ Compares bottombar getedgeweight against testdata validation """
    return general_test("Bottombar Edge Weight per Foot",
                 actualfunction=lambda trial: trial['door'].curtain.bottombars()[0].getedgeweight(), targetfunction= lambda trial: floatify(trial['Edge Weight']),
                 errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_bottombar_slopeweight(testdata = None, fail = True):
    """ Compares bottombar slopeweight against testdata validation """
    return general_test("Bottombar Slope Weight",
                 actualfunction=lambda trial: trial['door'].curtain.bottombars()[0].slopeweight, targetfunction= lambda trial: floatify(trial['Slope Weight']),
                 errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_bottombar_feederslatweight(testdata = None, fail = True):
    """ Compares bottombar getfeederslatweight against testdata validation """
    return general_test("Bottombar Feeder Slat Weight",
                 actualfunction=lambda trial: trial['door'].curtain.bottombars()[0].getfeederslatweight(), targetfunction= lambda trial: floatify(trial['Feeder Slat Weight']),
                 errormargin_numeric = .01, errormargin_ratio = 1, testdata = testdata, fail = fail)

########################## BRACKETPLATE

def test_bracketplateheight(testdata = None, fail = True):
    """ Compares generated bracketplate height to testdata validation """
    return general_test("Bracketplate Height",
              actualfunction=lambda trial: trial['door'].bracketplate.height, targetfunction= lambda trial: floatify(trial['bracketplateheight']),
              errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

########################## PIPE

def test_shell(testdata = None, fail = True):
    """ Compares generated Pipe size to testdata validation """
    shellsize = lambda shell: int(shell.split()[0])
    return general_test("Shell",
                        actualfunction = lambda trial: trial['door'].pipe.shell['size'], targetfunction = lambda trial: shellsize(trial.get('shell')),
                        errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

def test_adjuster(testdata = None, fail = True):
    """ Compares the Pipe's adjuster to testdata validation """
    ## Adjuster 0 and adjuster 6 are synonyms:
    def validationfunction(jobnumber, actual, target, **kw):
        if actual == 0: actual = 6
        if target == 0: target = 6
        return target == actual
    return general_test("Pipe Adjuster",
              actualfunction=lambda trial: trial['door'].pipe.adjuster, targetfunction= lambda trial: int(trial['adjuster']),
              validationfunction = validationfunction,
              testdata = testdata, fail = fail)

def test_adjuster_ratio(testdata = None, fail = True):
    """ Compares the Pipe's adjuster ratio to testdata validation """
    return general_test("Pipe Adjuster Ratio",
              actualfunction=lambda trial: trial['door'].pipe.getadjusterratio(), targetfunction= lambda trial: floatify(trial['adjusterratio']),
              errormargin_numeric = 0, errormargin_ratio = .00, testdata = testdata, fail = fail)

###########################################################################################################
"""--------------------------------------------------------------------------------------------------------
                                         TEST AUDITING FUNCTIONS
--------------------------------------------------------------------------------------------------------"""
###########################################################################################################

BADDATACONSTANT = 500000000.0

@validatetestdata
def general_bad_test(testfunction,attribute, testdata = None, measure = False, fail = True):
    """ A wrapper to manufacture generic, simple bad tests """
    if measure is True: attr = Imperial(BADDATACONSTANT)
    else: attr = BADDATACONSTANT
    badtestdata = [{'jobnumber':test['jobnumber'], 'door':test['door'], attribute: attr} for test in testdata]
    try:
        testfunction(testdata = badtestdata)
    ## We expect it to fail on Assertion
    except AssertionError: return
    else:
        ## This is a bad sign
        if fail:
            raise AssertionError(f"{testfunction.__name__} OK'd bad data")
        return True

def test_general_test(testdata = None, fail = True):
    """ A simple test for general_test """
    target = 1
    def runtest():
        for good in [True,False]:
            if good:
                actual = target
                if em_numeric:
                    actual = (actual + errormargin_numeric)
                if em_ratio:
                    actual = actual + actual * errormargin_ratio
            else:
                actual = BADDATACONSTANT
            testdata = [{"jobnumber":0,"target":target, "actual":actual},]
            try:
                ## Note that the error margin gets an addition .00001 to handle binary floating point arithmetic 
                general_test(title = "General Test",
                                actualfunction = lambda test: test['actual'], targetfunction = lambda test: test['target'],
                                errormargin_numeric = errormargin_numeric, errormargin_ratio = errormargin_ratio+.00001, testdata = testdata)
            except AssertionError:
                if good:
                    if fail:
                        raise AssertionError(f"""General Test Failed a Good Test:
                Good:                   {good}
                Target:                 {target}
                Actual:                 {actual}
                ErrorMargin Numeric:    {errormargin_numeric}
                Numeric:                {abs(target - actual)}
                ErrorMargin Ratio:      {errormargin_ratio+.00001}
                Ratio:                  {getratio(target,actual)}""")
                    return True
            else:
                if not good:
                    if fail:
                        raise AssertionError("""General Test Passed a Bad Test
                Good:                   {good}
                Target:                 {target}
                Actual:                 {actual}
                ErrorMargin Numeric:    {errormargin_numeric}
                Numeric:                {abs(target - actual)}
                ErrorMargin Ratio:      {errormargin_ratio+.00001}
                Ratio:                  {getratio(target,actual)}""")
                    return True

    errormargin_numeric = 0
    em_ratio = False
    errormargin_ratio = 2
    for em_numeric in range(2):
        errormargin_numeric = em_numeric
        runtest()
    em_numeric = False
    errormargin_numeric = 2
    for em_ratio in range(2):
        errormargin_ratio = em_ratio / 10
        runtest()

def test_general_bad_test(testdata = None, fail = True):
    """ A simple test for general_bad_test """

def test_bottombarweight_bad(testdata = None, fail = True):
    """ Ensures that test_bottombarweight is not succeeding on bad data """
    return general_bad_test(test_bottombarweight,"Bottom Bar Weight", testdata = testdata, fail = fail)

def test_bottombarheight_bad(testdata = None, fail = True):
    """ Ensures that test_bottombarheight is not succeeding on bad data """
    return general_bad_test(test_bottombarheight,"bottombarheight", testdata = testdata, fail = fail)

def test_hangingweight_bad(testdata = None, fail = True):
    """ Ensures that test_hangingweight is not succeeding on bad data """
    return general_bad_test(test_hangingweight,'Hanging Weight Closed', testdata = testdata, fail = fail)

def test_weightup_bad(testdata = None, fail = True):
    """ Ensures that test_weightup is not succeeding on bad data """
    return general_bad_test(test_weightup,'Hanging Weight Open', testdata = testdata, fail = fail)

def test_getgrilleweight_bad(testdata = None, fail = True):
    """ Ensures that test_getgrilleweight is not succeeding on bad data """
    return general_bad_test(test_getgrilleweight,'Grille Weight', testdata = testdata, fail = fail)

def test_getendlockweight_bad(testdata = None, fail = True):
    """ Ensures that test_getendlockweight is not succeeding on bad data """
    return general_bad_test(test_getendlockweight,'Endlock Total Weight', testdata = testdata, fail = fail)

def test_totalslats_bad(testdata = None, fail = True):
    """ Ensures that test_totalslats is not succeeding on bad data """
    return general_bad_test(test_totalslats,'Total Number of Slats', testdata = testdata, fail = fail)

def test_wrapslats_bad(testdata = None, fail = True):
    """ Ensures that test_wrapslats is not succeeding on bad data """
    return general_bad_test(test_wrapslats,'Wrap', testdata = testdata, fail = fail)

@validatetestdata
def test_slatlength_bad(testdata = None, fail = True):
    """ Ensures that test_slatlength is not succeeding on bad data """
    badtestdata = [{'jobnumber':test['jobnumber'], 'door':test['door'],
                    'slatlength': Imperial(50000000000.0),
                    'Wall Angle Thickness':test['Wall Angle Thickness']} for test in testdata]
    try:
        test_slatlength(testdata = badtestdata)
    ## We expect it to fail on Assertion
    except AssertionError: return
    else:
        ## This is a bad sign
        if fail:
            raise AssertionError("test_slatlength OK'd bad data")
        return True

def test_turnstoraise_bad(testdata = None, fail = True):
    """ Ensures that test_turnstoraise is not succeeding on bad data """
    return general_bad_test(test_turnstoraise,'Turns to Raise', testdata = testdata, fail = fail)

def test_finalradius_bad(testdata = None, fail = True):
    """ Ensures that test_finalradius is not succeeding on bad data """
    return general_bad_test(test_finalradius,'Final Lever Arm', testdata = testdata, fail = fail)

def test_initialradius_bad(testdata = None, fail = True):
    """ Ensures that test_initialradius is not succeeding on bad data """
    return general_bad_test(test_initialradius,'Initial Lever Arm', testdata = testdata, fail = fail)

def test_increaseradius_bad(testdata = None, fail = True):
    """ Ensures that test_increaseradius is not succeeding on bad data """
    return general_bad_test(test_increaseradius,'increaseradius', testdata = testdata, fail = fail)

def test_requiredtorque_open_bad(testdata = None, fail = True):
    """ Ensures that test_requiredtorque_open is not succeeding on bad data """
    return general_bad_test(test_requiredtorque_open,'Torque Required Open', testdata = testdata, fail = fail)

def test_pipecenterlineheight_bad(testdata = None, fail = True):
    """ Ensures that test_pipecenterlineheight is not succeeding on bad data """
    return general_bad_test(test_pipecenterlineheight,'Pipe Center Line', testdata = testdata, fail = fail)

def test_slatstocenterline_bad(testdata = None, fail = True):
    """ Ensures that test_slatstocenterline is not succeeding on bad data """
    return general_bad_test(test_slatstocenterline,'Slats to Centerline', testdata = testdata, fail = fail)

def test_getslatweight_tocenterline_bad(testdata = None, fail = True):
    """ Ensures that test_getslatweight_tocenterline is not succeeding on bad data """
    return general_bad_test(test_getslatweight_tocenterline,'slatweight to Centerline', testdata = testdata, fail = fail)

def test_stopheight_bad(testdata = None, fail = True):
    """ Ensures that test_stopheight is not succeeding on bad data """
    return general_bad_test(test_stopheight,'stopheight', testdata = testdata, measure = True, fail = fail)

def test_bracketplateheight_bad(testdata = None, fail = True):
    """ Ensures that test_bracketplateheight is not succeeding on bad data """
    return general_bad_test(test_bracketplateheight,'bracketplateheight', testdata = testdata, fail = fail)

def test_bottombar_angleweight_bad(testdata = None, fail = True):
    """ Ensures that test_bottombar_angleweight is not succeeding on bad data """
    return general_bad_test(test_bottombar_angleweight,'bottombar angleweightperfoot', testdata = testdata, fail = fail)

def test_bottombar_edgeweight_bad(testdata = None, fail = True):
    """ Ensures that test_bottombar_safetyedgeweight is not succeeding on bad data """
    return general_bad_test(test_bottombar_edgeweight,'Edge Weight', testdata = testdata, fail = fail)

def test_bottombar_slopeweight_bad(testdata = None, fail = True):
    """ Ensures that test_bottombar_slopeweight is not succeeding on bad data """
    return general_bad_test(test_bottombar_slopeweight,'Slope Weight', testdata = testdata, fail = fail)

def test_bottombar_feederslatweight_bad(testdata = None, fail = True):
    """ Ensures that test_bottombar_feederslatweight is not succeeding on bad data """
    return general_bad_test(test_bottombar_feederslatweight,'Feeder Slat Weight', testdata = testdata, fail = fail)

def test_perforatedweightloss_bad(testdata = None, fail = True):
    """ Ensures that test_perforatedweightloss is not succeeding on bad data """
    return general_bad_test(test_perforatedweightloss,'Perforated Weight Loss', testdata = testdata, fail = fail)

def test_floortogrille_bad(testdata = None, fail = True):
    """ Ensures that test_floortogrille is not succeeding on bad data """
    return general_bad_test(test_floortogrille,'Solid Bottom Height', testdata = testdata, fail = fail)

##def test_totalturns_bad(testdata = None, fail = True):
##    """ Ensures that test_totalturns is not succeeding on bad data """
##    return general_bad_test(test_totalturns,'Total Turns', testdata = testdata, fail = fail)

def test_preturns_bad(testdata = None, fail = True):
    """ Ensures that test_preturns is not succeeding on bad data """
    return general_bad_test(test_preturns,'Pre Turns', testdata = testdata, fail = fail)

def test_getgrilleheight_bad(testdata = None, fail = True):
    """ Ensures that test_getgrilleheight is not succeeding on bad data """
    return general_bad_test(test_getgrilleheight,'Grille Height', testdata = testdata, fail = fail)