##
#  file:   predictor.py
#  author: Polcz Péter <ppolcz@gmail.com> 
# 
#  Created on Sat Nov 29 15:41:43 CET 2014
#

from intellistock.data.data import int2year, date2year
from intellistock.ui.plotwidget import PlotWidget
from intellistock.predictor.predictor_helper import create_training_set, create_training_set_2, create_training_test_set

from threading import Thread, Event

import numpy as np

from sklearn import linear_model
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.gaussian_process import GaussianProcess


class Predictor(Thread):
    def __init__(self, figure: PlotWidget=None, ts_t: np.ndarray=None, ts_x: np.ndarray=None):
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

    def hide(self, plh: int, hide: bool=True):
        pass


class NaivePredictor(Predictor):
    def __init__(self, memory = 10):
        self.memory = memory
        self.state = np.zeros(self.memory)

    def new_input(self, x):
        self.state = np.roll(self.state, 1)
        self.state[0] = x
        return self

    def get_prediction(self, n = 1):
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

        self.stepNr += 1


class EnsemblePredictor(Predictor):
    """
    1.) multidimensional Gaussian prediction
    2.) linear one dimensional prediction
    3.) gradient boosting regression on past data
    """

    PLH_ALL = -1
    PLH_GAUSSIAN = 1
    PLH_LINEAR = 2
    PLH_GRAD_BOOSTING = 4

    def __init__(self, figure: PlotWidget=None, *_, __ts_t: np.ndarray=None, __ts_x: np.ndarray=None):
        """"""
        Predictor.__init__(self)
        self.figure = figure
        self.ts_t = __ts_t
        self.ts_x = __ts_x

        # declare other attributes
        self.indices = self.nr_data = None
        self.t_begin = self.t_present = self.t_far_past = self.t_near_past = self.t_max_prediction = self.t_min_prediction = None
        self.plh_linear = self.plh_gauss = self.plh_gbr = None

        # event object for simulating the wait-notify pattern
        self._event = Event()

        # time parameters got from UI
        self._tp = {}

        # flags
        self._interrupted = self._tp_changed = self._data_set_changed = False

        # time parameter values
        self.near_future = 6 / 24 / 365
        self.far_future = 1 / 365
        self.near_past = 1 / 365
        self.far_past = 60 / 365

        self.maxn = 1000
        self.nth = 1
        self.dim = 6
        self.dt_samples = 10 / 3600 / 24 / 365

        self.simulation = False

    def generate_time_params(self):
        try:
            self.near_past = self._tp["nearp"] / 24 / 365
            # self.far_past = self._tp["farp"] / 365
            self.near_future = self._tp["nearf"] / 24 / 365
            # self.far_future = self._tp["farf"] / 365

            if self._tp["maxn"] != 0:
                self.maxn = self._tp["maxn"]
            if self._tp["dim"] != 0:
                self.dim = self._tp["dim"]
            if self._tp["dt"] != 0:
                self.dt_samples = self._tp["dt"] / 3600 / 24 / 365
        except KeyError as e:
            print('KeyError:', e)

    def set_figure(self, figure: PlotWidget=None):
        self.figure = figure

    def set_data(self, ts_t: np.ndarray, ts_x: np.ndarray):
        self.ts_t = ts_t
        self.ts_x = ts_x

        self.nr_data = ts_t.shape[0]
        self.indices = np.arange(0, self.nr_data, 1)

    def generate_time_values(self):
        self.t_begin = self.ts_t[0]
        self.t_present = self.ts_t[self.nr_data-1]
        self.t_far_past = max(self.t_present - self.far_past, self.t_begin)
        self.t_near_past = max(self.t_present - self.near_past, self.t_begin)
        self.t_max_prediction = min(self.t_present + self.far_future, 2 * self.t_present - self.t_begin)
        self.t_min_prediction = min(self.t_present + self.near_future, 2 * self.t_present - self.t_begin)

    def _multidimensional_gaussian(self, update=False):
        print(self.dim)
        # nr_training_samples = min(20, self.ts_t.size)
        # print(sorted(set(myList)))
        # xx, y, t = create_training_set(np.array([self.ts_t, self.ts_x]), nr_training_samples, self.dim, self.nth)
        # xx, y, t = create_training_set_2(np.array([self.ts_t, self.ts_x]), self.maxn, self.dim, self.dt_samples)
        xx, y, t, xx_test, y_test, t_test = create_training_test_set(np.array([self.ts_t, self.ts_x]), self.maxn, self.dim, self.dt_samples)

        print(xx_test, t_test, y_test, len(t_test))

        # Instantiate a Gaussian Process model
        gp = GaussianProcess(corr='cubic', theta0=1e-2, thetaL=1e-4, thetaU=1e-1, random_start=100)
        gp.fit(xx, y)
        print(gp.score(xx_test, y_test))

        prediction_ticks = 20

        # Make the prediction on the meshed x-axis (ask for MSE as well)
        query = xx[len(xx)-1, :]
        query[0] = y[len(xx)-1]
        query = np.roll(query,shift=-1)
        step = (t[len(xx)-1] - t[0]) / prediction_ticks

        t_tick = [self.t_present]
        v_tick = [y[len(xx)-1]]
        # step = 0.01 / 365
        for i in range(prediction_ticks):
            y_pred, mse = gp.predict(query, eval_MSE=True)
            query[0] = y_pred
            query = np.roll(query,shift=-1)
            t_tick.append(t_tick[len(t_tick)-1] + step)
            v_tick.append(y_pred)

        # modifying UI on a background thread! Ohh! In fact self.figure is thread-safe :)
        self.plh_gauss = self.figure.plot(t_tick, v_tick, 'y-', label='multidim. pred', linewidth=3)
        self.plh_gauss.extend(self.figure.plot(t, y, 'b.', markersize=10, color='red', label='observations'))
        self.figure.legend(loc='upper left')
        if not self._tp['pl_guass']:
            self.figure.hide_line(ploth=self.plh_gauss)
        self.figure.draw()

    def _linear_regression(self, update=False):
        near_past_index = int(np.interp(self.t_near_past, self.ts_t, self.indices))
        t_linear = np.atleast_2d(self.ts_t[near_past_index:]).T
        x_linear = np.atleast_2d(self.ts_x[near_past_index:]).T
        t_linear_future = np.atleast_2d(np.linspace(self.t_near_past, self.t_min_prediction, 1000)).T

        regr = linear_model.LinearRegression()
        regr.fit(t_linear, x_linear)

        self.plh_linear = self.figure.plot(t_linear_future, regr.predict(t_linear_future), color='green', label='linear pred', linewidth=3)
        if not self._tp['pl_linear']:
            self.figure.hide_line(ploth=self.plh_linear)
        self.figure.legend(loc='upper left')
        self.figure.draw()

    def _gradient_boosting_regressor(self, update=False):
        if self.simulation:
            return

        far_past_index = int(np.interp(self.t_far_past, self.ts_t, self.indices))
        t_ensemble = np.atleast_2d(self.ts_t[far_past_index:]).T
        x_ensemble = np.atleast_2d(self.ts_x[far_past_index:]).T.ravel()
        t_ensemble_future = np.atleast_2d(np.linspace(self.t_far_past, self.t_present, 10000)).T

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

        self.plh_gbr = self.figure.plot(t_ensemble_future, y_prediction, 'r-')
        self.plh_gbr.extend(self.figure.plot(t_ensemble_future, y_upper, 'k-'))
        self.plh_gbr.extend(self.figure.plot(t_ensemble_future, y_lower, 'k-'))
        self.plh_gbr.extend(self.figure.fill(
            np.concatenate([t_ensemble_future, t_ensemble_future[::-1]]), np.concatenate([y_upper, y_lower[::-1]]),
            alpha=.5, fc='b', ec='None'))
        if not self._tp['pl_gbr']:
            self.figure.hide_line(ploth=self.plh_gbr)
        self.figure.legend(loc='upper left')
        self.figure.draw()

    def run(self):
        if self.ts_t.size < 10:
            return

        update = False
        while not self.interrupted():
            self._event.clear()
            print("predictor:run: waiting for update...")
            self._event.wait()
            print("predictor:run: processing...")

            if self.simulation:
                self.clear_all()
                self.generate_time_values()
                if self.interrupted():
                    return
                self._linear_regression(update)
                print("predictor:rum: simulation stepped on the plot")
            if self._tp_changed:
                self.clear_all()
                self.generate_time_values()
                if self.interrupted():
                    return
                self._multidimensional_gaussian(update)
                if self.interrupted():
                    return
                self._linear_regression(update)
                if self.interrupted():
                    return
                self._gradient_boosting_regressor(update)
                update = True

    def interrupt(self):
        self._interrupted = True
        self._event.set()

    def interrupted(self):
        ret = self._interrupted
        self._interrupted = False
        return ret

    def hide(self, plh: int, hide: bool=True):
        if plh & EnsemblePredictor.PLH_GAUSSIAN:
            self.figure.hide_line(ploth=self.plh_gauss, hide=hide)
        if plh & EnsemblePredictor.PLH_GRAD_BOOSTING:
            self.figure.hide_line(ploth=self.plh_gbr, hide=hide)
        if plh & EnsemblePredictor.PLH_LINEAR:
            self.figure.hide_line(ploth=self.plh_linear, hide=hide)
        self.legend()
        self.figure.draw()

    def clear_all(self):
        if self.plh_gbr:
            self.figure.erase_line(ploth=self.plh_gbr)
        if self.plh_gauss:
            self.figure.erase_line(ploth=self.plh_gauss)
        if self.plh_linear:
            self.figure.erase_line(ploth=self.plh_linear)

    def legend(self):
        self.figure.legend(loc='upper left')

    # @staticmethod
    # def _args2dict(**kwargs):
    #     return kwargs
    #
    # def update(self, nearp=None, farp=None, nearf=None, farf=None, maxn=None, nth=None):
    #     self._tp_changed = True
    #     self._tp = self._args2dict(nearf=nearf, nearp=nearp, farf=farf, farp=farp)

    def update(self, **kwargs):
        if kwargs["simulation"]:
            self.simulation = True
            self.set_data(kwargs["ts_t"], kwargs["ts_x"])
        else:
            self._tp_changed = True
        self._tp = kwargs
        self.generate_time_params()
        self._event.set()
        print("update vege")


class DataProcessor:
    def __init__(self, figure: PlotWidget=None, predictor: EnsemblePredictor=None):
        """"""
        # declare attributes
        self.ts_t = self.ts_x = None
        self.predictor = predictor
        self.figure = figure

        self.simulation = False
        self.mini = 0
        self.maxi = 0
        self.t_begin = 0
        self.t_end = 0

        self.pl = None

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
            self.indices = np.arange(len(self.ts_t))
            self.maxi = len(self.ts_t)
            self.t_begin = self.ts_t[0]
            self.t_end = self.ts_t[len(self.ts_t)-1]

        if time_series:
            pass

        if self.predictor:
            self.predictor.set_data(self.ts_t, self.ts_x)

    def set_figure(self, figure: PlotWidget=None):
        self.figure = figure

        if self.predictor:
            self.predictor.set_figure(figure)

    def process(self, **kwargs):
        self._plot_observations()
        if self.predictor:
            self.predictor.start()
            # self.predictor.update(**kwargs)

    def update(self, **kwargs):
        if self.simulation:
            if self.predictor:
                self.predictor.update(simulation=True, ts_t=self.ts_t, ts_x=self.ts_x, **kwargs)
                self._plot_observations()
                return
        if self.predictor:
            self.predictor.update(**kwargs)

    def _plot_observations(self):
        self.figure.erase_line(ploth=self.pl)
        # self.figure.clear()
        # self.figure.draw()
        self.pl = self.figure.plot(self.ts_t[self.mini:self.maxi], self.ts_x[self.mini:self.maxi], 'b.-', markersize=6, label='observations')
        self.figure.set_axes_labels("time [year]", "stock price [Ft]")
        self.figure.set_axis_offset()
        self.figure.legend(loc='upper left')
        self.figure.draw()

    def interrupt(self):
        self.predictor.interrupt()

    def set_minmaxt(self, mint=None, maxt=None):
        if mint and maxt:
            self.simulation = False

            mint = date2year(mint)
            maxt = date2year(maxt)
            print("---------------------", mint)
            print("---------------------", maxt)
            print("---------------------", self.ts_t[0])
            if maxt < self.t_begin:
                return

            self.mini = int(np.interp(mint, self.ts_t, self.indices))
            self.maxi = int(np.interp(maxt, self.ts_t, self.indices))
            print("----------------------------", self.mini, self.maxi, len(self.ts_t))
            if self.maxi - self.mini > 10:
                self.simulation = True
        else:
            self.simulation = False
            self.mini = 0
            self.maxi = len(self.ts_t)
        return self.simulation

if __name__ == "__main__":
    np = NaivePredictor()
