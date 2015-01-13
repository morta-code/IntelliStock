from PyQt4.QtGui import QWidget, QTableWidgetItem
from PyQt4.QtCore import QObject, QDateTime
from intellistock.ui.ui_simulation import Ui_SimulationForm
from datetime import datetime

class SimulationWidget(QWidget):
    def __init__(self, parent: QObject=None):
        super(QWidget, self).__init__(parent)
        # Initialize from Designer created
        self.ui = Ui_SimulationForm()
        self.ui.setupUi(self)
        self.ui.label_trFee.setText(str(self.ui.dial_transactFee.value()/10)+" %")
        self.ui.label_simSpeed.setText(str(self.ui.dial_speed.value()))
        # Initialize extras (not automateable by Designer)
        # Initialize members and settings

    def on_button_start_pressed(self):
        self.ui.button_stop.setEnabled(True)
        self.ui.button_start.setEnabled(False)
        self.ui.dateTime_start.setEnabled(False)
        self.ui.spin_cash.setEnabled(False)
        self.ui.dial_transactFee.setEnabled(False)
        self.ui.dial_speed.setEnabled(False)

    def on_button_stop_pressed(self):
        self.ui.button_stop.setEnabled(False)
        self.ui.button_start.setEnabled(True)
        self.ui.dateTime_start.setEnabled(True)
        self.ui.spin_cash.setEnabled(True)
        self.ui.dial_transactFee.setEnabled(True)
        self.ui.dial_speed.setEnabled(True)

    def on_spin_cash_valueChanged(self, v: int):
        pass

    def on_dateTime_start_dateTimeChanged(self, v: QDateTime):
        pass

    def on_dial_transactFee_valueChanged(self, v: int):
        self.ui.label_trFee.setText(str(v/10)+" %")

    def on_dial_speed_valueChanged(self, v: int):
        self.ui.label_simSpeed.setText(str(v))

    def start_datetime(self) -> datetime:
        qdt = self.ui.dateTime_start.dateTime()
        return datetime(qdt.date().year(),qdt.date().month(),qdt.date().day(),qdt.time().hour(),qdt.time().minute())

    def set_cash(self, i: int):
        self.ui.label_cash.setText(str(i))

    def set_stocks_value(self, i: int):
        self.ui.label_stocksValue.setText(str(i))

    def set_stocks(self, stocks: dict):
        pass
