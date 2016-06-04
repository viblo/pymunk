import doctest
import unittest
import pymunk


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(pymunk))
    return tests