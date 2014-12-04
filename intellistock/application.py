import sys
import time
from simulation.simulation import Simulation

from ui import mainwindow
from PyQt4.QtGui import QApplication, QSplashScreen, QPixmap
from PyQt4.Qt import Qt
from datetime import datetime


class Application:
    def __init__(self):
        self.q_application = QApplication(sys.argv)
        self.window = mainwindow.MainWindow(self)

        self.window.initialize(
            {"OTP": 3500, "MOL": 13400, "RICHTER": 3700, "DAX": 9950, "RÁBA": 1100, "UPDATE1": 990, "ELMŰ": 13900})

    def load(self):
        splash = QSplashScreen(QPixmap("resources/main_icon.png"))
        splash.show()
        splash.showMessage("Loading modules", Qt.AlignBottom)
        time.sleep(1)
        splash.showMessage("Loading data", Qt.AlignBottom)
        time.sleep(2)
        splash.finish(self.window)

    def exec(self):
        self.window.show()
        self.q_application.exec()

    def request_stock_values(self):
        """ TODO: STUB """
        self.window.stock_values("OTP",
                                 [(datetime(2014, 11, 27, 9, 32), 12400, 2), (datetime(2014, 11, 27, 9, 35), 12350, 5)])

    def start_simulation(self):
        simulation = Simulation(self)
        simulation.start_simulation()

    def receive_simulation_result(self, simulation: Simulation, simulation_result):
        self.window.update_simulation_results(simulation_result)
        pass

if __name__ == '__main__':
    application = Application()
    application.load()
    application.exec()
    