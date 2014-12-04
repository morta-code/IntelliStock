
from PyQt4.QtGui import QMainWindow, QListWidgetItem, QLabel, \
    QIcon, QCloseEvent, QColor
from PyQt4.QtCore import QSettings
from PyQt4.Qt import Qt
from .ui_mainwindow import Ui_MainWindow
from .navigatorplotwidget import NavigatorPlotWidget

# Polcz itt belenyult
# from .navigatorplotwidget import NavigatorPlotWidget
# import logging
# FORMAT = '%(levelname)s Proc[%(process)s] at %(pathname)s:%(lineno)d - %(message)s'
# logging.basicConfig(format=FORMAT)
# plogger = logging.getLogger('polcz')


class favsorter():
    def __init__(self, favs: list):
        self.favs = favs

    def __call__(self, a: str):
        if a in self.favs:
            return str(1)+a
        else:
            return a


class MainWindow(QMainWindow):
    def __init__(self, application):
        self.application = application        
        
        # Initialize from Designer created
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize extras (not automateable by Designer)
        self.setWindowIcon(QIcon("resources/main_icon.png"))
        self.run_result = QLabel("Kész.")  # todo: ui memberbe
        self.ui.statusbar.addWidget(self.run_result)

        # Initialize members and settings
        self._settings = QSettings("IntelliStock", "IntelliStock")
        self._favorites = self._settings.value("favorites", ["OTP"])
        self._plotters = {}
        self._datas = None

    def initialize(self, initial_stocks: dict):
        self._datas = initial_stocks

        keys = list(self._datas.keys())
        keys.sort(key=favsorter(self._favorites))

        for k in keys:
            wi = QListWidgetItem(k)
            if k in self._favorites:
                wi.setIcon(QIcon("resources/star.png"))
            wi.setToolTip(str(self._datas[k]))
            self.ui.listWidget_stocks.addItem(wi)

    # Polcz itt megint belepofazott, a fene vigye el
    # def setupPlotWidget(self):
    #     self.ui.plotWidget = NavigatorPlotWidget(cols = 2, rows = 1)
    #     self.ui.tabWidget.addTab(self.ui.plotWidget, "Polcz plot")
    #     self.ui.tabWidget.setCurrentIndex(0)

    def on_action_favorite_triggered(self, *b):
        if not b:
            return
        item = self.ui.listWidget_stocks.selectedItems()[0]
        if item.text() in self._favorites:
            self._favorites.remove(item.text())
            item.setIcon(QIcon())
        else:
            self._favorites.append(item.text())
            item.setIcon(QIcon("../resources/star.png"))

    def on_action_simulation_triggered(self, *b):
        if not b:
            return
        self.application.start_simulation()

    def on_lineEdit_search_textEdited(self, s: str):
        print("Text Edited: {}".format(s))
        # self.update_stocks({"OTP": 5000})
        # todo: lista szűrő.

    def on_listWidget_stocks_itemActivated(self, item: QListWidgetItem):
        # todo: ezt sort törölni:
        self.application.request_stock_values(item.text())

        if item.text() in self._plotters.keys():
            self.ui.tabWidget.setCurrentWidget(self._plotters[item.text()])
        else:
            npw = NavigatorPlotWidget(self)
            self._plotters[item.text()] = npw
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.addTab(npw, item.text()))

        # todo: MINDENKINEK: Nem névszerinti kérést küld, hanem legyárt egy plottert, amit átad szerkesztésre.
        # Ezáltal elválasztjuk az adatot a GUI-tól.

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

    def update_simulation_results(self, updated_simulation_results: dict):
        self.run_result.setText("Szimuláció kész.")
        pass

    def stock_values(self, name: str, datas):
        """Call it to show a time serie for the given stock.
        :param name: name of
        :param datas:
        :return:
        """
        print(name)
        # TODO: implement
        # Ha nincs megnyitva, nyit egy lapot, ha meg van nyitva, azt frissíti.
        pass

    def create_plotter(self, name: str):
        # todo: build a plotter widget
        pass

    def closeEvent(self, event: QCloseEvent):
        settings = QSettings("IntelliStock", "IntelliStock")
        settings.setValue("favorites", self._favorites)
        event.accept()
