# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwindow.ui'
#
# Created: Mon Jan 12 23:39:33 2015
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(734, 534)
        MainWindow.setWindowTitle(_fromUtf8("Stock"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.navigationLayout = QtGui.QVBoxLayout()
        self.navigationLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.navigationLayout.setObjectName(_fromUtf8("navigationLayout"))
        self.lineEdit_search = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_search.sizePolicy().hasHeightForWidth())
        self.lineEdit_search.setSizePolicy(sizePolicy)
        self.lineEdit_search.setMinimumSize(QtCore.QSize(120, 0))
        self.lineEdit_search.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit_search.setObjectName(_fromUtf8("lineEdit_search"))
        self.navigationLayout.addWidget(self.lineEdit_search)
        self.listWidget_stocks = QtGui.QListWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_stocks.sizePolicy().hasHeightForWidth())
        self.listWidget_stocks.setSizePolicy(sizePolicy)
        self.listWidget_stocks.setMinimumSize(QtCore.QSize(120, 0))
        self.listWidget_stocks.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listWidget_stocks.setObjectName(_fromUtf8("listWidget_stocks"))
        self.navigationLayout.addWidget(self.listWidget_stocks)
        self.progressBar_load = QtGui.QProgressBar(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar_load.sizePolicy().hasHeightForWidth())
        self.progressBar_load.setSizePolicy(sizePolicy)
        self.progressBar_load.setMinimumSize(QtCore.QSize(120, 0))
        self.progressBar_load.setMaximumSize(QtCore.QSize(200, 16777215))
        self.progressBar_load.setVisible(False)
        self.progressBar_load.setTextVisible(False)
        self.progressBar_load.setObjectName(_fromUtf8("progressBar_load"))
        self.navigationLayout.addWidget(self.progressBar_load)
        self.horizontalLayout.addLayout(self.navigationLayout)
        self.mainwidget = QtGui.QWidget(self.centralwidget)
        self.mainwidget.setObjectName(_fromUtf8("mainwidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.mainwidget)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.contentLayout = QtGui.QVBoxLayout()
        self.contentLayout.setObjectName(_fromUtf8("contentLayout"))
        self.tabWidget = QtGui.QTabWidget(self.mainwidget)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.contentLayout.addWidget(self.tabWidget)
        self.horizontalLayout_predictionOptions = QtGui.QHBoxLayout()
        self.horizontalLayout_predictionOptions.setObjectName(_fromUtf8("horizontalLayout_predictionOptions"))
        self.groupBox_predChecks = QtGui.QGroupBox(self.mainwidget)
        self.groupBox_predChecks.setObjectName(_fromUtf8("groupBox_predChecks"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_predChecks)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox_expTendency = QtGui.QCheckBox(self.groupBox_predChecks)
        self.checkBox_expTendency.setObjectName(_fromUtf8("checkBox_expTendency"))
        self.verticalLayout.addWidget(self.checkBox_expTendency)
        self.checkBox_multidimPred = QtGui.QCheckBox(self.groupBox_predChecks)
        self.checkBox_multidimPred.setObjectName(_fromUtf8("checkBox_multidimPred"))
        self.verticalLayout.addWidget(self.checkBox_multidimPred)
        self.checkBox_gradBoosting = QtGui.QCheckBox(self.groupBox_predChecks)
        self.checkBox_gradBoosting.setObjectName(_fromUtf8("checkBox_gradBoosting"))
        self.verticalLayout.addWidget(self.checkBox_gradBoosting)
        self.horizontalLayout_predictionOptions.addWidget(self.groupBox_predChecks)
        self.groupBox_time = QtGui.QGroupBox(self.mainwidget)
        self.groupBox_time.setObjectName(_fromUtf8("groupBox_time"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_time)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_near_future = QtGui.QLabel(self.groupBox_time)
        self.label_near_future.setObjectName(_fromUtf8("label_near_future"))
        self.gridLayout.addWidget(self.label_near_future, 1, 0, 1, 1)
        self.spin_near_past = QtGui.QSpinBox(self.groupBox_time)
        self.spin_near_past.setObjectName(_fromUtf8("spin_near_past"))
        self.gridLayout.addWidget(self.spin_near_past, 0, 2, 1, 1)
        self.spin_near_future = QtGui.QSpinBox(self.groupBox_time)
        self.spin_near_future.setObjectName(_fromUtf8("spin_near_future"))
        self.gridLayout.addWidget(self.spin_near_future, 1, 2, 1, 1)
        self.slider_near_future = QtGui.QSlider(self.groupBox_time)
        self.slider_near_future.setMinimum(0)
        self.slider_near_future.setMaximum(24)
        self.slider_near_future.setProperty("value", 3)
        self.slider_near_future.setOrientation(QtCore.Qt.Horizontal)
        self.slider_near_future.setTickPosition(QtGui.QSlider.TicksBelow)
        self.slider_near_future.setTickInterval(3)
        self.slider_near_future.setObjectName(_fromUtf8("slider_near_future"))
        self.gridLayout.addWidget(self.slider_near_future, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_time)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_near_past = QtGui.QLabel(self.groupBox_time)
        self.label_near_past.setObjectName(_fromUtf8("label_near_past"))
        self.gridLayout.addWidget(self.label_near_past, 0, 0, 1, 1)
        self.slider_near_past = QtGui.QSlider(self.groupBox_time)
        self.slider_near_past.setMinimum(0)
        self.slider_near_past.setMaximum(48)
        self.slider_near_past.setSingleStep(1)
        self.slider_near_past.setProperty("value", 2)
        self.slider_near_past.setOrientation(QtCore.Qt.Horizontal)
        self.slider_near_past.setTickPosition(QtGui.QSlider.TicksBelow)
        self.slider_near_past.setTickInterval(3)
        self.slider_near_past.setObjectName(_fromUtf8("slider_near_past"))
        self.gridLayout.addWidget(self.slider_near_past, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_default_params = QtGui.QPushButton(self.groupBox_time)
        self.btn_default_params.setDefault(False)
        self.btn_default_params.setFlat(False)
        self.btn_default_params.setObjectName(_fromUtf8("btn_default_params"))
        self.horizontalLayout_2.addWidget(self.btn_default_params)
        self.btn_update_all = QtGui.QPushButton(self.groupBox_time)
        self.btn_update_all.setEnabled(True)
        self.btn_update_all.setMouseTracking(False)
        self.btn_update_all.setObjectName(_fromUtf8("btn_update_all"))
        self.horizontalLayout_2.addWidget(self.btn_update_all)
        self.gridLayout.addLayout(self.horizontalLayout_2, 10, 0, 1, 3)
        self.slider_dt_samples = QtGui.QSlider(self.groupBox_time)
        self.slider_dt_samples.setMinimum(10)
        self.slider_dt_samples.setMaximum(1000)
        self.slider_dt_samples.setOrientation(QtCore.Qt.Horizontal)
        self.slider_dt_samples.setTickPosition(QtGui.QSlider.TicksBelow)
        self.slider_dt_samples.setTickInterval(100)
        self.slider_dt_samples.setObjectName(_fromUtf8("slider_dt_samples"))
        self.gridLayout.addWidget(self.slider_dt_samples, 3, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox_time)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.spin_dim = QtGui.QSpinBox(self.groupBox_time)
        self.spin_dim.setMinimum(4)
        self.spin_dim.setMaximum(16)
        self.spin_dim.setProperty("value", 6)
        self.spin_dim.setObjectName(_fromUtf8("spin_dim"))
        self.gridLayout.addWidget(self.spin_dim, 4, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox_time)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.spin_maxn = QtGui.QSpinBox(self.groupBox_time)
        self.spin_maxn.setMinimum(20)
        self.spin_maxn.setMaximum(10000)
        self.spin_maxn.setProperty("value", 20)
        self.spin_maxn.setObjectName(_fromUtf8("spin_maxn"))
        self.gridLayout.addWidget(self.spin_maxn, 2, 2, 1, 1)
        self.slider_maxn = QtGui.QSlider(self.groupBox_time)
        self.slider_maxn.setMinimum(20)
        self.slider_maxn.setMaximum(1000)
        self.slider_maxn.setOrientation(QtCore.Qt.Horizontal)
        self.slider_maxn.setTickPosition(QtGui.QSlider.TicksBelow)
        self.slider_maxn.setTickInterval(40)
        self.slider_maxn.setObjectName(_fromUtf8("slider_maxn"))
        self.gridLayout.addWidget(self.slider_maxn, 2, 1, 1, 1)
        self.slider_dim = QtGui.QSlider(self.groupBox_time)
        self.slider_dim.setOrientation(QtCore.Qt.Horizontal)
        self.slider_dim.setObjectName(_fromUtf8("slider_dim"))
        self.gridLayout.addWidget(self.slider_dim, 4, 1, 1, 1)
        self.spin_dt_samples = QtGui.QSpinBox(self.groupBox_time)
        self.spin_dt_samples.setObjectName(_fromUtf8("spin_dt_samples"))
        self.gridLayout.addWidget(self.spin_dt_samples, 3, 2, 1, 1)
        self.horizontalLayout_predictionOptions.addWidget(self.groupBox_time)
        self.contentLayout.addLayout(self.horizontalLayout_predictionOptions)
        self.horizontalLayout_3.addLayout(self.contentLayout)
        self.horizontalLayout.addWidget(self.mainwidget)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1008, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuStock = QtGui.QMenu(self.menubar)
        self.menuStock.setObjectName(_fromUtf8("menuStock"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_aboutStock = QtGui.QAction(MainWindow)
        self.action_aboutStock.setObjectName(_fromUtf8("action_aboutStock"))
        self.action_showToolbar = QtGui.QAction(MainWindow)
        self.action_showToolbar.setCheckable(True)
        self.action_showToolbar.setChecked(True)
        self.action_showToolbar.setObjectName(_fromUtf8("action_showToolbar"))
        self.action_showStatusbar = QtGui.QAction(MainWindow)
        self.action_showStatusbar.setCheckable(True)
        self.action_showStatusbar.setChecked(True)
        self.action_showStatusbar.setObjectName(_fromUtf8("action_showStatusbar"))
        self.action_fullscreen = QtGui.QAction(MainWindow)
        self.action_fullscreen.setObjectName(_fromUtf8("action_fullscreen"))
        self.action_exit = QtGui.QAction(MainWindow)
        self.action_exit.setObjectName(_fromUtf8("action_exit"))
        self.action_menubar = QtGui.QAction(MainWindow)
        self.action_menubar.setCheckable(True)
        self.action_menubar.setChecked(True)
        self.action_menubar.setObjectName(_fromUtf8("action_menubar"))
        self.action_favorite = QtGui.QAction(MainWindow)
        self.action_favorite.setEnabled(False)
        self.action_favorite.setObjectName(_fromUtf8("action_favorite"))
        self.action_simulation = QtGui.QAction(MainWindow)
        self.action_simulation.setCheckable(True)
        self.action_simulation.setObjectName(_fromUtf8("action_simulation"))
        self.action_showPrediction = QtGui.QAction(MainWindow)
        self.action_showPrediction.setCheckable(True)
        self.action_showPrediction.setChecked(True)
        self.action_showPrediction.setObjectName(_fromUtf8("action_showPrediction"))
        self.action_prediction = QtGui.QAction(MainWindow)
        self.action_prediction.setCheckable(True)
        self.action_prediction.setObjectName(_fromUtf8("action_prediction"))
        self.menuStock.addAction(self.action_simulation)
        self.menuStock.addAction(self.action_exit)
        self.menuView.addAction(self.action_showToolbar)
        self.menuView.addAction(self.action_showStatusbar)
        self.menuView.addAction(self.action_fullscreen)
        self.menuView.addAction(self.action_showPrediction)
        self.menuTools.addAction(self.action_favorite)
        self.menuTools.addAction(self.action_prediction)
        self.menuHelp.addAction(self.action_aboutStock)
        self.menubar.addAction(self.menuStock.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QObject.connect(self.action_showStatusbar, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.statusbar.setVisible)
        QtCore.QObject.connect(self.action_showToolbar, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.toolBar.setVisible)
        QtCore.QObject.connect(self.action_exit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.slider_near_past, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), self.spin_near_past.setValue)
        QtCore.QObject.connect(self.spin_near_past, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.slider_near_past.setValue)
        QtCore.QObject.connect(self.slider_near_future, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), self.spin_near_future.setValue)
        QtCore.QObject.connect(self.spin_near_future, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.slider_near_future.setValue)
        QtCore.QObject.connect(self.slider_near_past, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spin_near_past.setValue)
        QtCore.QObject.connect(self.slider_near_future, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spin_near_future.setValue)
        QtCore.QObject.connect(self.slider_maxn, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spin_maxn.setValue)
        QtCore.QObject.connect(self.spin_maxn, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.slider_maxn.setValue)
        QtCore.QObject.connect(self.slider_dt_samples, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spin_dt_samples.setValue)
        QtCore.QObject.connect(self.spin_dt_samples, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.slider_dt_samples.setValue)
        QtCore.QObject.connect(self.slider_dim, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spin_dim.setValue)
        QtCore.QObject.connect(self.spin_dim, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.slider_dim.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.lineEdit_search.setPlaceholderText(_translate("MainWindow", "gyorskeresés", None))
        self.groupBox_predChecks.setTitle(_translate("MainWindow", "Predikciók", None))
        self.checkBox_expTendency.setText(_translate("MainWindow", "Expected Tendency", None))
        self.checkBox_multidimPred.setText(_translate("MainWindow", "Gaussian Prediction", None))
        self.checkBox_gradBoosting.setText(_translate("MainWindow", "Gradient Boosting", None))
        self.groupBox_time.setTitle(_translate("MainWindow", "Linear and Multidimensional Prediction", None))
        self.label_near_future.setText(_translate("MainWindow", "Predikálandó közeljövő [óra]", None))
        self.label_2.setText(_translate("MainWindow", "Time between samples [sec]", None))
        self.label_near_past.setText(_translate("MainWindow", "Predikciós közelmúlt [óra]", None))
        self.btn_default_params.setText(_translate("MainWindow", "Alapértelmezett", None))
        self.btn_update_all.setText(_translate("MainWindow", "Frissítés", None))
        self.label.setText(_translate("MainWindow", "Max nr. of samples", None))
        self.label_4.setText(_translate("MainWindow", "Dimension", None))
        self.menuStock.setTitle(_translate("MainWindow", "&Stock", None))
        self.menuView.setTitle(_translate("MainWindow", "&Nézet", None))
        self.menuTools.setTitle(_translate("MainWindow", "&Eszközök", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Súg&ó", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Eszköztár", None))
        self.action_aboutStock.setText(_translate("MainWindow", "A &Stock névjegye", None))
        self.action_showToolbar.setText(_translate("MainWindow", "&Eszköztár", None))
        self.action_showToolbar.setStatusTip(_translate("MainWindow", "Eszköztár megjelenítése/eltejtése.", None))
        self.action_showToolbar.setShortcut(_translate("MainWindow", "Ctrl+E, T", None))
        self.action_showStatusbar.setText(_translate("MainWindow", "&Állapotsor", None))
        self.action_showStatusbar.setStatusTip(_translate("MainWindow", "Állapotsáv megjelenítése/elrejtése.", None))
        self.action_showStatusbar.setShortcut(_translate("MainWindow", "Ctrl+E, S", None))
        self.action_fullscreen.setText(_translate("MainWindow", "&Teljes képernyő", None))
        self.action_fullscreen.setStatusTip(_translate("MainWindow", "Ablak teljes képernyőre váltása.", None))
        self.action_fullscreen.setShortcut(_translate("MainWindow", "F11", None))
        self.action_exit.setText(_translate("MainWindow", "&Kilépés", None))
        self.action_exit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.action_menubar.setText(_translate("MainWindow", "Menüsor", None))
        self.action_menubar.setShortcut(_translate("MainWindow", "Ctrl+E, M", None))
        self.action_favorite.setText(_translate("MainWindow", "&Kedvenc", None))
        self.action_favorite.setStatusTip(_translate("MainWindow", "Kijelölt részvény hozzáadása/eltávolitása a kedvencek közül.", None))
        self.action_favorite.setShortcut(_translate("MainWindow", "Ctrl+F", None))
        self.action_simulation.setText(_translate("MainWindow", "Szimuláció", None))
        self.action_showPrediction.setText(_translate("MainWindow", "&Predikciós eszközök", None))
        self.action_showPrediction.setStatusTip(_translate("MainWindow", "Predikciós beállítások megjelenítése/elrejtése", None))
        self.action_showPrediction.setShortcut(_translate("MainWindow", "Ctrl+P", None))
        self.action_prediction.setText(_translate("MainWindow", "Predikció", None))

