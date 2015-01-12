# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_simulation.ui'
#
# Created: Mon Jan 12 23:35:23 2015
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

class Ui_SimulationForm(object):
    def setupUi(self, SimulationForm):
        SimulationForm.setObjectName(_fromUtf8("SimulationForm"))
        SimulationForm.resize(614, 476)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SimulationForm)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dateTime_start = QtGui.QDateTimeEdit(SimulationForm)
        self.dateTime_start.setObjectName(_fromUtf8("dateTime_start"))
        self.gridLayout.addWidget(self.dateTime_start, 1, 0, 1, 1)
        self.label = QtGui.QLabel(SimulationForm)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(SimulationForm)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.spin_cash = QtGui.QSpinBox(SimulationForm)
        self.spin_cash.setMaximum(1000000)
        self.spin_cash.setProperty("value", 10000)
        self.spin_cash.setObjectName(_fromUtf8("spin_cash"))
        self.gridLayout.addWidget(self.spin_cash, 1, 1, 1, 1)
        self.button_start = QtGui.QPushButton(SimulationForm)
        self.button_start.setObjectName(_fromUtf8("button_start"))
        self.gridLayout.addWidget(self.button_start, 1, 2, 1, 1)
        self.button_stop = QtGui.QPushButton(SimulationForm)
        self.button_stop.setEnabled(False)
        self.button_stop.setObjectName(_fromUtf8("button_stop"))
        self.gridLayout.addWidget(self.button_stop, 1, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tableWidget = QtGui.QTableWidget(SimulationForm)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_3 = QtGui.QLabel(SimulationForm)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_trFee = QtGui.QLabel(SimulationForm)
        self.label_trFee.setText(_fromUtf8(""))
        self.label_trFee.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_trFee.setObjectName(_fromUtf8("label_trFee"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_trFee)
        self.verticalLayout.addLayout(self.formLayout)
        self.dial_transactFee = QtGui.QDial(SimulationForm)
        self.dial_transactFee.setAcceptDrops(False)
        self.dial_transactFee.setMaximum(50)
        self.dial_transactFee.setSingleStep(1)
        self.dial_transactFee.setProperty("value", 3)
        self.dial_transactFee.setObjectName(_fromUtf8("dial_transactFee"))
        self.verticalLayout.addWidget(self.dial_transactFee)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_simSpeed = QtGui.QLabel(SimulationForm)
        self.label_simSpeed.setText(_fromUtf8(""))
        self.label_simSpeed.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_simSpeed.setObjectName(_fromUtf8("label_simSpeed"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_simSpeed)
        self.label_4 = QtGui.QLabel(SimulationForm)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_4)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.dial_speed = QtGui.QDial(SimulationForm)
        self.dial_speed.setMinimum(1)
        self.dial_speed.setMaximum(1000)
        self.dial_speed.setObjectName(_fromUtf8("dial_speed"))
        self.verticalLayout.addWidget(self.dial_speed)
        self.label_5 = QtGui.QLabel(SimulationForm)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.label_cash = QtGui.QLabel(SimulationForm)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_cash.setFont(font)
        self.label_cash.setText(_fromUtf8(""))
        self.label_cash.setTextFormat(QtCore.Qt.AutoText)
        self.label_cash.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cash.setMargin(4)
        self.label_cash.setObjectName(_fromUtf8("label_cash"))
        self.verticalLayout.addWidget(self.label_cash)
        self.label_6 = QtGui.QLabel(SimulationForm)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout.addWidget(self.label_6)
        self.label_stocksValue = QtGui.QLabel(SimulationForm)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_stocksValue.setFont(font)
        self.label_stocksValue.setText(_fromUtf8(""))
        self.label_stocksValue.setAlignment(QtCore.Qt.AlignCenter)
        self.label_stocksValue.setMargin(4)
        self.label_stocksValue.setObjectName(_fromUtf8("label_stocksValue"))
        self.verticalLayout.addWidget(self.label_stocksValue)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(SimulationForm)
        QtCore.QMetaObject.connectSlotsByName(SimulationForm)

    def retranslateUi(self, SimulationForm):
        SimulationForm.setWindowTitle(_translate("SimulationForm", "Form", None))
        self.label.setText(_translate("SimulationForm", "Kezdeti dátum:", None))
        self.label_2.setText(_translate("SimulationForm", "Készpénz: (HUF)", None))
        self.button_start.setText(_translate("SimulationForm", "&Start", None))
        self.button_stop.setText(_translate("SimulationForm", "Sto&p", None))
        self.label_3.setText(_translate("SimulationForm", "Tranzakciós díj:", None))
        self.label_4.setText(_translate("SimulationForm", "Szimuláció sebessége:", None))
        self.label_5.setText(_translate("SimulationForm", "Készpénz:", None))
        self.label_6.setText(_translate("SimulationForm", "Befektetett vagyon:", None))

