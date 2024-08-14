import sys, os
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QComboBox, QGridLayout, QMainWindow, QDialog
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QFrame
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon


from control_settings_window import ControlSettingsWindow
from key_press_handler import KeyPressHandler

# Function to list available serial ports
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    available_ports = [port.device for port in ports]
    return available_ports

class SerialReadThread(QThread):
    newData = pyqtSignal(str)

    def __init__(self, serial_connection):
        super().__init__()
        self.serial_connection = serial_connection
        self.running = True

    def run(self):
        while self.running:
            if self.serial_connection.in_waiting > 0:
                data = self.serial_connection.read(self.serial_connection.in_waiting).decode('utf-8')
                self.newData.emit(data)

    def stop(self):
        self.running = False
        self.wait()

# Serial Read Window (will be removed)
class SerialReadWindow(QDialog):
    def __init__(self, serial_connection):
        super().__init__()
        self.serial_connection = serial_connection
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Serial Port Reader')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.outputLabel = QLabel('Reading data from serial port\n')
        layout.addWidget(self.outputLabel)

        self.setLayout(layout)

        self.thread = SerialReadThread(self.serial_connection)
        self.thread.newData.connect(self.updateOutput)
        self.thread.start()

    def updateOutput(self, data):
        self.outputLabel.setText(self.outputLabel.text() + data)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.control_settings_window = ControlSettingsWindow()
        self.key_press_handler = None

        # Serial Commands
        self.key_processed = False

        
        self.hold_commands = {
            Qt.Key_A: "7100",
            Qt.Key_D: "7110",
            Qt.Key_S: "7200",
            Qt.Key_W: "7210",
        }

        self.toggle_commands = {
            Qt.Key_1: "7110",  # Rotation right
            Qt.Key_2: "-1070", # Drop
            Qt.Key_R: "-1070"
        }

        # self.left_sweep_command = "7100"
        # self.right_sweep_command = "7110"
        # self.down_sweep_command = "7200"
        # self.up_sweep_command = "7210"
        # self.calibration_command = "8700"
        # self.drop_command = "-1070"
        
    # NEED TO BE REMOVED (SETTINGS CODE) --------------
    def retrieve_control_settings(self):
        # Retrieve the selected control settings
        settings = self.control_settings_window.get_selected_settings()
        print(settings)  # Or use the settings as needed
    # ------------------------------------------------

    
    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            key = event.key()
            # if (key in self.operator_commands) and (not self.key_processed):
            #     print(f"Key pressed: {key}")
            #     command = self.operator_commands[key]
            #     self.sendSerialCode(command)
            #     self.key_processed = True
            #     print(f"Sent press command: {command} to serial port")
            #     event.accept()

            #if (not self.key_processed):
            if (key in self.hold_commands) and (not self.key_processed):
                print(f"Operator key pressed: {key}")
                command = self.hold_commands[key]
                self.sendSerialCode(command)
                self.key_processed = True
                print(f"Sent press command: {command} to serial port")
                # event.accept()

            elif key in self.toggle_commands:
                print(f"User key pressed: {key}")
                command = self.toggle_commands[key]
                self.sendSerialCode(command)
                #self.key_processed = False
                print(f"Sent press command: {command} to serial port")
                # event.accept()
            event.accept()

    
    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            key = event.key()
            if (key in self.hold_commands) and (self.key_processed):
                print(f"Key released: {key}")
                command = self.hold_commands[key]
                self.sendSerialCode(command)
                self.key_processed = False
                print(f"Sent release command: {command} to serial port")

    # def keyPressEvent(self, event):
    #     ''' Send serial code based on key press '''
    #     if not self.key_processed:
    #         key = event.key()          
    #         self.selectSerialCommand(key)
    #         super().keyPressEvent(event)
    #         self.key_processed = key

    # def keyReleaseEvent(self, event):
    #     ''' Send stop code when key is released '''
    #     if self.key_processed:
    #         key = event.key()
    #         if key == self.key_processed:
    #             self.selectSerialCommand(key)
    #             self.key_processed = None

            # self.selectSerialCommand(key)
            # self.key_processed = False
            
            # TO DO FOR ME -----------------------------------
            # Update buttons to not be buttons
            # Change the command labels to be rotation and elevation (space and enter)
            # Double check the slider values being sent
            # Check drop command
            # USE SEND SERIAL CODE
            # Clean UP CODE
            # ------------------------------------------------

    def selectSerialCommand(self, key):
        actions = {
            Qt.Key_A: lambda: self.sendSerialCode(self.left_sweep_command),
            Qt.Key_W: lambda: self.sendSerialCode(self.up_sweep_command),
            Qt.Key_D: lambda: self.sendSerialCode(self.right_sweep_command),
            Qt.Key_S: lambda: self.sendSerialCode(self.down_sweep_command),
            Qt.Key_Space: lambda: self.sendSerialCode(self.drop_command),
            Qt.Key_Return: lambda: self.sendSerialCode(self.calibration_command)

        }
        # action = actions.get(key)
        
        # if action:
        #     action()
        #     self.key_processed = !self.key_processed
        if key in actions:
            actions[key]()
            # self.key_processed = True
      

    def initUI(self):

        # title and styleimport os
        self.setWindowTitle('BCI Boccia Ramp Control')
        self.setStyleSheet("background-color: #2d2d2d; color: #ffffff;")
        
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        
        # Layouts
        mainLayout = QVBoxLayout()
        buttonsLayout = QGridLayout()
        topRightButtonsLayout = QHBoxLayout()
        
        # Connect Button
        self.connectButton = QPushButton('Connect')
        self.connectButton.setStyleSheet("font-size: 16px; background-color: green; color: #ffffff; padding: 5px; border: 1px solid #ffffff;")
        topRightButtonsLayout.addWidget(self.connectButton)
        topRightButtonsLayout.addStretch()
        self.connectButton.clicked.connect(self.toggleConnection)
        self.connectButton.clicked.connect(self.connectSerialPort)
        
        # Calibration Button
        self.calibrationButton = QPushButton('Calibrate')
        self.calibrationButton.clicked.connect(lambda: self.sendSerialCode(self.calibration_command))
        self.calibrationButton.setStyleSheet("""
                                                QPushButton {
                                                    font-size: 16px;
                                                    background-color: #3c3c3c;
                                                    color: #ffffff;
                                                    padding: 5px;
                                                    border: 1px solid #ffffff;
                                                }
                                                QPushButton:hover {
                                                    background-color: #555555;
                                                }
                                            """)
        
        topRightButtonsLayout.addWidget(self.calibrationButton)
        mainLayout.addLayout(topRightButtonsLayout)

        # Connection Status Label
        statusLayout = QHBoxLayout()
        self.statusLabel = QLabel('Status: Disconnected')
        self.statusLabel.setStyleSheet("font-size: 16px; color: #a9a9a9;")

        # Port Selection Label and ComboBox
        comLabel = QLabel('PORT')
        comLabel.setStyleSheet("font-size: 16px; color: #a9a9a9;")

        self.comComboBox = QComboBox()
        self.comComboBox.addItems(list_serial_ports())
        self.comComboBox.setStyleSheet("font-size: 16px; width: 70px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")

        statusLayout.addWidget(self.statusLabel)
        statusLayout.addStretch()
        statusLayout.addWidget(comLabel)
        statusLayout.addWidget(self.comComboBox)


 # SPEED CONTROLS -------------------------------
        controlsLayout = QHBoxLayout()
        speedLabel = QLabel('Speed')
        speedLabel.setStyleSheet("font-size: 16px; color: #2c2c2c;")
      
        # Height Speed Slider
        heightLayout = QHBoxLayout()
        heightLabel = QLabel('Height Speed: ')
        heightLabel.setStyleSheet("QLabel { font: 20px Calibri; color: #b48ead;}")
        
        self.heightSlider = QSlider(Qt.Horizontal)
        self.heightSlider.setMinimum(0)
        self.heightSlider.setMaximum(100)
        self.heightSlider.setValue(50)
        self.heightSlider.valueChanged.connect(self.updateHeightLabel)
        self.heightSlider.sliderReleased.connect(self.sendHeightValue)
        self.heightSlider.setStyleSheet("QSlider::groove:horizontal {background: #3c3c3c; height: 10px;}"
                                  "QSlider::handle:horizontal {background: #b48ead; width: 20px; margin: -5px 0;}")

        self.heightValueLabel = QLabel('50%')
        self.heightValueLabel.setStyleSheet("font-size: 16px; color: white;")
        
        heightLayout.addWidget(heightLabel)
        heightLayout.addWidget(self.heightSlider)
        heightLayout.addWidget(self.heightValueLabel)
        
        # Rotation Speed Slider
        rotationLayout = QHBoxLayout()
        rotationLabel = QLabel('Rotation Speed: ')
        rotationLabel.setStyleSheet("QLabel { font: 20px Calibri; color: #b48ead;}")
        self.rotationSlider = QSlider(Qt.Horizontal)
        self.rotationSlider.setMinimum(0)
        self.rotationSlider.setMaximum(100)
        self.rotationSlider.setValue(50)
        self.rotationSlider.valueChanged.connect(self.updateRotationLabel)
        self.rotationSlider.sliderReleased.connect(self.sendRotationValue)
        self.rotationSlider.setStyleSheet("QSlider::groove:horizontal {background: #3c3c3c; height: 10px;}"
                                  "QSlider::handle:horizontal {background: #b48ead; width: 20px; margin: -5px 0;}")

        self.rotationValueLabel = QLabel('50%')
        self.rotationValueLabel.setStyleSheet("font-size: 16px; color: #ffffff;")

        rotationLayout.addWidget(rotationLabel)
        rotationLayout.addWidget(self.rotationSlider)
        rotationLayout.addWidget(self.rotationValueLabel)


        # CONTROLS -------------------------
        controlsLabel = QLabel('Controls')
        controlsLabel.setStyleSheet("QLabel { font: 20px Calibri; color: #b48ead;}")

        buttonStyle = """
        QPushButton {
            width: 50px;
            height: 50px;
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #ffffff;
        }
        QPushButton:hover {
            background-color: #5c5c5c;
        }
        QPushButton:pressed {
            background-color: #7c7c7c;
        }
        """

        # Arrow Keys Visual
        buttonsLayout = QGridLayout()

        buttonsLayout = QGridLayout()
        self.upButton = QPushButton('W ↑')
        self.downButton = QPushButton('S ↓')
        self.leftButton = QPushButton('A ←')
        self.rightButton = QPushButton('→ D')

        self.dropButton = QPushButton('Drop \n(R)')

        self.upButton.setEnabled(False)
        self.downButton.setEnabled(False)
        self.leftButton.setEnabled(False)
        self.rightButton.setEnabled(False)
        self.dropButton.setEnabled(False)

        self.upButton.setStyleSheet(buttonStyle)
        self.downButton.setStyleSheet(buttonStyle)
        self.leftButton.setStyleSheet(buttonStyle)
        self.rightButton.setStyleSheet(buttonStyle)
        self.dropButton.setStyleSheet(buttonStyle)

        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        buttonsLayout.addItem(spacer, 0, 3)

        buttonsLayout.addWidget(self.upButton, 0, 1)
        buttonsLayout.addWidget(self.downButton, 2, 1)
        buttonsLayout.addWidget(self.leftButton, 1, 0)
        buttonsLayout.addWidget(self.rightButton, 1, 2)
        buttonsLayout.addWidget(self.dropButton, 1, 1)

        buttonsLayout.setColumnStretch(0, 2)
        buttonsLayout.setColumnStretch(1, 2)
        buttonsLayout.setColumnStretch(2, 2)

        # Adding the buttons to the layout
        heightLayout = QHBoxLayout()
        heightLayout.addWidget(heightLabel)
        heightLayout.addWidget(self.heightValueLabel)

        slidersLayout = QVBoxLayout()
        slidersLayout.addLayout(heightLayout)
        slidersLayout.addWidget(self.heightSlider)

        rotationLayout = QHBoxLayout()
        rotationLayout.addWidget(rotationLabel)
        rotationLayout.addWidget(self.rotationValueLabel)
        slidersLayout.addLayout(rotationLayout)
        slidersLayout.addWidget(self.rotationSlider)

        controlsLayout.addLayout(buttonsLayout)
        controlsLayout.addLayout(slidersLayout)

        
        # ENTER ADDED -------------------------  
        settingsButton = QPushButton('Control Settings')
        settingsButton.setStyleSheet("""
                                        QPushButton {
                                            font-size: 16px;
                                            background-color: #3c3c3c;
                                            color: #ffffff;
                                            border: 1px solid #ffffff;
                                        }
                                        QPushButton:hover {
                                            background-color: #555555;
                                        }
                                    """)
        settingsButton.clicked.connect(self.openControlSettings)

        serialReadButton = QPushButton('Read Serial')
        serialReadButton.setStyleSheet("""
                                        QPushButton {
                                            font-size: 16px;
                                            background-color: #3c3c3c;
                                            color: #ffffff;
                                            border: 1px solid #ffffff;
                                        }
                                        QPushButton:hover {
                                            background-color: #555555;
                                        }
                                    """)
        serialReadButton.clicked.connect(self.openSerialReadWindow)


        mainLayout.addLayout(statusLayout)
        mainLayout.addWidget(controlsLabel)
        mainLayout.addLayout(controlsLayout)
        mainLayout.addWidget(speedLabel)
        mainLayout.addWidget(settingsButton)
        mainLayout.addWidget(serialReadButton)
        centralWidget.setLayout(mainLayout)
    

 # FUNCTIONS ----------------------------------------

    # Update the height label
    def updateHeightLabel(self):
        value = self.heightSlider.value()
        self.heightValueLabel.setText(f'{value}%')

    # Update the rotation label
    def updateRotationLabel(self):
        value = self.rotationSlider.value()
        self.rotationValueLabel.setText(f'{value}%')

    # Toggle the connection status
    def toggleConnection(self):
        if self.connectButton.text() == 'Connect':
            self.connectButton.setText('Disconnect')
            self.connectButton.setStyleSheet("font-size: 16px; background-color: red; color: #ffffff; padding: 5px; border: 1px solid #ffffff;")
            self.statusLabel.setText('Status: Connected')
        else:
            self.connectButton.setText('Connect')
            self.connectButton.setStyleSheet("font-size: 16px; background-color: green; color: #ffffff; padding: 5px; border: 1px solid #ffffff;")
            self.statusLabel.setText('Status: Disconnected')
            
    # Connect to the selected serial port
    def connectSerialPort(self):
        port = self.comComboBox.currentText()
        try:
            self.serial_connection = serial.Serial(port, 9600, timeout=1)
            self.statusLabel.setText('Status: Connected')
        except Exception as e:
            self.statusLabel.setText(f'Status: Failed to connect')

    # Caclulate and send the Rotation slider value 
    def sendRotationValue(self):
        if hasattr(self, 'serial_connection') and self.serial_connection.is_open:
            value = (((self.rotationSlider.value()) / 100) * 1000) + 5000
            serial_value = f'{int(value):03d}\n'.encode()
            print(f'Rotation Value {serial_value}')
            try:
                self.serial_connection.write(serial_value)
            except Exception as e:
                self.statusLabel.setText(f'Status: Error sending rotation value')
        else:
            self.statusLabel.setText('Status: No serial connection')

    # Caclulate and send the Rotation slider value 
    def sendHeightValue(self):
        if hasattr(self, 'serial_connection') and self.serial_connection.is_open:
            value = (((self.heightSlider.value())/100) * 255 ) + 6000
            serial_value = f'{int(value):03d}\n'.encode()
            print(f'Height Value {serial_value}')
            try:
                self.serial_connection.write(serial_value)
            except Exception as e:
                self.statusLabel.setText(f'Status: Error sending height value')
        else:
            self.statusLabel.setText('Status: No serial connection')


    # def keyPressEvent(self, event):
    #     selected_key_L = self.control_settings_window.leftComboBox.currentText()
    #     selected_key_R = self.control_settings_window.rightComboBox.currentText()
        
    #     if event.text().upper() == selected_key_L:
    #         self.sendLeftArrowCode()
    #     elif event.text().upper() == selected_key_R:
    #         self.sendRightArrowCode()

    
    # def keyReleaseEvent(self, event):
    #     selected_key_L = self.control_settings_window.leftComboBox.currentText()
    #     selected_key_R = self.control_settings_window.rightComboBox.currentText()
        
    #     if event.text().upper() in [selected_key_L, selected_key_R]:
    #         self.sendStopCode()


    # SEND SERIAL CODE FUNCTION
    def sendSerialCode(self, code):
        if hasattr(self, 'serial_connection') and self.serial_connection.is_open:
            try:
                code_str = str(code) + "\n"
                self.serial_connection.write(code_str.encode("utf-8"))
                print(f'Status: Code {code_str}')
            except Exception as e:
                self.statusLabel.setText('Status: Error sending serial code')
        else:
            self.statusLabel.setText('Status: No serial connection')

    # CONTROL SETTINGS WINDOW
    def openControlSettings(self):
        self.controlSettingsWindow = ControlSettingsWindow()
        self.controlSettingsWindow.show()

    # SERIAL READ WINDOW (will be removed)
    def openSerialReadWindow(self):
        if hasattr(self, 'serial_connection') and self.serial_connection.is_open:
            self.serialReadWindow = SerialReadWindow(self.serial_connection)
            self.serialReadWindow.show()
        else:
            self.statusLabel.setText('Status: No serial connection')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.retrieve_control_settings()
    sys.exit(app.exec_())
