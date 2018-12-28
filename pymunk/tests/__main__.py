import unittest
import doctest
import sys
import os

def main():

    from . import doctests
    
    path = os.path.dirname(os.path.abspath(__file__))
    suite = unittest.TestLoader().discover(path)

    doctests.load_tests(None, suite, None)

    wasSuccessful = True

    filtered_suite = unittest.TestSuite()

    if len(sys.argv) > 1:
        m = sys.argv[1]

        def list_of_tests_gen(s):
            for test in s:
                if unittest.suite._isnotsuite(test):
                    yield test
                else:
                    for t in list_of_tests_gen(test):
                        yield t

        for test in list_of_tests_gen(suite):
            if isinstance(test, doctest.DocTestCase) \
                and m.startswith("doctest") \
                or m in str(test.id()):
                filtered_suite.addTest(test)
        suite = filtered_suite
    
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    wasSuccessful = res.wasSuccessful()

    sys.exit(not wasSuccessful)
    

if __name__ == '__main__':
    import os
    import sys
    #sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    main()