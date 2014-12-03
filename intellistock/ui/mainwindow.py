import sys
from PyQt4.QtGui import QMainWindow, QApplication, QListWidgetItem, QLabel, \
    QIcon, QCloseEvent, QColor, QSplashScreen, QPixmap
from PyQt4.QtCore import QSettings
from PyQt4.Qt import Qt
from ui_mainwindow import Ui_MainWindow
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import time
from datetime import datetime

class favsorter():
    def __init__(self, favs: list):
        self.favs = favs

    def __call__(self, a: str):
        if a in self.favs:
            return str(1)+a
        else:
            return a


class MainWindow(QMainWindow):
    def __init__(self, initial_stocks: dict, get_stock_datas_cb: callable):
        # Initialize from Designer created
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize extras (not automateable by Designer)
        self.setWindowIcon(QIcon("resources/main_icon.png"))
        self.ui.statusbar.addWidget(QLabel("Hello statusbar!"))
        self.ui.statusbar.addWidget(QLabel("Szia Állapotsor!"))

        # Initialize members and settings
        self._datas = initial_stocks
        self._settings = QSettings("IntelliStock", "IntelliStock")
        self._favorites = self._settings.value("favorites", ["OTP"])
        self._get_stock_datas_cb = get_stock_datas_cb


        keys = list(self._datas.keys())
        keys.sort(key=favsorter(self._favorites))

        for k in keys:
            wi = QListWidgetItem(k)
            if k in self._favorites:
                wi.setIcon(QIcon("resources/star.png"))
            wi.setToolTip(str(self._datas[k]))
            self.ui.listWidget_stocks.addItem(wi)

    def on_action_favorite_triggered(self, *b):
        if not b:
            return
        item = self.ui.listWidget_stocks.selectedItems()[0]
        if item.text() in self._favorites:
            self._favorites.remove(item.text())
            item.setIcon(QIcon())
        else:
            self._favorites.append(item.text())
            item.setIcon(QIcon("resources/star.png"))

    def on_lineEdit_search_textEdited(self, s: str):
        print("Text Edited: {}".format(s))
        self.update_stocks({"OTP": 5000})
        pass

    def on_listWidget_stocks_itemActivated(self, item: QListWidgetItem):
        self._get_stock_datas_cb(item.text())

    def on_listWidget_stocks_itemSelectionChanged(self):
        if self.ui.listWidget_stocks.selectedItems():
            self.ui.action_favorite.setEnabled(True)
        else:
            self.ui.action_favorite.setEnabled(False)

    def update_stocks(self, updated_stocks: dict):
        """Call it when new trades arrived.
        :param updated_stocks: is a names (str) keyed prize values.
        """
        for k, v in updated_stocks.items():
            it = self.ui.listWidget_stocks.findItems(k, Qt.MatchExactly)[0]
            if int(it.toolTip()) < v:
                it.setBackgroundColor(QColor(0, 255, 0))
                it.setToolTip(str(v))
            elif int(it.toolTip()) > v:
                it.setBackgroundColor(QColor(210, 0, 0))
                it.setToolTip(str(v))
            else:
                it.setBackgroundColor(QColor(255, 255, 255))
        # TODO: multi level coloring and represent datas divided from the widget

    def stock_values(self, name: str, datas):
        """Call it to show a time serie for the given stock.
        :param name: name of
        :param datas:
        :return:
        """
        print(name)
        # TODO: implement
        pass

    def closeEvent(self, event: QCloseEvent):
        settings = QSettings("IntelliStock", "IntelliStock")
        settings.setValue("favorites", self._favorites)
        event.accept()


if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap("resources/main_icon.png"))
    splash.show()
    splash.showMessage("Loading modules", Qt.AlignBottom)
    time.sleep(1)
    splash.showMessage("Loading data", Qt.AlignBottom)
    time.sleep(2)
    w = MainWindow({"OTP": 3500, "MOL": 13400, "RICHTER": 3700, "DAX": 9950, "RÁBA": 1100, "UPDATE1": 990,
                    "ELMŰ": 13900},
                   lambda n: w.stock_values(n, [(datetime(2014, 11, 27, 9, 32), 12400, 2), (datetime(2014, 11, 27, 9,
                                                                                                  35), 12350, 5)]))
    w.show()
    splash.finish(w)
    qApp.exec()
