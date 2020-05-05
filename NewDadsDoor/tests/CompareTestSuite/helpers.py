## Builtin
import csv
import os.path

## Custom Module
from alcustoms import measurement

ROOTDIR = os.path.dirname(os.path.realpath(__file__))

VALIDATIONREFERENCE = ROOTDIR + "/testdata/VALIDATION-REFERENCE.csv"
VALIDATIONDATA = ROOTDIR + "/testdata/OVAL.csv"
del ROOTDIR

def getarraytovaluelookup():
    with open(VALIDATIONREFERENCE,'r') as f:
        reader = csv.DictReader(f)
        return {int(line['Array Index']):line['Data'] for line in reader}

def getvaluetoarraylookup():
    with open(VALIDATIONREFERENCE,'r') as f:
        reader = csv.DictReader(f)
        return {line['Data']:line['Array Index'] for line in reader}

def getvalidationfields():
    """ Returns a list of references to pair to VALIDATIONDATA"""
    with open(VALIDATIONREFERENCE,'r') as f:
        reader = csv.DictReader(f)
        lines = sorted(reader,key = lambda line: int(line['Array Index']))
        return [line['Data'] for line in lines]

def importtestdata():
    """ Imports the trials csv with fields taken from the VALIDATIONREFERENCE """
    fields = getvalidationfields()
    with open(VALIDATIONDATA,'r') as f:
        reader = csv.DictReader(f,fieldnames = fields)
        trials = list(reader)
    for trial in trials:
        for k,v in trial.items():
            ## Convert measure returns any value un-modified that is not a measurement
            try: v = measurement.measuretotuple(v).tofloat()
            except: pass
            trial[k] = v
    return trials

def testdatabyjobnumber():
    """ Imports the testdata per importtestdata and then converts the data to a jobnumber-based lookup """

    testdata = importtestdata()
    return {data['jobnumber']:data for data in testdata}