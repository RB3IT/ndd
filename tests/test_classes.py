## Test Target
from NewDadsDoor import classes
## Test Framework
import unittest

"""
    CLASSES TESTS

    As the name says, tests pertaining to the NewDadsDoor.classes module.
"""

## Basic Springs
INNER1 = classes.Spring()
OUTER1 = classes.Spring(wire = .375, od = 3.75)
OUTER2 = classes.Spring(wire = .5, od = 5.625)


INNER1.coiledlength = 40
OUTER1.coiledlength = 50

VALIDSOCKETS = [
    classes.Socket(), ## Empty Socket
    classes.Socket(INNER1), ## Single Spring (smallest)
    classes.Socket(OUTER1), ## Single Spring (largest in 4" pipe)
    classes.Socket(OUTER1,INNER1), ## 4" Duplex
    ]

class DoorCase(unittest.TestCase):
    """ Test case for the Door Class """
    def test_setsizes(self):
        """ Test that doors can be initialized and later changed to different heights/widths in different formats """
        size = "12ft-0/1in"
        door = classes.Door(size,size)
        ## Initial initialization test
        self.assertEqual(door.clearopening_height,144)
        self.assertEqual(door.clearopening_width,144)
        ## Iterative Tests
        for (height,width,nheight,nwidth) in [(10,10,120,120),
                               ("14","14",168,168),
                               ("12ft",12,144,144),
                               ("10ft1in","""9'11" """,121,119),]:
            with self.subTest(door = door, height = height, width = width, nheight = nheight, nwidth = nwidth):
                newdoor = classes.Door(height,width)
                self.assertEqual(newdoor.clearopening_height,nheight)
                self.assertEqual(newdoor.clearopening_width, nwidth)
                door.clearopening_height = height
                door.clearopening_width = width
                self.assertEqual(door.clearopening_height,nheight)
                self.assertEqual(door.clearopening_width, nwidth)

class MiscCase(unittest.TestCase):
    """ Test Case for various unbound methods """
    def test_get_all_compounds(self):
        """ Tests that get_all_compounds returns sockets (in general) """
        ## With no pipe provided, it should return ALL compounds
        self.assertTrue(classes.get_all_compounds())

    def test_assemblywrapper(self):
        """ Tests that the Assembly Wrapper properly handles different output formats """
        @classes.assemblywrapper
        def passthrough(output):
            """ A simple function to be wrapped by assemblywrapper """
            return output

        tests = build_assemblywrapper_tests()

        for i,(output,result) in enumerate(tests,start=1):
            with self.subTest(output = output, result = result, testnumber = i):
                out = passthrough(output)
                self.assertEqual(out,result)

class SocketCase(unittest.TestCase):
    """ Test case for the Socket Class """
    def test_validate_good(self):
        """ Tests a variety of good configurations for Sockets with Springs """
        for socket in VALIDSOCKETS:
            with self.subTest(socket = socket):
                ## TODO: is_valid was replaced with validate(turns) to imporve consistency
                return
                ##self.assertTrue(socket.is_valid)

class AssemblyCase(unittest.TestCase):
    def test_addsocket(self):
        """ Tests that Assembly.addsocket works as expected """
        assem = classes.Assembly()
        socket = classes.Socket(classes.Spring())
        assem.addsocket(socket)

        self.assertEqual(len(assem.sockets),1)
        self.assertEqual(assem.sockets[0],socket)

class CompareCase(unittest.TestCase):
    """ Location for all comparison function tests (==, <, etc.) """
    def test_spring(self):
        """ Tests that springs compare equally """
        s1,s2 = classes.Spring(),classes.Spring()
        ## Something is seriously wrong if this first one doesn't pass...
        self.assertEqual(s1,s1)
        self.assertEqual(s1,s2)

    def test_socket(self):
        """" Tests that sockets compare equally """
        s1 = classes.Socket(classes.Spring())
        s2 = classes.Socket(classes.Spring())
        ## Something is seriously wrong if this first one doesn't pass...
        self.assertEqual(s1,s1)
        self.assertEqual(s1,s2)

    def test_assemblysockets(self):
        """" Tests that assemblysockets compare equally """
        s1 = classes.AssemblySockets()
        s1.addsocket(classes.Socket(classes.Spring()))
        s2 = classes.AssemblySockets()
        s2.addsocket(classes.Socket(classes.Spring()))
        ## Something is seriously wrong if this first one doesn't pass...
        self.assertEqual(s1,s1)
        self.assertEqual(s1,s2)

    def test_assembly(self):
        """" Tests that assemblysockets compare equally """
        s1 = classes.Assembly()
        s1.addsocket(classes.Socket(classes.Spring()))
        s2 = classes.Assembly()
        s2.addsocket(classes.Socket(classes.Spring()))
        ## Something is seriously wrong if this first one doesn't pass...
        self.assertEqual(s1,s1)
        self.assertEqual(s1,s2)

    def test_castings_equal(self):
        """ Tests that two identical CastingSets evaluate as equal """
        for castings in [("Standard 4 Pipe", "Standard 2 Spring"), ## Single small spring
                         ("Standard 4 Pipe", "Standard 2 Spring", "Standard 4 Spring"), ## Compound Spring
                         ("Standard 6 Pipe", "Standard 6 Pipe"), ## Single Large Spring (Probably Unnecessary)
                         ("Standard 6 Pipe", "Standard 4 Spring", "Standard 6 Pipe"), ## Compound Large Springs (Also, probably unnecessary)
                         ]:
            with self.subTest(castings = castings):
                c1 = classes.CastingSet(*castings)
                c2 = classes.CastingSet(*castings)
                self.assertEqual(c1,c2)

    def test_castings_not_equal(self):
        """ Tests that two different CastingSets evaluate as inequal """
        for c1,c2 in [(("Standard 4 Pipe","Standard 2 Spring"), ("Standard 6 Pipe", "Standard 6 Spring")), ## Completely Different
                      (("Standard 4 Pipe", "Standard 2 Spring"), ("Standard 2 Spring", "Standard 4 Pipe")), ## Reverse Order
                      (("Standard 4 Pipe", "Standard 2 Spring", "Standard 4 Spring"), ("Standard 4 Pipe", "Standard 4 Spring")), ## Missing Casting
                         ]:
            with self.subTest(c1 = c1, c2 = c2):
                c1 = classes.CastingSet(*c1)
                c2 = classes.CastingSet(*c2)
                self.assertNotEqual(c1,c2)

class CastingCase(unittest.TestCase):
    """ TestCase for CastingSet Object """
    def test_name_to_casting(self):
        """ Tests that the CastingSet object automatically converts names to casting dicts """
        ## Using CASTINGLOOKUP to garauntee the values exist
        for name in list(classes.CASTINGLOOKUP):
            with self.subTest(name = name):
                try:
                    casting = classes.CastingSet(name)
                except Exception as e:
                    self.fail(e,e.message)
                self.assertEqual(classes.CASTINGLOOKUP[name],casting.castings[0])

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

    def test_get_all_compound_castings(self):
        """ Tests that get_all_compounds can be safely used without throwing Casting errors. """
        ## Using a None-type pipe allows us to get all possible spring configurations
        pipe = classes.validate_assembly_pipe(None)
        ## _get_all_compound_springs is a testing/extension method that will avoid generating the Sockets immediately
        ## which allows us to see what Springs (if any) cannot be matched to a Casting configuration
        springs = classes._get_all_compound_springs()
        for pair in springs:
            with self.subTest(pair = pair):
                ## Cycles is probably unnecessary as we aren't validating here.
                springs = [classes.Spring(**spring, cycles = pipe.cycles) for spring in pair]
                ## See if this raises an exception
                classes.getcasting(*springs)

#class GenerationCase(unittest.TestCase):
#    """ Test Case for Generation Methods.

#        These tests are heavily generalized and more testing is likely required to validate.
#    """

#    def test_generate_single_spring(self):
#        """ Tests that Sockets generated by generate_single_spring all have valid springs """
#        torque,turns = 437,4.027
#        assemblies = classes.generate_single_spring(torque,turns)
#        self.assertTrue(assemblies)
#        for assembly in assemblies:
#            with self.subTest(assembly = assembly):
#                socket = assembly.sockets[0]
#                spring = socket.springs[0]
#                self.assertTrue(spring.validatetorque(torque))
#                self.assertTrue(spring.validatemaxturns(turns))

#    def test_generate_compound_ALL(self):
#        """ Tests that all compound generation methods return valid sockets/springs """
#        import traceback
#        for height,width in [
#            (8,8),
#            (10,10),
#            (12,12),
#            (14,14),
#            (16,16)]:
#            door = classes.Door(height,width)
#            pipe = classes.validate_assembly_pipe(None)
#            door.pipe = pipe
#            door.setcurtain()
#            classes.create_curtain(door)
#            with self.subTest(door = door, pipe = pipe):
#                torque, turns = door.torqueperturn, door.totalturns
#                for meth in [classes.generate_compound_rti,]:
#                    with self.subTest(meth = meth):
#                        sockets = meth(torque,turns,pipe = pipe)
#                        self.assertTrue(sockets)
#                        for socket in sockets:
#                            with self.subTest(socket = socket):
#                                o,i = socket.springs
#                                self.assertAlmostEqual(socket.lift,torque, delta = torque*.05)

#    def test_generate_compound_rti(self):
#        """ Tests specific to RTI """
#        import traceback
#        for height,width in [
#            (8,8),
#            (10,10),
#            (12,12),
#            (14,14),
#            (16,16)]:
#            door = classes.Door(height,width)
#            pipe = classes.validate_assembly_pipe(None)
#            door.pipe = pipe
#            door.setcurtain()
#            classes.create_curtain(door)
#            with self.subTest(door = door, pipe = pipe):
#                torque, turns = door.torqueperturn, door.totalturns
#                assemblies = classes.generate_compound_rti(torque,turns,pipe = pipe)
#                self.assertTrue(assemblies)
#                for assembly in assemblies:
#                    with self.subTest(assembly = assembly):
#                        socket = assembly.sockets[0]
#                        o,i = socket.springs
#                        self.assertEqual(int(o.coiledlength), int(i.coiledlength))
#                        rti = classes.get_rti(socket.springs[0],socket.springs[1])
#                        tru = torque / (rti + 1)
#                        tri = tru * rti
#                        self.assertAlmostEqual(o.lift,tru,delta = tru * .05)
#                        self.assertAlmostEqual(i.lift,tri,delta = tri * .05)
#                        ## The combined lift is tested in the _ALL method

def build_assemblywrapper_tests():
    """ Separate Area for putting together the tests for test_assemblywrapper """
    ## Test that a Single Spring output results in 1 Assembly with 1 Single-Spring Assembly
    test1 = [classes.Spring(),]
    assembly1 = classes.Assembly()
    assembly1.addsocket(classes.Socket(*test1))

    ## Test that a list of springs gets turned into single-spring assemblies
    test2 = [classes.Spring(),classes.Spring()]
    assembly2 = [classes.Assembly() for spring in test2]
    for spring,assembly in zip(test2,assembly2):
        assembly.addsocket(classes.Socket(spring))

    ## Test that a Single Socket output results in 1 Assembly with 1 Socket
    test3  = classes.Socket(classes.Spring())
    assembly3 = classes.Assembly()
    assembly3.addsocket(test3)

    ## Test that list of sockets gets turned into single-socket Assemblies
    test4 = [classes.Socket(classes.Spring()), classes.Socket(classes.Spring())]
    assembly4 = [classes.Assembly() for socket in test4]
    for socket,assembly in zip(test4,assembly4):
        assembly.addsocket(socket)

    ## Test that a mix of Sockets and Springs gets sorted into their own assemblies (adding sockets for individual springs)
    test5 = [classes.Spring(), classes.Socket(classes.Spring())]
    assembly5 = [classes.Assembly(), classes.Assembly()]
    assembly5[0].addsocket(classes.Socket(test5[0]))
    assembly5[1].addsocket(test5[1])

    ## Test that a single assembly results in the assembly being outputted without change
    test6 = [classes.Assembly(),]
    test6[0].addsocket(classes.Socket(classes.Spring()))
    assembly6 = test6[0]

    return [
        (
            test1,
            [assembly1,]
        ),
        (
            test2,
            assembly2
        ),
        (
            test3,
            [assembly3,]
        ),
        (
            test4,
            assembly4
        ),
        (
            test5,
            assembly5
        ),
        (
            test6,
            [assembly6,]
        ),

                            ]


if __name__ == "__main__":
    unittest.main()