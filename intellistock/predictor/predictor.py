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
        self.t_begin = self.t_end = self.t_far_past = self.t_near_past = self.t_max_prediction = None

    def set_figure(self, figure: PlotWidget=None):
        self.figure = figure

    def set_data(self, ts_t: np.ndarray, ts_x: np.ndarray):
        self.ts_t = ts_t
        self.ts_x = ts_x

        self.nr_data = ts_t.shape[0]
        self.indices = np.arange(0, self.nr_data, 1)

    def _multidimensional_gaussian(self):
        nr_training_samples = min(20, self.ts_t.size)
        xx, y, t = create_training_set(np.array([self.ts_t, self.ts_x]), nr_training_samples, 6, 1)

        # Instantiate a Gaussian Process model
        gp = GaussianProcess(corr='cubic', theta0=1e-2, thetaL=1e-4, thetaU=1e-1,
                             random_start=100)
        gp.fit(xx, y)

        # time values
        self.t_begin = self.ts_t[0]
        self.t_end = self.ts_t[self.nr_data-1]
        self.t_far_past = max(self.t_end - make_far_prediction_from_time, self.t_begin)
        self.t_near_past = max(self.t_end - make_near_prediction_from_time, self.t_begin)
        self.t_max_prediction = min(self.t_end + max_prediction_time, 2 * self.t_end - self.t_begin)

        prediction_ticks = 20

        # Make the prediction on the meshed x-axis (ask for MSE as well)
        query = xx[len(xx)-1, :]
        query[0] = y[len(xx)-1]
        query = np.roll(query,shift=-1)
        step = (t[len(xx)-1] - t[0]) / prediction_ticks

        t_tick = [self.t_end]
        v_tick = [y[len(xx)-1]]
        # step = 0.01 / 365
        for i in range(prediction_ticks):
            y_pred, MSE = gp.predict(query, eval_MSE=True)
            query[0] = y_pred
            query = np.roll(query,shift=-1)
            t_tick.append(t_tick[len(t_tick)-1] + step)
            v_tick.append(y_pred)

        # modifying UI on a background thread! Ohh! In fact self.figure is thread-safe :)
        self.figure.plot(t_tick, v_tick, 'y-', label='multidim pred', linewidth=3)
        self.figure.legend(loc='upper left')
        self.figure.draw()

    def _linear_regression(self):
        near_past_index = int(np.interp(self.t_near_past, self.ts_t, self.indices))
        t_linear = np.atleast_2d(self.ts_t[near_past_index:]).T
        x_linear = np.atleast_2d(self.ts_x[near_past_index:]).T
        t_linear_future = np.atleast_2d(np.linspace(self.t_near_past, self.t_max_prediction, 1000)).T

        regr = linear_model.LinearRegression()
        regr.fit(t_linear, x_linear)

        self.figure.plot(t_linear_future, regr.predict(t_linear_future), color='green', label='expected tendency (linear regression)',
                         linewidth=3)
        self.figure.legend(loc='upper left')
        self.figure.draw()

    def _gradient_boosting_regressor(self):
        far_past_index = int(np.interp(self.t_far_past, self.ts_t, self.indices))
        t_ensemble = np.atleast_2d(self.ts_t[far_past_index:]).T
        x_ensemble = np.atleast_2d(self.ts_x[far_past_index:]).T.ravel()
        t_ensemble_future = np.atleast_2d(np.linspace(self.t_far_past, self.t_max_prediction, 10000)).T

        alpha = 0.95
        clf = GradientBoostingRegressor(loss='quantile', alpha=alpha,
                                        n_estimators=250, max_depth=3,
                                        learning_rate=.1, min_samples_leaf=9,
                                        min_samples_split=20)
        clf.fit(t_ensemble, x_ensemble)

        # Make the prediction on the meshed x-axis
        y_upper = clf.predict(t_ensemble_future)

        clf.set_params(alpha=1.0 - alpha)
        clf.fit(t_ensemble, x_ensemble)

        # Make the prediction on the meshed x-axis
        y_lower = clf.predict(t_ensemble_future)

        clf.set_params(loss='ls')
        clf.fit(t_ensemble, x_ensemble)

        # Make the prediction on the meshed x-axis
        y_prediction = clf.predict(t_ensemble_future)

        self.figure.plot(t_ensemble_future, y_prediction, 'r-', label=u'Prediction')
        self.figure.plot(t_ensemble_future, y_upper, 'k-')
        self.figure.plot(t_ensemble_future, y_lower, 'k-')
        self.figure.fill(np.concatenate([t_ensemble_future, t_ensemble_future[::-1]]),
                         np.concatenate([y_upper, y_lower[::-1]]),
                         alpha=.5, fc='b', ec='None', label='90% prediction interval')
        self.figure.legend(loc='upper left')
        self.figure.draw()

    def run(self):
        if self.ts_t.size < 10:
            return
        self._multidimensional_gaussian()
        self._linear_regression()
        self._gradient_boosting_regressor()


class DataProcessor:
    def __init__(self, figure: PlotWidget=None, predictor: Predictor=None):
        """"""
        # declare attributes
        self.ts_t = self.ts_x = None
        self.predictor = predictor
        self.figure = figure

    def set_predictor(self, predictor):
        self.predictor = predictor

    def set_data(self, raw_data: map=None, time_series: np.array=None, append = False):
        """
        :param raw_data:
        :param time_series:
        :return:
        """
        if raw_data:
            self.ts_t = np.asarray(list(map(lambda t: int2year(t[1]), raw_data)), dtype=float)
            self.ts_x = np.asarray(list(map(lambda t: t[2], raw_data)), dtype=float)

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

    def update(self):
        print("DataProcessor::update - not implemented yet")
        self.figure.clear()
        self.figure.draw()

    def _plot_observations(self):
        self.figure.plot(self.ts_t, self.ts_x, 'b.-', markersize=10, label='Observations')
        self.figure.set_axes_labels("time [year]", "stock price [Ft]")
        self.figure.set_axis_offset()
        self.figure.legend(loc='upper left')
        self.figure.draw()

if __name__ == "__main__":
    np = NaivePredictor()
