from PyQt5 import QtCore, QtGui, QtWidgets
from pyModbusTCP.client import ModbusClient
import time
from multiprocessing import Process
#import win32api
import sys, os
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from functools import partial

class Ui_MainWindow(QObject):
    az_val = pyqtSignal()

    @pyqtSlot(int)
    def display(self, az_pot_value):
        self.azimuthDialDisplay.setValue(int(self.convert(az_pot_value)))
        self.azimuthLCDDisplay.display(int(self.convert(az_pot_value)))

    @pyqtSlot(int)
    def display2(self, el_clinometer_value):
        self.elevationDialDisplay.setValue(int(self.convert(el_clinometer_value)))
        self.elevationLCDDisplay.display(int(self.convert(el_clinometer_value)))
        
    def convert(self, az_pot_value):
        max_val = 2428.0
        min_val = 688.0
        pot_interval = max_val-min_val
        az_angle = (float(az_pot_value-min_val)*360.0)/pot_interval
        return az_angle

    def convert2(self, el_clinometer_value):
        min_val2 = 312.00
        max_val2 = 4092.00
        clinometer_interval = max_val2-min_val2
        el_angle = (float(el_clinometer_value-min_val2)*120.0)/clinometer_interval
        return el_angle

    def run_modbus_read(self):
        self.thread = QThread(parent=self)
        self.worker = ModbusWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.modbus_read)
        self.worker.azimuth_value.connect(self.display)
        self.worker.elevation_value.connect(self.display2)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def run_go_to_position(self):
        self.thread = QThread()
        self.worker = ModbusWorker()
        self.worker.moveToThread(self.thread)
        #val = self.az_valLineEdit.text()
        val = self.azimuthDialInput.value()
        val2 = self.elevationDialInput.value()
        self.thread.started.connect(self.worker.go_to_position(val=int(val), val2=int(val2)))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

        self.goPositionButton.setEnabled(False)
        self.thread.finished.connect(
            partial(self.goPositionButton.setEnabled(True))
        )
        
    def up(self):
        az_speed = 2000
        el_speed = 2000
        az_control = 0
        el_control = 1
        #1:CCW   2:CW   0:STOP
        #1:UP   2:DOWN  0:STOP 
        pol_speed = 0
        pol_control = 0
        home_internal_function = 0
        reset_enc = 0
        frequency = 0
        symbol_route = 0
        power_mode = 0
        write_command_list = [az_speed, el_speed, az_control, el_control, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
        c.write_multiple_registers(0, write_command_list)
        c.close()

    def down(self):
        az_speed = 2000
        el_speed = 2000
        az_control = 0
        el_control = 2
        #1:CCW   2:CW   0:STOP
        #1:UP   2:DOWN  0:STOP 
        pol_speed = 0
        pol_control = 0
        home_internal_function = 0
        reset_enc = 0
        frequency = 0
        symbol_route = 0
        power_mode = 0
        write_command_list = [az_speed, el_speed, az_control, el_control, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
        c.write_multiple_registers(0, write_command_list)
        c.close()

    def ccw(self):
        az_speed = 2000
        el_speed = 2000
        az_control = 1
        el_control = 0
        #1:CCW   2:CW   0:STOP
        #1:UP   2:DOWN  0:STOP 
        pol_speed = 0
        pol_control = 0
        home_internal_function = 0
        reset_enc = 0
        frequency = 0
        symbol_route = 0
        power_mode = 0
        write_command_list = [az_speed, el_speed, az_control, el_control, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
        c.write_multiple_registers(0, write_command_list)
        c.close()

    def cw(self):
        az_speed = 2000
        el_speed = 2000
        az_control = 2
        el_control = 0
        #1:CCW   2:CW   0:STOP
        #1:UP   2:DOWN  0:STOP 
        pol_speed = 0
        pol_control = 0
        home_internal_function = 0
        reset_enc = 0
        frequency = 0
        symbol_route = 0
        power_mode = 0
        write_command_list = [az_speed, el_speed, az_control, el_control, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
        c.write_multiple_registers(0, write_command_list)
        c.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 636)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(33, 33, 33);\n"
"color: white;\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.azimuthDisplayGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.azimuthDisplayGroup.setGeometry(QtCore.QRect(20, 10, 381, 231))
        self.azimuthDisplayGroup.setStyleSheet("")
        self.azimuthDisplayGroup.setObjectName("azimuthDisplayGroup")
        self.azimuthDialDisplay = QtWidgets.QDial(self.azimuthDisplayGroup)
        self.azimuthDialDisplay.setGeometry(QtCore.QRect(110, 50, 171, 161))
        self.azimuthDialDisplay.setStyleSheet("background-color: rgb(109, 152, 134);")
        self.azimuthDialDisplay.setMaximum(360)
        self.azimuthDialDisplay.setTracking(True)
        self.azimuthDialDisplay.setInvertedControls(False)
        self.azimuthDialDisplay.setWrapping(True)
        self.azimuthDialDisplay.setNotchesVisible(True)
        self.azimuthDialDisplay.setObjectName("azimuthDialDisplay")
        self.azimuthLCDDisplay = QtWidgets.QLCDNumber(self.azimuthDisplayGroup)
        self.azimuthLCDDisplay.setGeometry(QtCore.QRect(160, 120, 71, 23))
        self.azimuthLCDDisplay.setObjectName("azimuthLCDDisplay")
        self.ccwButton = QtWidgets.QCommandLinkButton(self.azimuthDisplayGroup)
        self.ccwButton.setGeometry(QtCore.QRect(20, 20, 101, 71))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/arrow-left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ccwButton.setIcon(icon)
        self.ccwButton.setIconSize(QtCore.QSize(50, 50))
        self.ccwButton.setObjectName("ccwButton")
        self.cwButton = QtWidgets.QCommandLinkButton(self.azimuthDisplayGroup)
        self.cwButton.setGeometry(QtCore.QRect(270, 20, 91, 71))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/arrow-right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cwButton.setIcon(icon1)
        self.cwButton.setIconSize(QtCore.QSize(50, 50))
        self.cwButton.setObjectName("cwButton")
        self.elevationDisplayGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.elevationDisplayGroup.setGeometry(QtCore.QRect(410, 10, 391, 231))
        self.elevationDisplayGroup.setStyleSheet("")
        self.elevationDisplayGroup.setObjectName("elevationDisplayGroup")
        self.elevationDialDisplay = QtWidgets.QDial(self.elevationDisplayGroup)
        self.elevationDialDisplay.setGeometry(QtCore.QRect(110, 50, 171, 161))
        self.elevationDialDisplay.setStyleSheet("background-color: rgb(109, 152, 134);")
        self.elevationDialDisplay.setMaximum(120)
        self.elevationDialDisplay.setSingleStep(1)
        self.elevationDialDisplay.setPageStep(10)
        self.elevationDialDisplay.setSliderPosition(0)
        self.elevationDialDisplay.setTracking(True)
        self.elevationDialDisplay.setOrientation(QtCore.Qt.Horizontal)
        self.elevationDialDisplay.setInvertedAppearance(False)
        self.elevationDialDisplay.setInvertedControls(False)
        self.elevationDialDisplay.setWrapping(False)
        self.elevationDialDisplay.setNotchTarget(3.7)
        self.elevationDialDisplay.setNotchesVisible(True)
        self.elevationDialDisplay.setObjectName("elevationDialDisplay")
        self.elevationLCDDisplay = QtWidgets.QLCDNumber(self.elevationDisplayGroup)
        self.elevationLCDDisplay.setGeometry(QtCore.QRect(160, 120, 71, 23))
        self.elevationLCDDisplay.setObjectName("elevationLCDDisplay")
        self.downButton = QtWidgets.QCommandLinkButton(self.elevationDisplayGroup)
        self.downButton.setGeometry(QtCore.QRect(280, 90, 111, 71))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/arrow-down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downButton.setIcon(icon2)
        self.downButton.setIconSize(QtCore.QSize(50, 50))
        self.downButton.setObjectName("downButton")
        self.upButton = QtWidgets.QCommandLinkButton(self.elevationDisplayGroup)
        self.upButton.setGeometry(QtCore.QRect(10, 90, 91, 71))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/arrow-up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.upButton.setIcon(icon3)
        self.upButton.setIconSize(QtCore.QSize(50, 50))
        self.upButton.setObjectName("upButton")
        self.setPositionGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.setPositionGroup.setGeometry(QtCore.QRect(210, 280, 391, 291))
        self.setPositionGroup.setObjectName("setPositionGroup")
        self.azimuthDialInput = QtWidgets.QDial(self.setPositionGroup)
        self.azimuthDialInput.setGeometry(QtCore.QRect(20, 40, 171, 161))
        self.azimuthDialInput.setStyleSheet("background-color: rgb(109, 152, 134);")
        self.azimuthDialInput.setMaximum(360)
        self.azimuthDialInput.setTracking(True)
        self.azimuthDialInput.setInvertedControls(False)
        self.azimuthDialInput.setWrapping(True)
        self.azimuthDialInput.setNotchesVisible(True)
        self.azimuthDialInput.setObjectName("azimuthDialInput")
        self.azimuthLCDDisplayInput = QtWidgets.QLCDNumber(self.setPositionGroup)
        self.azimuthLCDDisplayInput.setGeometry(QtCore.QRect(70, 110, 71, 23))
        self.azimuthLCDDisplayInput.setObjectName("azimuthLCDDisplayInput")
        self.elevationLCDDisplayInput = QtWidgets.QLCDNumber(self.setPositionGroup)
        self.elevationLCDDisplayInput.setGeometry(QtCore.QRect(250, 110, 71, 23))
        self.elevationLCDDisplayInput.setObjectName("elevationLCDDisplayInput")
        self.elevationDialInput = QtWidgets.QDial(self.setPositionGroup)
        self.elevationDialInput.setGeometry(QtCore.QRect(200, 40, 171, 161))
        self.elevationDialInput.setStyleSheet("background-color: rgb(109, 152, 134);")
        self.elevationDialInput.setMaximum(120)
        self.elevationDialInput.setSingleStep(1)
        self.elevationDialInput.setPageStep(10)
        self.elevationDialInput.setSliderPosition(0)
        self.elevationDialInput.setTracking(True)
        self.elevationDialInput.setOrientation(QtCore.Qt.Horizontal)
        self.elevationDialInput.setInvertedAppearance(False)
        self.elevationDialInput.setInvertedControls(False)
        self.elevationDialInput.setWrapping(False)
        self.elevationDialInput.setNotchTarget(3.7)
        self.elevationDialInput.setNotchesVisible(True)
        self.elevationDialInput.setObjectName("elevationDialInput")
        self.azimuthLabel = QtWidgets.QLabel(self.setPositionGroup)
        self.azimuthLabel.setGeometry(QtCore.QRect(70, 80, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.azimuthLabel.setFont(font)
        self.azimuthLabel.setStyleSheet("background-color: transparent;\n"
"font-weight: bold;\n"
"color: black;")
        self.azimuthLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.azimuthLabel.setObjectName("azimuthLabel")
        self.elevationLabel = QtWidgets.QLabel(self.setPositionGroup)
        self.elevationLabel.setGeometry(QtCore.QRect(249, 80, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.elevationLabel.setFont(font)
        self.elevationLabel.setStyleSheet("background-color: transparent;\n"
"font-weight: bold;\n"
"color: black;")
        self.elevationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.elevationLabel.setObjectName("elevationLabel")
        self.goPositionButton = QtWidgets.QPushButton(self.setPositionGroup)
        self.goPositionButton.setGeometry(QtCore.QRect(140, 240, 113, 32))
        self.goPositionButton.setStyleSheet("")
        self.goPositionButton.setObjectName("goPositionButton")
        self.elevationDialInput.raise_()
        self.azimuthDialInput.raise_()
        self.azimuthLCDDisplayInput.raise_()
        self.elevationLCDDisplayInput.raise_()
        self.azimuthLabel.raise_()
        self.elevationLabel.raise_()
        self.goPositionButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.goPositionButton.clicked.connect(self.run_go_to_position)
        self.upButton.clicked.connect(self.up)
        self.downButton.clicked.connect(self.down)
        self.cwButton.clicked.connect(self.cw)
        self.ccwButton.clicked.connect(self.ccw)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.azimuthDisplayGroup.setTitle(_translate("MainWindow", "Azimuth"))
        self.ccwButton.setText(_translate("MainWindow", "CCW"))
        self.cwButton.setText(_translate("MainWindow", "CW"))
        self.elevationDisplayGroup.setTitle(_translate("MainWindow", "Elevation"))
        self.downButton.setText(_translate("MainWindow", "DOWN"))
        self.upButton.setText(_translate("MainWindow", "UP"))
        self.setPositionGroup.setTitle(_translate("MainWindow", "Set Position Values"))
        self.azimuthLabel.setText(_translate("MainWindow", "Azimuth"))
        self.elevationLabel.setText(_translate("MainWindow", "Elevation"))
        self.goPositionButton.setText(_translate("MainWindow", "Go To Position"))

class ModbusWorker(QObject):
    finished = pyqtSignal()
    azimuth_value = pyqtSignal(int)
    elevation_value = pyqtSignal(int)
    #read_list = []
    def modbus_read(self):
        #send signal with a new value
        while True:
            list = c.read_input_registers(0, 26)
            az_val = list[12]
            el_val = list[5]
            self.azimuth_value.emit(az_val)
            self.elevation_value.emit(el_val)
            self.finished.emit()
            time.sleep(0.01)
            
    def convert_input_to_pot(self, angle):
        max_val = 2428.0
        min_val = 688.0
        pot_interval = max_val-min_val
        converted_pot = (angle*(pot_interval)/360) + min_val
        return converted_pot

    def convert_input_to_cli(self, angle):
        max_val = 4092.0
        min_val = 316.0
        cli_interval = max_val-min_val
        converted_cli = (angle*(cli_interval)/120) + min_val
        return converted_cli

    def go_to_position(self, val, val2):
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
        converted_pot = self.convert_input_to_pot(angle=val)
        converted_cli = self.convert_input_to_cli(angle=val2)
        while True:
            try:
                list = c.read_input_registers(0, 26)
                az_val = list[12]
                el_val = list[5]
        
                if az_val <= converted_pot+2 and az_val >= converted_pot-2:
                    az_control = 0
                    el_control = 0
                    az_speed = 0
                    write_command_list = [az_speed, el_speed, az_control, el_control, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
                    c.write_multiple_registers(0, write_command_list)
                    time.sleep(1)
                    
                elif converted_pot > az_val:
                    az_control = 1
                    el_control = 0
                    write_command_list = [az_speed, el_speed, az_control, el_control, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
                    c.write_multiple_registers(0, write_command_list)
                    time.sleep(0.01)
                else:
                    az_control = 2
                    el_control = 0
                    write_command_list = [az_speed, el_speed, az_control, el_control, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
                    c.write_multiple_registers(0, write_command_list)
                    time.sleep(1)

                if el_val <= converted_cli+2 and el_val >= converted_cli-2:
                    az_control = 0
                    el_control = 0
                    write_command_list = [az_speed, el_speed, az_control, el_control, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
                    c.write_multiple_registers(0, write_command_list)
                    time.sleep(1)
                elif converted_cli > el_val:
                    az_control = 0
                    el_control = 1
                    write_command_list = [az_speed, el_speed, az_control, el_control, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
                    c.write_multiple_registers(0, write_command_list)
                    time.sleep(1)
                else:
                    az_control = 0
                    el_control = 2
                    write_command_list = [az_speed, el_speed, az_control, el_control, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
                    c.write_multiple_registers(0, write_command_list)
                    time.sleep(1)
            except Exception as e:
                print(e)
                time.sleep(0.001)
            self.finished.emit()

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
