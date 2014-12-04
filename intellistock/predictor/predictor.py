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
        return self

    def getPrediction(self, n = 1):
        self.predState = self.state
        for k in range(1,n+1):
            ret = 2 * self.predState[0] - self.predState[1]
            yield (k, ret, ret-k, ret+k)
            self.predState = np.roll(self.predState, 1)
            self.predState[0] = ret

class PredictorTestSimulation:
    def __init__(self, application):
        self.application = application
        self.figure = None
        self.predictor = None
        self.stepNr = 0
        self.stepMax = 1000
        self.futureMax = 10

    def setPredictor(self, predictor):
        self.predictor = predictor

    def setFigure(self, figure):
        self.figure = figure

    def start_simulation(self):
        self.t = np.linspace(0, 10 * (self.stepMax + self.futureMax) / self.stepMax, self.stepMax + self.futureMax)
        self.x = np.sin(self.t)*0.2 + np.cos(self.t * 10) * 0.02 + np.cos(self.t * 10 + 0.2) * 0.01 + np.cos(self.t * 11 + 0.2) * 0.01 + np.random.randn(self.t.shape[0]) * 5
        self.x = np.convolve(self.x, np.ones(100), 'same') + 200 + np.random.randn(self.t.shape[0])
        self.step_simulation()

    def step_simulation(self):
        if self.stepNr == self.stepMax:
            return True

        if self.figure:
            self.figure.clear()
            #print(self.t.shape)
            #print(self.x.shape)
            self.figure.plot(self.t, self.x, 'b')
            self.figure.draw()

        # if self.predictor:
        #     t1 = self.t[self.stepNr]
        #     t2 = self.t[self.stepNr + self.futureMax]
            
        #     prediction = self.predictor.newInput(self.x[t1]).getPrediction(self.futureMax)
        #     t_pred = self.t[self.stepNr:(self.stepNr + self.futureMax)]
            
        #     pred = np.zeros(t_pred.shape[0])
            
        #     for k,p,mi,ma in prediction:
        #         pred[k-1] = p
                
        #     if self.figure:
        #         self.figure.plot(t_pred, pred, 'r')
        #         self.figure.draw()

        self.stepNr += 1
        #return self.step_simulation()

if __name__ == "__main__":
    np = NaivePredictor()
