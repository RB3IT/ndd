""" NewDadsDoor/tests/test_testmethods.py

    Tests for NewDadsDoor/tests/methods

"""
## Test Target
from NewDadsDoor.tests import methods
from NewDadsDoor.tests.methods import Difference
## Test Framework
import unittest
## This package
from NewDadsDoor import classes, constants, methods as nddmethods

class CompareCase(unittest.TestCase):
    def test_compare_hood(self):
        """ Simple test for compare_hood """
        h1,h2 = classes.Hood(), classes.Hood()
        self.assertEqual(methods.compare_hood(h1,h2),[])
        h1.baffle = True
        self.assertEqual(methods.compare_hood(h1,h2),[Difference("Hood.baffle",(h1.baffle,h2.baffle)),])

    def test_compare_tracks(self):
        """ Simple test for compare_tracks """
        t1,t2 = classes.Tracks(), classes.Tracks()
        self.assertEqual(methods.compare_tracks(t1,t2),[])
        t1.inner = 4.0
        self.assertEqual(methods.compare_tracks(t1,t2),[Difference("Tracks.inner",(t1.inner,t2.inner))])

    def test_compare_shell(self):
        """ Simple test for compare_shell """
        s1,s2 = constants.PIPESIZES[4], constants.PIPESIZES[4]
        self.assertEqual(methods.compare_shell(s1,s2),[])
        s1 = constants.PIPESIZES[6]
        self.assertEqual(methods.compare_shell(s1,s2),[Difference("Shell",(s1,s2))])

    def test_compare_sections(self):
        """ Simple test for compare_sections """
        s1,s2 = classes.SlatSection(), classes.SlatSection()
        self.assertEqual(methods.compare_sections(s1,s2),[])
        s1.slat = classes.Slat(2)
        ## Changing the slat also changes the Increase Radius (in this case)
        self.assertEqual(methods.compare_sections(s1,s2),
                         [Difference("SlatSection.increaseradius",(s1.increaseradius,s2.increaseradius)),
                          Difference("SlatSection.slat",(s1.slat,s2.slat))])

    def test_compare_curtain(self):
        """ Simple test for compare_curtain """
        ## Curtain requires door (may change in future)
        d1,d2 = classes.Door(1.0,1.0), classes.Door(1.0,1.0)
        c1,c2 = classes.Curtain(d1), classes.Curtain(d2)
        self.assertEqual(methods.compare_curtain(c1,c2),[])
        bbar = classes.BottomBar(classes.Slat("2 1/2 INCH FLAT SLAT"))
        c1.append(bbar)
        self.assertEqual(methods.compare_curtain(c1,c2),
                         [Difference("Curtain",
                                     (1,Difference("Second BottomBar is None",(bbar,None)))
                                     ),]
                         )
        c2.append(bbar)
        self.assertEqual(methods.compare_curtain(c1,c2),[])
        s1,s2 = classes.SlatSection(slat = 2), classes.SlatSection(slat = 3)
        c1.append(s1)
        c2.append(s2)
        self.assertEqual(methods.compare_curtain(c1,c2),
                         [Difference("Curtain",
                                     (2,[Difference("SlatSection.increaseradius",
                                                   (s1.increaseradius,s2.increaseradius)),
                                         Difference("SlatSection.slat",
                                                   (s1.slat,s2.slat))]
                                      )
                                     )])

    def test_compare_assembly(self):
        """ Simple test for compare_assembly """
        a1,a2 = classes.Assembly(), classes.Assembly()
        self.assertEqual(methods.compare_assembly(a1,a2),[])

        s1 = nddmethods.build_sockets([classes.Spring(.375),],["Standard 4 Pipe","Standard 4 Spring"])[0]
        a1.addsocket(s1)

        self.assertEqual(methods.compare_assembly(a1,a2),[
            Difference("Assembly Extra Socket",(1,s1)),
            ])

        s2 = nddmethods.build_sockets([classes.Spring(.3125),],["Standard 4 Pipe","Standard 2 Spring"])[0]
        a2.addsocket(s2)

        self.assertEqual(methods.compare_assembly(a1,a2),[
            Difference("Assembly Extra Socket",(1,s1)),
            Difference("Assembly Extra Socket",(2,s2))
            ])

    def test_compare_socket(self):
        """ Simple test for compare_socket """
        s1,s2 = classes.Socket(), classes.Socket()
        self.assertEqual(methods.compare_socket(s1,s2),[])

        sp1 = classes.Spring(.5)
        s1.addspring(sp1)
        self.assertEqual(methods.compare_socket(s1,s2),[
            Difference("Socket Difference",Difference("Extra Spring",(1,sp1)))
            ])

        s2.addspring(sp1)
        self.assertEqual(methods.compare_socket(s1,s2),[])

        c1 = nddmethods.convert_to_casting("Standard 4 Pipe")
        s2.castings.addcasting(c1)
        self.assertEqual(methods.compare_socket(s1,s2),[
            Difference("Socket Difference", Difference("Extra Casting", (2,c1)))
            ])

        

if __name__ == "__main__":
    unittest.main()