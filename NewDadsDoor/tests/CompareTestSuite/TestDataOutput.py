""" TestDataOutput.py

Script to output the test doors to a text file

"""

from NewDadsDoor.tests.CompareTestSuite import classes
from NewDadsDoor import methods
from alcustoms import text
import argparse, sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("outputfile", nargs = "?", type=argparse.FileType("w"), default = sys.stdout, help="File to output to (will print to console otherwise")
    args = parser.parse_args()
    file = args.outputfile
    doors = classes.gathertestdata()
    for door in doors:
        doorobj = door.pop("door")
        vals = [f"{k}: {v}" for k,v in door.items()]
        vals = text.format_list_to_columns(vals,columns = 2)
        output = methods.format_adc_output(methods.output_all_door_calculations(doorobj))
        file.write(f"DOOR: {doorobj}\n---- TEST DATA:\n")
        file.write(vals)
        file.write("\n---- RESULT DATA:\n")
        file.write(output)
        file.write("\n=================================\n\n")