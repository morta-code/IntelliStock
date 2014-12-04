##
#  file:   predictor.py
#  author: Polcz Péter <ppolcz@gmail.com> 
# 
#  Created on Sat Nov 29 15:41:43 CET 2014
#

# import sklearn 

import numpy as np

class Predictor:
    def __init__(self):
        pass

    def newInput(self, x, t = 0):
        pass

    # returns a list of tuples: 
    # (k, predicted value, estimated error lower bound, estimated error upper bound)
    def getPrediction(self, n = 1):
        pass



class NaivePredictor(Predictor):
    def __init__(self, memory = 10):
        self.memory = memory
        self.state = np.zeros(self.memory)

    def newInput(self, x):
        self.state = np.roll(self.state, 1)
        self.state[0] = x

    def getPrediction(self, n = 1):
        self.predState = self.state
        for k in range(1,n+1):
            ret = 2 * self.predState[0] - self.predState[1]
            yield (k, ret, ret-k, ret+k)
            self.predState = np.roll(self.predState, 1)
            self.predState[0] = ret



if __name__ == "__main__":
    np = NaivePredictor()
