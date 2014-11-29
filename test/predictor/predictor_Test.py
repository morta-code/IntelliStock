
# TODO - ezt lehetne egy kicsit ugyesebben is megoldani : relative import
import sys
sys.path.append("../../")

import predictor as pred
import numpy as np

import random
import unittest

class NaivePredictor_Test(unittest.TestCase):

    def pcz_checkPredictorState(self, *l):
        self.assertEqual(self.predictor.state.tolist(), list(l))

    def setUp(self):
        self.regsize = 2
        self.predictor = pred.NaivePredictor(memory=self.regsize)

    def test_newInput(self):
        self.pcz_checkPredictorState(0, 0)

        self.predictor.newInput(1.0)
        self.pcz_checkPredictorState(1, 0)

        self.predictor.newInput(2.0)
        self.pcz_checkPredictorState(2, 1)

    def test_getPrediction(self):
        self.test_newInput()

        pred = self.predictor.getPrediction(5)
        self.assertEqual(next(pred), (1, 3, 2, 4))
        self.assertEqual(next(pred), (2, 4, 2, 6))
        self.assertEqual(next(pred), (3, 5, 2, 8))


# class TestSequenceFunctions(unittest.TestCase):

#     def setUp(self):
#         self.seq = list(range(10))

#     def test_shuffle(self):
#         # make sure the shuffled sequence does not lose any elements
#         random.shuffle(self.seq)
#         self.seq.sort()
#         self.assertEqual(self.seq, list(range(10)))

#         # should raise an exception for an immutable sequence
#         self.assertRaises(TypeError, random.shuffle, (1,2,3))

#     def test_choice(self):
#         element = random.choice(self.seq)
#         self.assertTrue(element in self.seq)

#     def test_sample(self):
#         with self.assertRaises(ValueError):
#             random.sample(self.seq, 20)
#         for element in random.sample(self.seq, 5):
#             self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()