"""
    COMPARISON TESTS

    This module compares output from the Original Spring Calculation program
    (DadsDoor) with the current output from this Package.

"""

if __name__=="__main__":
    ## Custom Module
    from alcustoms import tests
    ## This Module
    import classes

    testmodules = [classes,]

    tests.runtestmodules(testmodules,sortmethod=tests.sortbylinenumber, fail = True)