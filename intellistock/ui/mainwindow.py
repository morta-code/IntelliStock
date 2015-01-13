
from PyQt4.QtGui import QMainWindow, QListWidgetItem, QLabel, QIcon, QCloseEvent, QColor, QSystemTrayIcon, \
    QMessageBox, QWidget
from PyQt4.QtCore import QSettings
from PyQt4.Qt import Qt
from intellistock.ui.ui_mainwindow import Ui_MainWindow
from intellistock.ui.simulationwidget import SimulationWidget
from intellistock.ui.navigatorplotwidget import NavigatorPlotWidget

from intellistock.data import data

from inspect import currentframe
from intellistock.predictor.pczdebug import pczdebug

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
    exit = None

    @staticmethod
    def load_icons():
        IconBank.star = QIcon("resources/star.png")
        IconBank.main = QIcon("resources/main_icon.png")
        IconBank.exit = QIcon("resources/exit.png")


class MainWindow(QMainWindow):
    def __init__(self, application):
        self.application = application
        IconBank.load_icons()

        # Initialize from Designer created
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._sliders = ["near_future", "maxn", "near_past", "dt_samples", "dim"]
        self._default_pred_params = list(map(lambda x: 0, self._sliders))

        # Initialize extras (not automateable by Designer)
        self.setWindowIcon(IconBank.main)
        self.run_result = QLabel("Kész.")  # todo: ui memberbe
        self.ui.statusbar.addWidget(self.run_result)
        self.ui.tabWidget.tabCloseRequested.connect(self.kill_plotter)
        self.ui.action_favorite.setIcon(IconBank.star)
        self.ui.action_exit.setIcon(IconBank.exit)
        self.init_sliders()
        self.init_systray()
        self.init_simwidget()

        # Initialize members and settings
        self._settings = QSettings("IntelliStock", "IntelliStock")
        self._favorites = self._settings.value("favorites", ["OTP"])
        self._plotters = {}
        self._actual_plotter_name = None
        self._datas = None

    def init_sliders(self):
        for i in range(len(self._sliders)):
            slider = getattr(self.ui, "slider_" + self._sliders[i])
            spin = getattr(self.ui, "spin_" + self._sliders[i])
            spin.setValue(slider.value())
            spin.setRange(slider.minimum(), slider.maximum())
            self._default_pred_params[i] = slider.value()

    def init_systray(self):
        self.ui.systray = QSystemTrayIcon(IconBank.main)
        self.ui.systray.setToolTip("IntelliStock")
        self.ui.systray.show()

    def init_simwidget(self):
        self.ui.simwidget = SimulationWidget(self)
        sw = self.ui.simwidget
        sw.setVisible(False)
        self.ui.centralwidget.layout().addWidget(sw)
        sw.ui.button_start.pressed.connect(lambda : self.application.start_simulation(sw.ui.spin_cash.value(),
                                                (sw.ui.dial_transactFee.value())/100, sw.ui.dial_speed.value(),
                                                sw.start_datetime()))
        sw.ui.button_stop.pressed.connect(self.application.stop_simulation)
        sw.action_buy.triggered.connect(lambda: self.application.simulation.buy_stock(sw.selected_stock_name, 1))
        sw.action_sell.triggered.connect(lambda: self.application.simulation.sell_stock(sw.selected_stock_name, 1))
        sw.action_update.triggered.connect(lambda: self.application.simulation.update_stock_list())
        sw.update_timer.timeout.connect(lambda: self.application.simulation.update_stock_list())


    def initialize(self, initial_stocks: dict):
        """ Initialize datas only for opening window.
        It sorts by name for GUI and handles the favorite stocks, too.

        :param initial_stocks: dict of the most current values by stock names
        """
        self._datas = initial_stocks

        keys = list(self._datas.keys())
        keys.sort(key=FavSorter(self._favorites))

        for k in keys:
            wi = QListWidgetItem(k)
            if k in self._favorites:
                wi.setIcon(IconBank.star)
            wi.setToolTip(str(self._datas[k]))
            self.ui.listWidget_stocks.addItem(wi)

    def on_btn_default_params_pressed(self):
        for i in range(len(self._sliders)):
            getattr(self.ui, "slider_" + self._sliders[i]).setValue(self._default_pred_params[i])

    def collect_prediction_time_params(self):
        return {"nearp": self.ui.spin_near_past.value(),
                "nearf": self.ui.spin_near_future.value(),
                "maxn": self.ui.spin_maxn.value(),
                "dim": self.ui.spin_dim.value(),
                "dt": self.ui.spin_dt_samples.value(),
                "pl_gbr": self.ui.checkBox_gradBoosting.isChecked(),
                "pl_linear": self.ui.checkBox_expTendency.isChecked(),
                "pl_guass": self.ui.checkBox_multidimPred.isChecked()}

    def on_btn_update_all_pressed(self):
        """"""
        if self._actual_plotter_name:
            self.application.update_data_processor(self._actual_plotter_name,**self.collect_prediction_time_params())

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

    def on_action_simulation_toggled(self, b: bool):
        if b:
            self.ui.mainwidget.setVisible(False)
            self.ui.simwidget.setVisible(True)
            self.ui.centralwidget.layout().setStretch(1, 7)
            pass
        else:
            self.ui.mainwidget.setVisible(True)
            self.ui.simwidget.setVisible(False)
            self.ui.centralwidget.layout().setStretch(1, 7)
            pass

    def on_lineEdit_search_textEdited(self, s: str):
        if s:
            founds = self.ui.listWidget_stocks.findItems(s, Qt.MatchStartsWith)
            for item in self.ui.listWidget_stocks.findItems("", Qt.MatchStartsWith):
                if item in founds:
                    self.ui.listWidget_stocks.setItemHidden(item, False)
                else:
                    self.ui.listWidget_stocks.setItemHidden(item, True)
        else:
            for item in self.ui.listWidget_stocks.findItems("", Qt.MatchStartsWith):
                self.ui.listWidget_stocks.setItemHidden(item, False)

    def on_action_aboutStock_triggered(self):
        about = QMessageBox(self)
        about.setWindowTitle("Az IntelliStock-ról")
        about.setText("Ez nagyon király!")
        about.show()

    def on_listWidget_stocks_itemActivated(self, item: QListWidgetItem):
        if self.ui.simwidget.isVisible():
            self.application.simulation.buy_stock(item.text(), 1)
            return
        self._actual_plotter_name = item.text()
        if item.text() in self._plotters.keys():
            self.ui.tabWidget.setCurrentWidget(self._plotters[item.text()])
        else:
            self.create_plotter(item.text())
            # MINDENKINEK: Nem névszerinti kérést küld, hanem legyárt egy plottert, amit átad szerkesztésre.
            # Ezáltal elválasztjuk az adatot a GUI-tól.

    def on_listWidget_stocks_itemSelectionChanged(self):
        if self.ui.listWidget_stocks.selectedItems():
            self.ui.action_favorite.setEnabled(True)
        else:
            self.ui.action_favorite.setEnabled(False)

    def on_action_showPrediction_toggled(self, b: bool):
        self.ui.groupBox_time.setVisible(b)
        self.ui.groupBox_predChecks.setVisible(b)

    def on_action_prediction_toggled(self, b: bool):
        self.application.data_processors[self._actual_plotter_name].predictor.hide(
            plh=self.application.predictor_cls.PLH_ALL, hide=not b)

    def on_checkBox_expTendency_toggled(self, b: bool):
        if self._actual_plotter_name:
            self.application.data_processors[self._actual_plotter_name].predictor.hide(plh=self.application.predictor_cls.PLH_LINEAR, hide=not b)

    def on_checkBox_gradBoosting_toggled(self, b: bool):
        if self._actual_plotter_name:
            self.application.data_processors[self._actual_plotter_name].predictor.hide(plh=self.application.predictor_cls.PLH_GRAD_BOOSTING, hide=not b)

    def on_checkBox_multidimPred_toggled(self, b: bool):
        if self._actual_plotter_name:
            self.application.data_processors[self._actual_plotter_name].predictor.hide(plh=self.application.predictor_cls.PLH_GAUSSIAN, hide=not b)

    # def on_spinBox_eachNthSample_valueChanged(self, i: int):
    #     # DO NOT REMOVE THIS CONDITION! (Signal emitted also with i as a string)
    #     if type(i) is not int:
    #         return
    #     self._ploter_params[self._actual_plotter_name]["nth"] = i
    #     pass
    #
    # def on_spinBox_maxNrSamples_valueChanged(self, i: int):
    #     # DO NOT REMOVE THIS CONDITION! (Signal emitted also with i as a string)
    #     if type(i) is not int:
    #         return
    #     self._ploter_params[self._actual_plotter_name]["maxn"] = i
    #     pass

    def update_stocks(self, updated_stocks: dict):
        """Call it when new trades arrived.
        :param updated_stocks: is a names (str) keyed prize values.
        """
        for k, v in updated_stocks.items():
            it = self.ui.listWidget_stocks.findItems(k, Qt.MatchExactly)[0]
            if int(it.toolTip()) < v:
                it.setBackgroundColor(QColor(0, 255, 0))
                it.setToolTip(str(v))
                if k in self._favorites:
                    self.ui.systray.showMessage(k, str(v))
            elif int(it.toolTip()) > v:
                it.setBackgroundColor(QColor(210, 0, 0))
                it.setToolTip(str(v))
                if k in self._favorites:
                    self.ui.systray.showMessage(k, str(v))
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
        self.application.launch_data_processor(name, npw, **self.collect_prediction_time_params())

    def kill_plotter(self, index: int):
        name = self.ui.tabWidget.tabText(index)
        self.ui.tabWidget.removeTab(index)
        del self._plotters[name]
        self.application.kill_plotter(name)

    def closeEvent(self, event: QCloseEvent):
        settings = QSettings("IntelliStock", "IntelliStock")
        settings.setValue("favorites", self._favorites)
        event.accept()
