
"""
   STANDARD TESTS

   Tests found in this (the root ./tests folder) evaluate classes and methods function as
   intended by their writing. This contrasts with the CompareTestSuite which tests that
   this Package (NewDadsDoor) reflects the output of the original GWBasic Spring  Calculation
   program (DadsDoor) as closesly as possible.

"""

if __name__ == "__main__":
    import unittest
    import pathlib
    path = pathlib.Path.cwd()
    tests = unittest.TestLoader().discover(path)
    unittest.TextTestRunner().run(tests)