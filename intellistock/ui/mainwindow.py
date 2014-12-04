
from PyQt4.QtGui import QMainWindow, QListWidgetItem, QLabel, \
    QIcon, QCloseEvent, QColor, QWidget
from PyQt4.QtCore import QSettings
from PyQt4.Qt import Qt
from .ui_mainwindow import Ui_MainWindow
from .navigatorplotwidget import NavigatorPlotWidget

# Polcz itt belenyult
# import logging
# FORMAT = '%(levelname)s Proc[%(process)s] at %(pathname)s:%(lineno)d - %(message)s'
# logging.basicConfig(format=FORMAT)
# plogger = logging.getLogger('polcz')


class FavSorter():
    def __init__(self, favs: list):
        self.favs = favs

    def __call__(self, a: str):
        if a in self.favs:
            return str(1)+a
        else:
            return a


class IconBank:
    star = None
    main = None

    @staticmethod
    def load_icons():
        IconBank.star = QIcon("resources/star.png")
        IconBank.main = QIcon("resources/main_icon.png")





class MainWindow(QMainWindow):
    def __init__(self, application):
        self.application = application        
        IconBank.load_icons()

        # Initialize from Designer created
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize extras (not automateable by Designer)
        self.setWindowIcon(IconBank.main)
        self.run_result = QLabel("Kész.")  # todo: ui memberbe
        self.ui.statusbar.addWidget(self.run_result)
        self.ui.tabWidget.tabCloseRequested.connect(self.kill_plotter)

        # Initialize members and settings
        self._settings = QSettings("IntelliStock", "IntelliStock")
        self._favorites = self._settings.value("favorites", ["OTP"])
        self._plotters = {}
        self._datas = None

    def initialize(self, initial_stocks: dict):
        self._datas = initial_stocks

        keys = list(self._datas.keys())
        keys.sort(key=FavSorter(self._favorites))

        for k in keys:
            wi = QListWidgetItem(k)
            if k in self._favorites:
                wi.setIcon(IconBank.star)
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
            item.setIcon(IconBank.star)

    def on_action_simulation_triggered(self, *b):
        if not b:
            return
        self.application.start_simulation()

    def on_lineEdit_search_textEdited(self, s: str):
        print("Text Edited: {}".format(s))
        # todo: lista szűrő.

    def on_listWidget_stocks_itemActivated(self, item: QListWidgetItem):
        if item.text() in self._plotters.keys():
            self.ui.tabWidget.setCurrentWidget(self._plotters[item.text()])
        else:
            self.create_plotter(item.text())
        # MINDENKINEK: Nem névszerinti kérést küld, hanem legyárt egy plottert, amit átad szerkesztésre.
        # Ezáltal elválasztjuk az adatot a GUI-tól.

    def on_listWidget_stocks_itemSelectionChanged(self):
        if self.ui.listWidget_stocks.selectedItems():
            self.ui.action_favorite.setEnabled(True)
            self.ui.action_simulation.setEnabled(True)
        else:
            self.ui.action_favorite.setEnabled(False)
            self.ui.action_simulation.setEnabled(False)

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

    def create_plotter(self, name: str):
        npw = NavigatorPlotWidget(self)
        self._plotters[name] = npw
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.addTab(npw, name))
        self.application.new_plotter(name, npw)

    def kill_plotter(self, index: int):
        name = self.ui.tabWidget.tabText(index)
        self.ui.tabWidget.removeTab(index)
        del self._plotters[name]
        self.application.kill_plotter(name)


    def closeEvent(self, event: QCloseEvent):
        settings = QSettings("IntelliStock", "IntelliStock")
        settings.setValue("favorites", self._favorites)
        event.accept()
