import doctest
import unittest
import pymunk
import pkgutil
import sys


def load_tests(loader, tests, ignore):
    for importer, modname, ispkg in pkgutil.iter_modules(pymunk.__path__):
        try:
            tests.addTests(doctest.DocTestSuite("pymunk." + modname))
        except:
            print("Skipping " + modname)
    tests.addTests(doctest.DocTestSuite(pymunk))
    return tests


if __name__ == '__main__':
    print("running doctests")
    suite = unittest.TestSuite()  
    load_tests(None, suite, None)
    res = unittest.TextTestRunner().run(suite)
    sys.exit(not res.wasSuccessful())
    
    