##
#  file:   predictor.py
#  author: Polcz Péter <ppolcz@gmail.com> 
# 
#  Created on Sat Nov 29 15:41:43 CET 2014
#

import sklearn

import numpy as np
from inspect import currentframe
import matplotlib.pyplot as plt

from intellistock.predictor.pczdebug import pczdebug
from intellistock.data.data import int2year
from intellistock.ui.plotwidget import PlotWidget

from threading import Thread

class Predictor(Thread):
    def __init__(self, figure=None, ts_t: np.ndarray=None, ts_x: np.ndarray=None):
        """"""
        Thread.__init__(self)
        self.figure = figure
        self.ts_t = ts_t
        self.ts_x = ts_x

    def set_figure(self, figure: PlotWidget=None):
        self.figure = figure

    def set_data(self, ts_t: np.ndarray, ts_x: np.ndarray):
        self.ts_t = ts_t
        self.ts_x = ts_x

    @DeprecationWarning
    def newInput(self, x, t = 0):
        pass

    @DeprecationWarning
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


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from sklearn import linear_model
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.gaussian_process import GaussianProcess

from intellistock.predictor.predictor_helper import create_training_set

# constant values
max_prediction_time_in_days = 1
max_prediction_time = max_prediction_time_in_days / 365

make_near_prediction_from_time_in_days = 1
make_near_prediction_from_time = make_near_prediction_from_time_in_days / 365

make_far_prediction_from_time_in_days = 60
make_far_prediction_from_time = make_far_prediction_from_time_in_days / 365

class EnsemblePredictor(Predictor):
    """"""
    def __init__(self, figure=None, *_, __ts_t: np.ndarray=None, __ts_x: np.ndarray=None):
        """"""
        Predictor.__init__(self)
        self.figure = figure
        self.ts_t = __ts_t
        self.ts_x = __ts_x

        # declare other attributes
        self.indices = self.nr_data = None

    def set_figure(self, figure: PlotWidget=None):
        self.figure = figure

    def set_data(self, ts_t: np.ndarray, ts_x: np.ndarray):
        self.ts_t = ts_t
        self.ts_x = ts_x

        self.nr_data = ts_t.shape[0]
        self.indices = np.arange(0, self.nr_data, 1)
        pczdebug(currentframe(), self.nr_data, self.indices)

    def run(self):
        xx, y, _ = create_training_set(np.array([self.ts_t, self.ts_x]), 20, 6, 1)
        print(xx)
        print(y)

        # Instantiate a Gaussian Process model
        gp = GaussianProcess(corr='cubic', theta0=1e-2, thetaL=1e-4, thetaU=1e-1,
                             random_start=100)

        gp.fit(xx, y)

        # time values
        t_begin = self.ts_t[0]
        t_end = self.ts_t[self.nr_data-1]
        t_far_past = t_end - make_far_prediction_from_time
        t_near_past = t_end - make_near_prediction_from_time
        t_max_prediction = t_end + max_prediction_time

        # Make the prediction on the meshed x-axis (ask for MSE as well)
        query = xx[len(xx)-1, :]
        query[0] = y[len(xx)-1]
        query = np.roll(query,shift=-1)

        t_tick = [t_end]
        v_tick = [y[len(xx)-1]]
        step = 0.01 / 365
        for i in range(20):
            # print(query)
            y_pred, MSE = gp.predict(query, eval_MSE=True)
            print(y_pred, np.sqrt(MSE))
            query[0] = y_pred
            query = np.roll(query,shift=-1)
            t_tick.append(t_tick[len(t_tick)-1] + step)
            v_tick.append(y_pred)
        self.figure.plot(t_tick, v_tick, 'y-', label='multidim pred', linewidth=3)
        self.figure.get_axes().legend(loc='upper left')
        self.figure.draw()
        pass


class DataProcessor:
    def __init__(self, figure: PlotWidget=None, predictor: Predictor=None):
        """"""
        # declare attributes
        self.ts_t = self.ts_x = None
        self.predictor = predictor
        self.figure = figure

    def set_predictor(self, predictor):
        self.predictor = predictor

    def set_data(self, raw_data: map=None, time_series: np.array=None):
        """
        :param raw_data:
        :param time_series:
        :return:
        """
        if raw_data:
            self.ts_t = np.asarray(list(map(lambda t: int2year(t[1]), raw_data)), dtype=float)
            self.ts_x = np.asarray(list(map(lambda t: t[2], raw_data)), dtype=float)
            pczdebug(currentframe(), self.ts_t, self.ts_x, sep="\n")

        if time_series:
            pass

        if self.predictor:
            self.predictor.set_data(self.ts_t, self.ts_x)

    def set_figure(self, figure: PlotWidget=None):
        self.figure = figure

        if self.predictor:
            self.predictor.set_figure(figure)

    def process(self):
        self._plot_observations()
        if self.predictor:
            self.predictor.start()

    def _plot_observations(self):
        axes = self.figure.get_axes()
        axes.plot(self.ts_t, self.ts_x, 'b.-', markersize=10, label='Observations')
        self.figure.set_axes_labels("time [year]", "stock price [Ft]")
        self.figure.set_axis_offset()
        self.figure.draw()
        axes.legend(loc='upper left')

if __name__ == "__main__":
    np = NaivePredictor()
