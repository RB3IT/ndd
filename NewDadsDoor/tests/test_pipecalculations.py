""" NewDadsDoor.tests.test_pipecalculations

Tests for the NewDadsDoor.pipecalculations module

"""
## Test Target
from NewDadsDoor import pipecalculations
## Test Framework
import unittest
## Utility module
from NewDadsDoor.tests.utils import pipecalculations as utils
## This Module
from NewDadsDoor import classes, methods

class MiscCase(unittest.TestCase):
    """ Test Case for various unbound methods """
    def test_get_all_compounds(self):
        """ Tests that get_all_compounds returns sockets (in general) """
        ## With no pipe provided, it should return ALL compounds
        self.assertTrue(pipecalculations.get_all_compounds())

    def test_assemblywrapper(self):
        """ Tests that the Assembly Wrapper properly handles different output formats """
        @pipecalculations.assemblywrapper
        def passthrough(output):
            """ A simple function to be wrapped by assemblywrapper """
            return output

        tests = utils.build_assemblywrapper_tests()

        for i,(output,result) in enumerate(tests,start=1):
            with self.subTest(output = output, result = result, testnumber = i):
                out = passthrough(output)
                self.assertEqual(out,result)

    def test_get_all_compound_castings(self):
        """ Tests that get_all_compounds can be safely used without throwing Casting errors. """
        ## Using a None-type pipe allows us to get all possible spring configurations
        pipe = pipecalculations.validate_assembly_pipe(None)
        ## _get_all_compound_springs is a testing/extension method that will avoid generating the Sockets immediately
        ## which allows us to see what Springs (if any) cannot be matched to a Casting configuration
        springs = pipecalculations._get_all_compound_springs()
        for pair in springs:
            with self.subTest(pair = pair):
                ## Cycles is probably unnecessary as we aren't validating here.
                springs = [classes.Spring(**spring, cycles = pipe.cycles) for spring in pair]
                ## See if this raises an exception
                methods.getcasting(*springs)


if __name__ == "__main__":
    unittest.main()