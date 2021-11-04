from PyQt5 import QtCore, QtGui, QtWidgets
from pyModbusTCP.client import ModbusClient
import time
from multiprocessing import Process
#import win32api
import threading
from threading import Thread, Lock
import sys, os
from PyQt5.QtCore import QObject, QRunnable, QThread, QTimer, pyqtSignal, pyqtSlot
from functools import partial


class Ui_MainWindow(QObject):
    az_val = pyqtSignal()

    @pyqtSlot(int)
    def display(self, az_pot_value):
        self.az_lcdDisplay.display(az_pot_value)
        self.el_lcdDisplay.display(self.convert(az_pot_value=az_pot_value))

    def convert(self, az_pot_value):
        max_val = 2428.0
        min_val = 688.0
        pot_interval = max_val-min_val
        az_angle = (float(az_pot_value-min_val)*360.0)/pot_interval
        return az_angle

    def run_modbus_read(self):
        self.thread = QThread(parent=self)
        self.worker = ModbusWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.modbus_read)
        self.worker.azimuth_value.connect(self.display)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def run_go_to_position(self):
        self.thread = QThread()
        self.worker = ModbusWorker()
        self.worker.moveToThread(self.thread)
        #val = self.az_valLineEdit.text()
        val = self.azimuth_input_dial.value()
        self.thread.started.connect(self.worker.go_to_position(val=int(val)))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

        self.btn_goToPosition.setEnabled(False)
        self.thread.finished.connect(
            partial(self.btn_goToPosition.setEnabled(True))
            #lambda: 
        )

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(503, 510)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.input_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.input_groupBox.setGeometry(QtCore.QRect(240, 10, 251, 121))
        self.input_groupBox.setObjectName("input_groupBox")
        self.az_valLineEdit = QtWidgets.QLineEdit(self.input_groupBox)
        self.az_valLineEdit.setGeometry(QtCore.QRect(120, 30, 113, 20))
        self.az_valLineEdit.setObjectName("az_valLineEdit")
        self.azimuth_label = QtWidgets.QLabel(self.input_groupBox)
        self.azimuth_label.setGeometry(QtCore.QRect(20, 30, 101, 20))
        self.azimuth_label.setObjectName("azimuth_label")
        self.elevation_label = QtWidgets.QLabel(self.input_groupBox)
        self.elevation_label.setGeometry(QtCore.QRect(20, 60, 111, 20))
        self.elevation_label.setObjectName("elevation_label")
        self.el_valLineEdit = QtWidgets.QLineEdit(self.input_groupBox)
        self.el_valLineEdit.setGeometry(QtCore.QRect(120, 60, 113, 20))
        self.el_valLineEdit.setObjectName("el_valLineEdit")
        self.btn_goToPosition = QtWidgets.QPushButton(self.input_groupBox)
        self.btn_goToPosition.setGeometry(QtCore.QRect(160, 90, 75, 23))
        self.btn_goToPosition.setObjectName("saveBtn")
        self.controls_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.controls_groupBox.setGeometry(QtCore.QRect(240, 150, 251, 111))
        self.controls_groupBox.setObjectName("controls_groupBox")
        self.el_upBtn = QtWidgets.QPushButton(self.controls_groupBox)
        self.azimuth_input_dial = QtWidgets.QDial(self.centralwidget)
        self.azimuth_input_dial.setGeometry(QtCore.QRect(260, 275, 200, 200))
        self.azimuth_input_dial.setAcceptDrops(False)
        self.azimuth_input_dial.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.azimuth_input_dial.setAutoFillBackground(False)
        self.azimuth_input_dial.setMaximum(360)
        self.azimuth_input_dial.setPageStep(45)
        self.azimuth_input_dial.setSliderPosition(0)
        self.azimuth_input_dial.setTracking(True)
        self.azimuth_input_dial.setOrientation(QtCore.Qt.Vertical)
        self.azimuth_input_dial.setInvertedAppearance(True)
        self.azimuth_input_dial.setInvertedControls(True)
        self.azimuth_input_dial.setWrapping(True)
        self.azimuth_input_dial.setNotchesVisible(True)
        self.azimuth_input_dial.setObjectName("dial")
        self.el_upBtn.setGeometry(QtCore.QRect(90, 20, 75, 23))
        self.el_upBtn.setObjectName("el_upBtn")
        self.el_downBtn = QtWidgets.QPushButton(self.controls_groupBox)
        self.el_downBtn.setGeometry(QtCore.QRect(90, 80, 75, 23))
        self.el_downBtn.setObjectName("el_downBtn")
        self.az_ccwBtn = QtWidgets.QPushButton(self.controls_groupBox)
        self.az_ccwBtn.setGeometry(QtCore.QRect(10, 50, 75, 23))
        self.az_ccwBtn.setObjectName("az_ccwBtn")
        self.az_cwBtn = QtWidgets.QPushButton(self.controls_groupBox)
        self.az_cwBtn.setGeometry(QtCore.QRect(170, 50, 75, 23))
        self.az_cwBtn.setObjectName("az_cwBtn")
        self.display_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.display_groupBox.setGeometry(QtCore.QRect(20, 10, 201,400))
        self.display_groupBox.setObjectName("display_groupBox")
        self.az_lcdDisplay = QtWidgets.QLCDNumber(self.display_groupBox)
        self.az_lcdDisplay.setGeometry(QtCore.QRect(10, 20, 181, 161))
        self.az_lcdDisplay.setAutoFillBackground(True)
        self.az_lcdDisplay.setObjectName("az_lcdDisplay")
        self.el_lcdDisplay = QtWidgets.QLCDNumber(self.display_groupBox)
        self.el_lcdDisplay.setGeometry(QtCore.QRect(10, 200, 181, 161))
        self.el_lcdDisplay.setAutoFillBackground(True)
        self.el_lcdDisplay.setObjectName("el_lcdDisplay")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 503, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        self.btn_goToPosition.clicked.connect(self.run_go_to_position)

        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.input_groupBox.setTitle(_translate("MainWindow", "Pozition Inputs"))
        self.azimuth_label.setText(_translate("MainWindow", "Azimuth Angle:"))
        self.elevation_label.setText(_translate("MainWindow", "Azimuth Speed:"))
        self.btn_goToPosition.setText(_translate("MainWindow", "Go"))
        self.controls_groupBox.setTitle(_translate("MainWindow", "Manuel Controls"))
        self.el_upBtn.setText(_translate("MainWindow", "Up"))
        self.el_downBtn.setText(_translate("MainWindow", "Down"))
        self.az_ccwBtn.setText(_translate("MainWindow", "CCW"))
        self.az_cwBtn.setText(_translate("MainWindow", "CW"))
        self.display_groupBox.setTitle(_translate("MainWindow", "Displays"))

class ModbusWorker(QObject,):
    finished = pyqtSignal()
    azimuth_value = pyqtSignal(int)
    #read_list = []
    
    def modbus_read(self):
        #send signal with a new value
        while True:
            list = c.read_input_registers(0, 26)
            az_val = list[12]
            # if len(self.read_list) == 0:
            #     self.read_list.append(list)
            # else:
            #     self.read_list.clear()
            #     self.read_list.append(list)
            self.azimuth_value.emit(az_val)
            time.sleep(0.01)
            self.finished.emit()
            return list

    def convert_input_to_pot(self, angle):
        max_val = 2428.0
        min_val = 688.0
        pot_interval = max_val-min_val
        converted_pot = (angle*(pot_interval)/360) + min_val
        return converted_pot

    def go_to_position(self, val):
        az_speed = 2000
        el_speed = 1000
        #1:CCW   2:CW   0:STOP
        #1:UP   2:DOWN  0:STOP 
        pol_speed = 0
        pol_control = 0
        home_internal_function = 0
        reset_enc = 0
        frequency = 0
        symbol_route = 0
        power_mode = 0
        print(val)
        converted_pot = self.convert_input_to_pot(angle=val)
        while True:
            try:
                # print(self.read_list[0])
                # list = self.read_list[0]
                list = c.read_input_registers(0,26)
                print('Converted: ' + str(converted_pot))
                az_val = list[12]
                print('Azimuth: ' + str(az_val))
                if az_val <= converted_pot+2 and az_val >= converted_pot-2:
                    az_control = 0
                    az_speed = 0
                    write_command_list = [az_speed, el_speed, az_control, 0, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
                    c.write_multiple_registers(0, write_command_list)
                    time.sleep(1)
                    self.finished.emit()
                    break
                elif converted_pot > az_val:
                    az_control = 1
                    write_command_list = [az_speed, el_speed, az_control, 0, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
                    c.write_multiple_registers(0, write_command_list)
                    time.sleep(0.01)
                else:
                    az_control = 2
                    write_command_list = [az_speed, el_speed, az_control, 0, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
                    c.write_multiple_registers(0, write_command_list)
                    time.sleep(0.01)
            except Exception as e:
                #win32api.MessageBox(0,f'{exc_type}: {e}, {fname}',f'{exc_obj}',0x00000010)
                print(e)
                break
                #time.sleep(0.001)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    c = ModbusClient(host="10.0.1.36", port=5002, auto_open=True, auto_close=True)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.run_modbus_read()
    MainWindow.show()
    sys.exit(app.exec_())
