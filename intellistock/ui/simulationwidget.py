from PyQt4.QtGui import QWidget, QTableWidgetItem, QMenu, QAction
from PyQt4.QtCore import QObject, QDateTime, QPoint, QTimer
from PyQt4.Qt import Qt
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
        self.ui.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        
        # Initialize extras (not automateable by Designer)
        self.action_buy = QAction("Vétel", self)
        self.action_sell = QAction("Eladás", self)
        self.action_update = QAction("Frissítés", self)
        self.cmenu = QMenu(self)
        self.cmenu.addAction(self.action_buy)
        self.cmenu.addAction(self.action_sell)
        self.cmenu.addAction(self.action_update)
        self.update_timer = QTimer()
        # Initialize members and settings
        self.selected_stock_name = ""

    def on_button_start_pressed(self):
        self.ui.button_stop.setEnabled(True)
        self.ui.button_start.setEnabled(False)
        self.ui.dateTime_start.setEnabled(False)
        self.ui.spin_cash.setEnabled(False)
        self.ui.dial_transactFee.setEnabled(False)
        self.ui.dial_speed.setEnabled(False)
        self.update_timer.start(2000)

    def on_button_stop_pressed(self):
        self.ui.button_stop.setEnabled(False)
        self.ui.button_start.setEnabled(True)
        self.ui.dateTime_start.setEnabled(True)
        self.ui.spin_cash.setEnabled(True)
        self.ui.dial_transactFee.setEnabled(True)
        self.ui.dial_speed.setEnabled(True)
        self.update_timer.stop()

    def on_tableWidget_customContextMenuRequested(self, p: QPoint):
        rowi = self.ui.tableWidget.indexAt(p).row()
        if rowi < 0:
            return
        self.selected_stock_name = self.ui.tableWidget.item(rowi, 0).text()
        self.cmenu.popup(self.ui.tableWidget.viewport().mapToGlobal(p))

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
        self.ui.label_cash.setText(str(int(i))+" Ft")

    def set_stocks_value(self, i: int):
        self.ui.label_stocksValue.setText(str(int(i))+" Ft")

    def set_stocks(self, stocks: dict, get_stock_price: callable):
        self.ui.tableWidget.setRowCount(len(stocks.keys()))
        i = 0
        sum_of_stocks = 0
        for s, am in stocks.items():
            val = am*get_stock_price(s)
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(s))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(str(am)))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(str(val)))
            i += 1
            sum_of_stocks += val
        self.set_stocks_value(sum_of_stocks)