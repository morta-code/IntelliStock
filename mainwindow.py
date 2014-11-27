import sys
from PyQt4.QtGui import QMainWindow, QMenuBar, QToolBar, QSplitter, QWidget, QApplication, QListWidgetItem, QLabel, \
    QIcon
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
    def __init__(self, initial_stocks: dict):
        # QApplication as a member
        self.qApp = QApplication(sys.argv)

        # Initialize from Designer created
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize extras (not automateable by Designer)
        self.setWindowIcon(QIcon("main_icon.png"))
        self.ui.statusbar.addWidget(QLabel("Hello statusbar!"))

        # Initialize members
        self._datas = initial_stocks
        self._favorites = ["OTP"]

        keys = list(self._datas.keys())
        keys.sort(key=favsorter(self._favorites))

        for k in keys:
            wi = QListWidgetItem(k)
            if k in self._favorites:
                wi.setIcon(QIcon("star.png"))
            wi.setToolTip(str(self._datas[k]))
            self.ui.listWidget_stocks.addItem(wi)




    def on_lineEdit_search_textEdited(self, s: str):
        print("Text Edited: {}".format(s))

    def on_listWidget_stocks_itemDoubleClicked(self, item: QListWidgetItem):
        print("{} will be opened in a new tab/view.".format(item.text()))

    def on_listWidget_stocks_itemClicked(self, item: QListWidgetItem):
        print("{} clicked.".format(item.text()))

    def on_listWidget_stocks_itemActivated(self, item: QListWidgetItem):
        print("{} activated.".format(item.text()))

    def on_listWidget_stocks_itemEntered(self, item: QListWidgetItem):
        print("{} Entered.".format(item.text()))

    def on_listWidget_stocks_itemPressed(self, item: QListWidgetItem):
        print("{} Pressed.".format(item.text()))

    def update_stocks(self, updated_stocks: dict):
        """Must be called by main program if new datas arrived
        :param stocks: dict of last values by stock_names
        """

    def exec(self) -> int:
        return self.qApp.exec()

if __name__ == '__main__':
    w = MainWindow({"OTP": 3500, "MOL": 13400, "RICHTER": 3700, "DAX": 9950})
    w.show()
    w.exec()
