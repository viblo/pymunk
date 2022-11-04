"""
The Pymunk test suite.

The tests cover most of Pymunk and is quick to run. However, some parts 
requires an additional dependency to tests, e.g. to test pygame the pygame 
library must be installed. 

Tests can be run both by running the module from a shell::

$> python -m pymunk.tests

But also by importing and running the run_tests method from a python prompt::

    > from pymunk.tests import run_tests
    > run_tests()

Some arguments are allowed to the tests. You can show them with the --help 
flag::

    $> python pymunk.tests --help

It is possible to filter out tests with the filter parameter. Tests containing 
the filter will be run, the others skipped. A special case is doctests, which 
can be matched against the filter doctest::

$> python -m pymunk.tests -f testTransform
$> python -m pymynk.tests -f doctest

By default all tests will run except those with an additional dependency. To 
run tests with dependencies, specify them with the -d parameter::

$> python -m pymunk.tests -d pygame

Note that the tests covers most/all of Pymunk, but does not test the 
underlying Chipmunk library in a significant way except as a side effect of 
testing Pymunk features.
"""

import doctest
import faulthandler
import logging
import os
import os.path
import platform
import sys
import unittest
from typing import Any, Iterator, List

import cffi  # type: ignore

from . import doctests


def run_tests(filter: str = "", with_dependencies: List[str] = []) -> bool:
    """Run the Pymunk test suite."""

    faulthandler.enable()
    print("####################")
    print("RUNNING pymunk.tests")
    print("Python / platform:")
    print(sys.version)
    print(f"on {platform.system()} {platform.machine()} using cffi {cffi.__version__}")
    print("")

    def list_of_tests_gen(s: Any) -> Iterator[Any]:
        for test in s:
            if unittest.suite._isnotsuite(test):  # type: ignore
                yield test
            else:
                for t in list_of_tests_gen(test):
                    yield t

    path = os.path.dirname(os.path.abspath(__file__))
    suite = unittest.TestLoader().discover(path)

    doctests.load_tests(suite, with_dependencies)

    filtered_suite = unittest.TestSuite()

    if filter is not None:
        for test in list_of_tests_gen(suite):
            if (
                isinstance(test, doctest.DocTestCase)
                and filter.startswith("doctest")
                or filter in str(test.id())
            ):
                filtered_suite.addTest(test)
    else:
        filtered_suite = suite

    res = unittest.TextTestRunner(verbosity=2).run(filtered_suite)
    return res.wasSuccessful()
