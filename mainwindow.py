import sys
from PyQt4.QtGui import QMainWindow, QMenuBar, QToolBar, QSplitter, QWidget, QApplication, QListWidgetItem
from ui_mainwinow import Ui_MainWindow
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.listWidget_stocks.addItems(["MOL", "OTP", "Telekom".upper(), "Richter".upper(), "FHB",
                                            "Danubius".upper(),
                                            "Pannergy".upper(),
                                            "RÁBA", "TVK", "Appeninn".upper(), "4IG", "ALTERA", "BIF", "CSEPEL",
                                            "EHEP", "ELMÜ", "ÉMÁSZ", "ESTMÉDIA", "UPDATE1", "ZWACK", "KONZUM",
                                            "OPIMUS", "SYNERGON", "EXTERNET", "VISONKA", "FUTURAQUA"])

    def on_lineEdit_search_textEdited(self, s: str):
        print("Text Edited: {}".format(s))

    def on_listWidget_stocks_itemDoubleClicked(self, item: QListWidgetItem):
        print("{}".format(item.text()))

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
