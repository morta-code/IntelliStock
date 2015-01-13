import sys
from threading import Lock
import time
from intellistock.simulation.simulation import Simulation
from intellistock.ui import mainwindow
from intellistock.data import data
from PyQt4.QtGui import QApplication, QSplashScreen, QPixmap
from PyQt4.Qt import Qt
from datetime import datetime
from intellistock.predictor.predictor import PredictorTestSimulation, NaivePredictor, EnsemblePredictor, DataProcessor

from inspect import currentframe
from intellistock.predictor.pczdebug import pczdebug

class Application:
    def __init__(self):
        self.q_application = QApplication(sys.argv)
        self.window = mainwindow.MainWindow(self)
        self.window.initialize(dict(data.get_stocks_with_last_close()))
        self.predictor_cls = EnsemblePredictor
        # list of actually running data processors, which should be notified on every changes of the data stream
        self.data_processors = {}
        self.simulation = None
        self.lock = Lock()

    def load(self):
        # todo: az importok és a gui betöltés átszervezésésvel gyorsítható az indítás. Majd a végén.
        # splash = QSplashScreen(QPixmap("resources/main_icon.png"))
        # splash.show()
        # splash.showMessage("Loading modules", Qt.AlignBottom)
        #time.sleep(1)
        # splash.showMessage("Loading data", Qt.AlignBottom)
        # time.sleep(2)
        # splash.finish(self.window)
        pass

    def exec(self):
        self.window.show()
        self.q_application.exec()

    def halt(self):
        for name, dp in self.data_processors.items():
            dp.interrupt()
        if self.simulation:
            self.simulation.stop_simulation()

    def launch_data_processor(self, name: str, plotter, **kwargs):
        """Add new plotter (from the GUI) to the application.
        The given plotter is needed for the data manager and the predictors.

        :param name: is the Stock's name
        :param plotter: is an object to draw the datas. It must have the following methods:
            subplot()
            plot()
            plot_candles()
            draw()
        """
        processor = DataProcessor(predictor=self.predictor_cls())
        if name in self.data_processors:
            raise AssertionError()
        self.data_processors[name] = processor
        processor.set_data(raw_data=data.get_trades(20090104100000, 20150104110000, name))
        processor.set_figure(plotter)
        processor.process(**kwargs)

    def update_data_processor(self, name: str, **kwargs):
        """
        :param data
        :param farp=None
        :param nearp=None
        :param farf=None
        :param nearf=None
        :param maxn=None
        :param nth=None
        """
        if name not in self.data_processors:
            raise AssertionError()
        self.data_processors[name].update(**kwargs)

    def kill_plotter(self, name: str):
        """Destroys the managers and predictors to the given Stock
        :param name: the stock's name
        :return:
        """
        # todo: implement.
        pass

    def start_simulation(self, money: int, interest: float, speed: int, start: datetime):
        if self.simulation:
            self.simulation.stop_simulation()
        self.simulation = Simulation(self)
        self.simulation.set_money(money)
        self.simulation.set_interest(interest)
        self.simulation.set_speed(speed)
        self.simulation.set_start_time(start)
        self.simulation.start_simulation()

    def stop_simulation(self):
        if self.simulation:
            self.simulation.stop_simulation()

    def receive_simulation_result(self, simulation: Simulation, simulation_result):
        self.window.update_simulation_results(simulation_result)
        pass

    def set_my_stocks(self, stocks):
        #TODO
        pass

    def get_stock_price(self, stock_name, data_time=datetime.now()):
        #TODO
        pass

    def set_graph_times(self, begin, end):
        #TODO
        pass

application = None


def main():
    global application
    application = Application()
    application.load()
    application.exec()
    application.halt()

if __name__ == '__main__':
    main()
    exit(0)
