""" NewDadsDoor.tests.test_methods

    Unittests for NewDadsDoor.methods

"""

## Test Target
from NewDadsDoor import methods
## Test Framework
import unittest
## Test Utilities
from NewDadsDoor.tests.utils import methods as utils
## This Module
from NewDadsDoor import classes, constants


class GeneralCase(unittest.TestCase):
    """ Generic tests of various methods from NDD.methods """

    def test_convert_to_casting(self):
        """ Generic tests for convert_to_casting """
        ## TODO

    def test_build_sockets(self):
        """ Generic tests for build_sockets """
        for [test,expected] in utils.BUILD_SOCKET_VALUES:
            with self.subTest(test = test, expected = expected):
                result = methods.build_sockets(*test)
                self.assertCountEqual(result, expected)

    def test_build_sockets_bad(self):
        """ Bad arguments for build_sockets """
        self.assertRaises(ValueError, methods.build_sockets, [classes.Spring(wire=.1875, od=2.75, ),],["Standard 2 Spring"])

    def test_getcasting(self):
        """ Tests the getcasting method for expected values.
        
            The expected output of this method should be inspected if castings are changed or added.
        """
        for result,wires in [
            (["Standard 4 Pipe", "Standard 2 Spring"], [(.1875,2.75),]),
            ]:
            with self.subTest(result = result, wires = wires):
                result = classes.CastingSet(*result)
                springs = [classes.Spring(wire,od = od) for (wire,od) in wires]
                ## socket automatically runs getcasting when casting is False
                socket = classes.Socket(*springs, castings = False)

                self.assertEqual(socket.castings,result)