import argparse
import doctest
import faulthandler
import os
import os.path
import platform
import sys
import unittest
from typing import Any, Iterator

import cffi  # type: ignore

from . import doctests


def main(args: Any) -> None:
    def list_of_tests_gen(s: Any) -> Iterator[Any]:
        for test in s:
            if unittest.suite._isnotsuite(test):  # type: ignore
                yield test
            else:
                for t in list_of_tests_gen(test):
                    yield t

    path = os.path.dirname(os.path.abspath(__file__))
    suite = unittest.TestLoader().discover(path)

    doctests.load_tests(suite, args.dependencies)

    wasSuccessful = True

    filtered_suite = unittest.TestSuite()

    if args.filter is not None:
        test_filter = args.filter
        for test in list_of_tests_gen(suite):
            if (
                isinstance(test, doctest.DocTestCase)
                and test_filter.startswith("doctest")
                or test_filter in str(test.id())
            ):
                filtered_suite.addTest(test)
    else:
        filtered_suite = suite

    res = unittest.TextTestRunner(verbosity=2).run(filtered_suite)
    wasSuccessful = res.wasSuccessful()

    sys.exit(not wasSuccessful)


if sys.argv[0].endswith("__main__.py"):
    # We change sys.argv[0] to make help message more useful
    # use executable without path, unquoted
    # (it's just a hint anyway)
    # (if you have spaces in your executable you get what you deserve!)
    executable = os.path.basename(sys.executable)
    sys.argv[0] = executable + " -m pymunk.tests"


desc = """
Run the Pymunk unittests.
Note that by default it does not run with external dependencies. 
See the -d flag for details.
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-d",
        "--dependencies",
        choices=["pygame", "pyglet", "matplotlib"],
        nargs="*",
        help="Include tests with these dependencies",
        default=[],
    )
    parser.add_argument("-f", "--filter", help="Only run tests matching the filter")
    args = parser.parse_args()

    faulthandler.enable()
    print("RUNNING pymunk.tests ##################")
    print("Python / platform:")
    print(sys.version)
    print(f"on {platform.system()} {platform.machine()} using cffi {cffi.__version__}")
    print("")

    print(args)
    # sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    main(args)
