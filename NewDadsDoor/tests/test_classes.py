""" NewDadsDoor.tests.test_classes.py

Tests for the NewDadsDoor.classes module

"""

## Test Target
from NewDadsDoor import classes
## Test Framework
import unittest
## This module
from NewDadsDoor import constants, pipecalculations, methods
## 3rd Party
from alcustoms import measurement

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
        """ Test that doors can be initialized and later changed to different heights/widths in different formats and that they are always Measurments """
        size = "12ft-0/1in"
        door = classes.Door(size,size)
        ## Initial initialization test
        self.assertEqual(door.clearopening_height,144)
        self.assertEqual(door.clearopening_width,144)
        ## Iterative Tests
        for (height,width,nheight,nwidth) in [(120,120,120,120),
                               ("14'","14'",168,168),
                               ("12ft","12ft0",144,144),
                               ("10ft1in","""9'11" """,121,119),]:
            with self.subTest(door = door, height = height, width = width, nheight = nheight, nwidth = nwidth):
                newdoor = classes.Door(height,width)
                self.assertEqual(newdoor.clearopening_height,nheight)
                self.assertEqual(newdoor.clearopening_width, nwidth)
                self.assertIsInstance(newdoor.clearopening_height, measurement.Imperial)
                self.assertIsInstance(newdoor.clearopening_width, measurement.Imperial)
                door.clearopening_height = height
                door.clearopening_width = width
                self.assertEqual(door.clearopening_height,nheight)
                self.assertEqual(door.clearopening_width, nwidth)
                self.assertIsInstance(newdoor.clearopening_height, measurement.Imperial)
                self.assertIsInstance(newdoor.clearopening_width, measurement.Imperial)


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
                C1 = classes.CastingSet()
                C2 = classes.CastingSet()
                C1._castings = [methods.convert_to_casting(c) for c in c1]
                C2._castings = [methods.convert_to_casting(c) for c in c2]
                self.assertNotEqual(C1,C2)

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

    def test_sortcastings(self):
        """ Tests that sort_castings works as expected """
        TESTVALUES = (
            [], ## Empty does nothing
            ["Standard 4 Pipe", "Standard 4 Spring"], ## 2 Castings in proper order already (does nothing)
            ["Standard 4 Spring", "Standard 4 Pipe"], ## Same castings reversed (4P -> 4S)
            ["Standard 2 Spring", "Standard 4 Spring", "Standard 4 Pipe"], ## 3 Scrambled Castings (4P -> 2S -> 4S)
            ["Standard 6 Spring", "Standard 4 Spring"] ## Missing Pipe and backwards (4S -> 6S)
            )
        TESTRESULTS = (
            [],
            ["Standard 4 Pipe", "Standard 4 Spring"],
            ["Standard 4 Pipe", "Standard 4 Spring"],
            ["Standard 4 Pipe", "Standard 2 Spring", "Standard 4 Spring"],
            ["Standard 4 Spring", "Standard 6 Spring"]
            )
        for (test,result) in zip(TESTVALUES, TESTRESULTS):
            with self.subTest(test = test, result = result):
                casting = classes.CastingSet()
                casting._castings = [methods.convert_to_casting(c) for c in test]
                resultcasting = classes.CastingSet()
                resultcasting._castings = [methods.convert_to_casting(c) for c in result]
                casting._sortcastings()
                self.assertEqual(casting, resultcasting)

    def test_addcasting(self):
        """ Tests that addcasting works as expected """
        cs = classes.CastingSet()
        self.assertEqual(cs.castings, [])

        ## Testing add string
        cs.addcasting("Standard 4 Pipe")
        self.assertEqual(cs.castings, [methods.convert_to_casting("Standard 4 Pipe"),])

        ## Testing add "Instance" (technically dict right now, unless it changes in the future)
        spring = methods.convert_to_casting("Standard 4 Spring")
        cs.addcasting(spring)
        self.assertEqual(cs.castings, [methods.convert_to_casting("Standard 4 Pipe"), spring])

        ## Testing that new Pipe castings replace old ones (highlander rule)
        pipe = methods.convert_to_casting("Standard 6 Pipe")
        cs.addcasting(pipe)
        self.assertEqual(cs.castings, [pipe, spring])

class SpringCase(unittest.TestCase):
    """ Test Case for Springs """

    def test_od_None(self):
        """ Tests that ommitting od results in min_od specified by the wire """
        for testwire in [.25, .375, .5]:
            with self.subTest(testwire = testwire):
                self.assertEqual(classes.Spring(testwire).od, constants.WIRE[testwire]['min_od'])

    def test_bad_od(self):
        """ Tests that the od cannot be set below the min_od """
        for (bad_od,testwire) in [(1,.25), (2.75,.375), (3.75,.5)]:
            with self.subTest(bad_od = bad_od, testwire = testwire):
                self.assertRaisesRegex(ValueError,"Invalid Wire od: od is smaller than Wire's minimum od",
                                       classes.Spring,wire = testwire, od = bad_od)

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




if __name__ == "__main__":
    unittest.main()