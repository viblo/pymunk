import argparse
import logging
import os
import os.path
import sys

from . import run_tests

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
    parser.add_argument(
        "-v", "--verbose", help="Enable debug logging", action="store_true"
    )
    args = parser.parse_args()

    print(args)
    if args.verbose:
        logging.basicConfig(level=0)
    # sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    wasSuccessful = run_tests(args.filter, args.dependencies)
    sys.exit(not wasSuccessful)
