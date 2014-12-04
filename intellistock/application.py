import sys
import time
from intellistock.simulation.simulation import Simulation
from intellistock.ui import mainwindow
from intellistock.data import data
from PyQt4.QtGui import QApplication, QSplashScreen, QPixmap
from PyQt4.Qt import Qt
from datetime import datetime
from intellistock.predictor.predictor import PredictorTestSimulation, NaivePredictor


class Application:
    def __init__(self):
        self.q_application = QApplication(sys.argv)
        self.window = mainwindow.MainWindow(self)
        self.window.initialize(dict(data.get_stocks_with_last_close()))

    def load(self):
        splash = QSplashScreen(QPixmap("resources/main_icon.png"))
        splash.show()
        splash.showMessage("Loading modules", Qt.AlignBottom)
        #time.sleep(1)
        splash.showMessage("Loading data", Qt.AlignBottom)
        #time.sleep(2)
        splash.finish(self.window)

    def exec(self):
        self.window.show()
        self.q_application.exec()

    def request_stock_values(self, name: str):
        """ TODO: STUB """
        self.window.stock_values("OTP",
                                 [(datetime(2014, 11, 27, 9, 32), 12400, 2), (datetime(2014, 11, 27, 9, 35), 12350, 5)])

    def new_plotter(self, name: str, plotter):
        """Add new plotter (from the GUI) to the application.
        The given plotter is needed for the data manager and the predictors.

        :param name: is the Stock's name
        :param plotter: is an object to draw the datas. It must have the following methods:
            subplot()
            plot()
            plot_candles()
            draw()
        """

        simulation = PredictorTestSimulation(application)
        simulation.setFigure(plotter)
        simulation.start_simulation()

        pass

    def kill_plotter(self, name: str):
        """Destroys the managers and predictors to the given Stock
        :param name: the stock's name
        :return:
        """
        # todo: implement.
        pass

    def start_simulation(self, name: str):
        simulation = Simulation(self)
        simulation.start_simulation()

    def receive_simulation_result(self, simulation: Simulation, simulation_result):
        self.window.update_simulation_results(simulation_result)
        pass

application = None

def main():
    global application
    application = Application()
    application.load()
    application.exec()

if __name__ == '__main__':
    main()
    
