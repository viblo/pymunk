import pickle
import unittest

import pymunk as p


class UnitTestTransform(unittest.TestCase):
    def testPickle(self) -> None:
        x = p.Transform.identity()
        s = pickle.dumps(x, 2)
        actual = pickle.loads(s)
        self.assertEqual(x, actual)
