from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QObject, QDateTime
from intellistock.ui.ui_simulation import Ui_SimulationForm

class SimulationWidget(QWidget):
    def __init__(self, parent: QObject=None):
        super(QWidget, self).__init__(parent)
        # Initialize from Designer created
        self.ui = Ui_SimulationForm()
        self.ui.setupUi(self)
        # Initialize extras (not automateable by Designer)
        # Initialize members and settings

    def on_button_start_pressed(self):
        print(2)

    def on_button_stop_pressed(self):
        print(2)

    def on_spin_cash_valueChanged(self, v: int):
        print(v)

    def on_dateTime_start_dateTimeChanged(self, v: QDateTime):
        print(v)

    def on_dial_transactFee_valueChanged(self, v: int):
        print(v)

    def on_dial_speed_valueChanged(self, v: int):
        print(v)