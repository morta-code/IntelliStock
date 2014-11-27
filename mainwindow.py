import sys
from PyQt4.QtGui import QMainWindow, QMenuBar, QToolBar, QSplitter, QWidget, QApplication, QListWidgetItem, QLabel, \
    QIcon, QCloseEvent
from PyQt4.QtCore import QSettings
from scipy.signal._arraytools import even_ext
from ui_mainwinow import Ui_MainWindow
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


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
        # QApplication as a member
        self.qApp = QApplication(sys.argv)

        # Initialize from Designer created
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize extras (not automateable by Designer)
        self.setWindowIcon(QIcon("main_icon.png"))
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
                wi.setIcon(QIcon("star.png"))
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
            item.setIcon(QIcon("star.png"))

    def on_lineEdit_search_textEdited(self, s: str):
        print("Text Edited: {}".format(s))

    def on_listWidget_stocks_itemDoubleClicked(self, item: QListWidgetItem):
        print("{} will be opened in a new tab/view.".format(item.text()))
        self._get_stock_datas_cb(item.text())

    def on_listWidget_stocks_itemClicked(self, item: QListWidgetItem):
        print("{} clicked.".format(item.text()))

    def on_listWidget_stocks_itemActivated(self, item: QListWidgetItem):
        print("{} activated.".format(item.text()))

    def on_listWidget_stocks_itemEntered(self, item: QListWidgetItem):
        print("{} Entered.".format(item.text()))

    def on_listWidget_stocks_itemPressed(self, item: QListWidgetItem):
        print("{} Pressed.".format(item.text()))

    def on_listWidget_stocks_itemSelectionChanged(self):
        print("{} SELECTED.".format(self.ui.listWidget_stocks.selectedItems()[0].text()))
        self.ui.action_favorite.setEnabled(True)

    def update_stocks(self, updated_stocks: dict):
        """Call it when new trades arrived.
        :param updated_stocks: is a names (str) keyed prize values.
        """
        pass

    def stock_values(self, name: str, datas):
        """Call it to show a time serie for the given stock.
        :param name: name of
        :param datas:
        :return:
        """
        pass

    def exec(self) -> int:
        return self.qApp.exec()

    def closeEvent(self, event: QCloseEvent):
        settings = QSettings("IntelliStock", "IntelliStock")
        settings.setValue("favorites", self._favorites)
        event.accept()

if __name__ == '__main__':
    w = MainWindow({"OTP": 3500, "MOL": 13400, "RICHTER": 3700, "DAX": 9950}, lambda n: print(n))
    w.show()
    w.exec()
