""" NewDadsDoor.tests.utils.pipecalculations

    Utilities for testing pipecalculations
"""
## This Module
from NewDadsDoor import classes

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