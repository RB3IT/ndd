"""  NewDadsDoor.tests.utils.methods

    Utilties for testing NewDadsDoor.methods

"""
from NewDadsDoor import classes as c, constants


BUILD_SOCKET_VALUES = [
    (
        ([],[]), []
        ),

    ( ## 2.75 Inch Spring
        ## Test
        ([c.Spring(wire=.1875, od=2.75, ),],
         ["Standard 4 Pipe", "Standard 2 Spring"]),
         ## Result
         [c.Socket(c.Spring(wire=.1875, od=2.75, ),
                            castings = c.CastingSet("Standard 4 Pipe", "Standard 2 Spring"))]
        ),

    ( ## 3.75 Inch Spring
        ## Test
        ([c.Spring(wire=.3125, od=3.75,),],
         [ "Standard 4 Pipe", "Standard 4 Spring"]),
         ## Result
         [c.Socket(c.Spring(wire=.3125, od=3.75),
                   castings = c.CastingSet("Standard 4 Pipe", "Standard 4 Spring"))]
        ),

    ( ## 5.625 Inch Spring
        ## Test
        ([c.Spring(wire=.5, od=5.625,),],
         [ "Standard 6 Pipe", "Standard 6 Spring"]),
         ## Result
         [c.Socket(c.Spring(wire=.5, od=5.625),
                   castings = c.CastingSet("Standard 6 Pipe", "Standard 6 Spring"))]
        ),

    ( ## 4 Inch Compound Assembly
        ## Test
        ([c.Spring(wire = .4375, od = 3.75), c.Spring(wire = .25, od = 2.75)],
         [ "Standard 4 Pipe",  "Standard 4 Spring", "Standard 2 Spring"]),
        ## Result
        [c.Socket(c.Spring(wire = .4375, od = 3.75), c.Spring(wire = .25, od = 2.75),
                  castings = c.CastingSet("Standard 4 Pipe", "Standard 4 Spring", "Standard 2 Spring"))]
        ),

    ( ## 6 Inch Compound Assembly
        ## Test
        ([c.Spring(wire=.625, od = 5.625), c.Spring(wire = .3125, od = 3.75)],
         ["Standard 6 Pipe", "Standard 4 Spring", "Standard 6 Spring"]),
        ## Result
        [c.Socket(c.Spring(wire=.625, od = 5.625), c.Spring(wire = .3125, od = 3.75),
                  castings = c.CastingSet("Standard 6 Pipe", "Standard 6 Spring", "Standard 4 Spring"))]
        ),

    ( ## 4 Inch Duplex
        ## Test
        ([c.Spring(wire = .46875, od = 3.75), c.Spring(wire = .46875, od = 3.75)],
         ["Standard 4 Pipe", "Standard 4 Spring", "Standard 4 Pipe", "Standard 4 Spring"]),
        ## Result
        [c.Socket(c.Spring(wire = .46875, od = 3.75),
                  castings = c.CastingSet("Standard 4 Pipe", "Standard 4 Spring")),
         c.Socket(c.Spring(wire = .46875, od = 3.75),
                  castings = c.CastingSet("Standard 4 Pipe", "Standard 4 Spring")),]
        ),

    ( ## 6 Inch Duplex
        ## Test
        ([c.Spring(wire = .5, od = 5.625), c.Spring(wire = .5, od = 5.625)],
         ["Standard 6 Pipe", "Standard 6 Spring", "Standard 6 Pipe", "Standard 6 Spring"]),
        ## Result
        [c.Socket(c.Spring(wire = .5, od = 5.625),
                  castings = c.CastingSet("Standard 6 Pipe", "Standard 6 Spring")),
         c.Socket(c.Spring(wire = .5, od = 5.625),
                  castings = c.CastingSet("Standard 6 Pipe", "Standard 6 Spring")),]
        ),

    ( ## 4 Inch Compound + Duplex
        ## Test
        ([c.Spring(wire = .3125, od = 2.75), c.Spring(wire = .46875, od = 3.75), c.Spring(wire = .46875, od = 3.75)],
         ["Standard 4 Pipe", "Standard 4 Spring", "Standard 4 Pipe", "Standard 4 Spring", "Standard 2 Spring"]),
        ## Result
        [c.Socket(c.Spring(wire = .46875, od = 3.75), c.Spring(wire = .3125, od = 2.75),
                  castings = c.CastingSet("Standard 4 Pipe", "Standard 4 Spring", "Standard 2 Spring")),
         c.Socket(c.Spring(wire = .46875, od = 3.75),
                  castings = c.CastingSet("Standard 4 Pipe", "Standard 4 Spring")),]
        ),

    ( ## 6 Inch Compound + Duplex
        ## Test
        ([c.Spring(wire = .5, od = 5.625), c.Spring(wire = .5, od = 5.625), c.Spring(wire = .4375, od = 3.75)],
         ["Standard 6 Pipe", "Standard 6 Spring", "Standard 6 Pipe", "Standard 4 Spring", "Standard 6 Spring"]),
        ## Result
        [c.Socket(c.Spring(wire = .5, od = 5.625),
                  castings = c.CastingSet("Standard 6 Pipe", "Standard 6 Spring")),
         c.Socket(c.Spring(wire = .5, od = 5.625), c.Spring(wire = .4375, od = 3.75),
                  castings = c.CastingSet("Standard 6 Pipe", "Standard 6 Spring", "Standard 4 Spring")),]
        ),
    ]