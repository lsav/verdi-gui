# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'verdi-gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(710, 842)
        self.verticalLayout_4 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.frame_1 = QtGui.QFrame(Form)
        self.frame_1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_1.setObjectName(_fromUtf8("frame_1"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_1)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.powerFrame = QtGui.QFrame(self.frame_1)
        self.powerFrame.setAutoFillBackground(True)
        self.powerFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.powerFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.powerFrame.setObjectName(_fromUtf8("powerFrame"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.powerFrame)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.statusGroup = QtGui.QGroupBox(self.powerFrame)
        self.statusGroup.setObjectName(_fromUtf8("statusGroup"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.statusGroup)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.shutter_btn = QtGui.QPushButton(self.statusGroup)
        self.shutter_btn.setCheckable(True)
        self.shutter_btn.setObjectName(_fromUtf8("shutter_btn"))
        self.verticalLayout_2.addWidget(self.shutter_btn)
        self.verticalLayout_3.addWidget(self.statusGroup)
        self.groupBox = QtGui.QGroupBox(self.powerFrame)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.power_lcd = QtGui.QLCDNumber(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.power_lcd.sizePolicy().hasHeightForWidth())
        self.power_lcd.setSizePolicy(sizePolicy)
        self.power_lcd.setMinimumSize(QtCore.QSize(120, 40))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.power_lcd.setPalette(palette)
        self.power_lcd.setAutoFillBackground(True)
        self.power_lcd.setFrameShape(QtGui.QFrame.Box)
        self.power_lcd.setSmallDecimalPoint(True)
        self.power_lcd.setNumDigits(3)
        self.power_lcd.setObjectName(_fromUtf8("power_lcd"))
        self.verticalLayout.addWidget(self.power_lcd)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.power_up = QtGui.QToolButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.power_up.sizePolicy().hasHeightForWidth())
        self.power_up.setSizePolicy(sizePolicy)
        self.power_up.setArrowType(QtCore.Qt.UpArrow)
        self.power_up.setObjectName(_fromUtf8("power_up"))
        self.horizontalLayout_3.addWidget(self.power_up)
        self.power_down = QtGui.QToolButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.power_down.sizePolicy().hasHeightForWidth())
        self.power_down.setSizePolicy(sizePolicy)
        self.power_down.setArrowType(QtCore.Qt.DownArrow)
        self.power_down.setObjectName(_fromUtf8("power_down"))
        self.horizontalLayout_3.addWidget(self.power_down)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_3 = QtGui.QGroupBox(self.powerFrame)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.export_btn = QtGui.QPushButton(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.export_btn.sizePolicy().hasHeightForWidth())
        self.export_btn.setSizePolicy(sizePolicy)
        self.export_btn.setToolTip(_fromUtf8(""))
        self.export_btn.setObjectName(_fromUtf8("export_btn"))
        self.horizontalLayout_7.addWidget(self.export_btn)
        self.openLog_btn = QtGui.QToolButton(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openLog_btn.sizePolicy().hasHeightForWidth())
        self.openLog_btn.setSizePolicy(sizePolicy)
        self.openLog_btn.setObjectName(_fromUtf8("openLog_btn"))
        self.horizontalLayout_7.addWidget(self.openLog_btn)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.horizontalLayout.addWidget(self.powerFrame)
        self.frame_4 = QtGui.QFrame(self.frame_1)
        self.frame_4.setAutoFillBackground(True)
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.healthGroup = QtGui.QGroupBox(self.frame_4)
        self.healthGroup.setObjectName(_fromUtf8("healthGroup"))
        self.gridLayout_2 = QtGui.QGridLayout(self.healthGroup)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.C_box = QtGui.QLineEdit(self.healthGroup)
        self.C_box.setReadOnly(True)
        self.C_box.setObjectName(_fromUtf8("C_box"))
        self.gridLayout_2.addWidget(self.C_box, 0, 1, 1, 1)
        self.D1C_box = QtGui.QLineEdit(self.healthGroup)
        self.D1C_box.setReadOnly(True)
        self.D1C_box.setObjectName(_fromUtf8("D1C_box"))
        self.gridLayout_2.addWidget(self.D1C_box, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.healthGroup)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_1 = QtGui.QLabel(self.healthGroup)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.gridLayout_2.addWidget(self.label_1, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.healthGroup)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.D2C_box = QtGui.QLineEdit(self.healthGroup)
        self.D2C_box.setReadOnly(True)
        self.D2C_box.setObjectName(_fromUtf8("D2C_box"))
        self.gridLayout_2.addWidget(self.D2C_box, 2, 1, 1, 1)
        self.verticalLayout_5.addWidget(self.healthGroup)
        self.groupBox_2 = QtGui.QGroupBox(self.frame_4)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        self.D2HST_box = QtGui.QLineEdit(self.groupBox_2)
        self.D2HST_box.setReadOnly(True)
        self.D2HST_box.setObjectName(_fromUtf8("D2HST_box"))
        self.gridLayout_3.addWidget(self.D2HST_box, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 3, 0, 1, 1)
        self.ET_box = QtGui.QLineEdit(self.groupBox_2)
        self.ET_box.setReadOnly(True)
        self.ET_box.setObjectName(_fromUtf8("ET_box"))
        self.gridLayout_3.addWidget(self.ET_box, 3, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)
        self.D1HST_box = QtGui.QLineEdit(self.groupBox_2)
        self.D1HST_box.setObjectName(_fromUtf8("D1HST_box"))
        self.gridLayout_3.addWidget(self.D1HST_box, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 2, 0, 1, 1)
        self.BT_box = QtGui.QLineEdit(self.groupBox_2)
        self.BT_box.setObjectName(_fromUtf8("BT_box"))
        self.gridLayout_3.addWidget(self.BT_box, 2, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_3.addWidget(self.label_9, 4, 0, 1, 1)
        self.VT_box = QtGui.QLineEdit(self.groupBox_2)
        self.VT_box.setObjectName(_fromUtf8("VT_box"))
        self.gridLayout_3.addWidget(self.VT_box, 4, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_3.addWidget(self.label_10, 5, 0, 1, 1)
        self.LBOT_box = QtGui.QLineEdit(self.groupBox_2)
        self.LBOT_box.setObjectName(_fromUtf8("LBOT_box"))
        self.gridLayout_3.addWidget(self.LBOT_box, 5, 1, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBox_2)
        self.horizontalLayout.addWidget(self.frame_4)
        self.verticalLayout_4.addWidget(self.frame_1)
        self.frame_2 = QtGui.QFrame(Form)
        self.frame_2.setAutoFillBackground(True)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.output_box = QtGui.QTextEdit(self.frame_2)
        self.output_box.setReadOnly(True)
        self.output_box.setObjectName(_fromUtf8("output_box"))
        self.verticalLayout_6.addWidget(self.output_box)
        self.frame = QtGui.QFrame(self.frame_2)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.input_box = QtGui.QLineEdit(self.frame)
        self.input_box.setObjectName(_fromUtf8("input_box"))
        self.horizontalLayout_2.addWidget(self.input_box)
        self.doc_btn = QtGui.QToolButton(self.frame)
        self.doc_btn.setObjectName(_fromUtf8("doc_btn"))
        self.horizontalLayout_2.addWidget(self.doc_btn)
        self.verticalLayout_6.addWidget(self.frame)
        self.verticalLayout_4.addWidget(self.frame_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Verdi GUI", None))
        self.statusGroup.setTitle(_translate("Form", "Shutter", None))
        self.shutter_btn.setText(_translate("Form", "CLOSED", None))
        self.groupBox.setTitle(_translate("Form", "Power (Watt)", None))
        self.power_up.setText(_translate("Form", "...", None))
        self.power_down.setText(_translate("Form", "...", None))
        self.groupBox_3.setTitle(_translate("Form", "Log", None))
        self.export_btn.setText(_translate("Form", "Export", None))
        self.openLog_btn.setText(_translate("Form", "Open", None))
        self.healthGroup.setTitle(_translate("Form", "Currents (Amp)", None))
        self.label_2.setText(_translate("Form", "Diode 1      ", None))
        self.label_1.setText(_translate("Form", "Average      ", None))
        self.label_3.setText(_translate("Form", "Diode 2      ", None))
        self.groupBox_2.setTitle(_translate("Form", "Temperatures (Celsius)", None))
        self.label_4.setText(_translate("Form", "Diode 2 heatsink", None))
        self.label_5.setText(_translate("Form", "Etalon", None))
        self.label_8.setText(_translate("Form", "Diode 1 heatsink", None))
        self.label.setText(_translate("Form", "Baseplate", None))
        self.label_9.setText(_translate("Form", "Vanadate", None))
        self.label_10.setText(_translate("Form", "LBO", None))
        self.input_box.setPlaceholderText(_translate("Form", "Enter command here, or \"help\" for options", None))
        self.doc_btn.setText(_translate("Form", "...", None))

