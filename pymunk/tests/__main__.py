import unittest
import doctest
import sys
import os

def main():
    
    def list_of_tests_gen(s):
        for test in s:
            if unittest.suite._isnotsuite(test):
                yield test
            else:
                for t in list_of_tests_gen(test):
                    yield t

    from . import doctests
    
    path = os.path.dirname(os.path.abspath(__file__))
    suite = unittest.TestLoader().discover(path)

    doctests.load_tests(None, suite, None)

    wasSuccessful = True

    filtered_suite = unittest.TestSuite()

    if len(sys.argv) > 1:
        test_filter = sys.argv[1]
        for test in list_of_tests_gen(suite):
            if isinstance(test, doctest.DocTestCase) \
                and test_filter.startswith("doctest") \
                or test_filter in str(test.id()):
                filtered_suite.addTest(test)

    elif sys.version_info.major < 3:
        print("Skipping doctests"
              " (Doctests uses formatting that differ between Py2 and 3"
              " and the Pymunk doctests target Python 3")
        for test in list_of_tests_gen(suite):
            if not isinstance(test, doctest.DocTestCase):
                filtered_suite.addTest(test)
    else:
        filtered_suite = suite
    
    res = unittest.TextTestRunner(verbosity=2).run(filtered_suite)
    wasSuccessful = res.wasSuccessful()

    sys.exit(not wasSuccessful)
    
if __name__ == '__main__':
    import os
    import sys
    #sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    main()