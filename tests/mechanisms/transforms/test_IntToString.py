import numpy as np
from unittest import TestCase

from diffprivlib.mechanisms import ExponentialHierarchical
from diffprivlib.mechanisms.transforms import IntToString


class TestIntToString(TestCase):
    def test_not_none(self):
        mech = IntToString(ExponentialHierarchical())
        self.assertIsNotNone(mech)
        _mech = mech.copy()
        self.assertIsNotNone(_mech)

    def test_class(self):
        from diffprivlib.mechanisms import DPMachine
        from diffprivlib.mechanisms.transforms import DPTransformer
        self.assertTrue(issubclass(IntToString, DPMachine))
        self.assertTrue(issubclass(IntToString, DPTransformer))

    def test_no_parent(self):
        with self.assertRaises(TypeError):
            IntToString()

    def test_randomise(self):
        mech = IntToString(ExponentialHierarchical().set_hierarchy(["0", "1", "2", "3"]).set_epsilon(1))
        self.assertIsInstance(mech.randomise(1), int)

    def test_distrib(self):
        epsilon = np.log(2)
        runs = 10000
        mech = IntToString(ExponentialHierarchical().set_hierarchy(["0", "1", "2", "3"]).set_epsilon(epsilon))
        count = [0, 0]

        for _ in range(runs):
            val = mech.randomise(0)
            if val == 0:
                count[0] += 1

            val = mech.randomise(1)
            if val == 0:
                count[1] += 1

        self.assertGreater(count[0], count[1])
        self.assertLessEqual(count[0] / runs, count[1] * np.exp(epsilon) / runs + 0.05)
