
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QSlider, QComboBox, QGridLayout, QMainWindow, QDialog, QSpacerItem, 
    QSizePolicy, QFrame, QScrollArea
)
from operator_controls_widget import OperatorControlsWidget
from serial_controls_widget import SerialControlsWidget
from user_controls_widget import UserControlsWidget
from serial_handler import SerialHandler
from styles import Styles


# # Function to list available serial ports


# # Serial Read Thread
# class SerialReadThread(QThread):
#     newData = pyqtSignal(str)

#     def __init__(self, serial_connection):
#         super().__init__()
#         self.serial_connection = serial_connection
#         self.running = True

#     def run(self):
#         while self.running:
#             if self.serial_connection.in_waiting > 0:
#                 data = self.serial_connection.read(self.serial_connection.in_waiting).decode('utf-8')
#                 self.newData.emit(data)

#     def stop(self):
#         self.running = False
#         self.wait()

# class SerialReadWindow(QDialog):
#     def __init__(self, serial_connection):
#         super().__init__()
#         self.serial_connection = serial_connection
#         self.serial_buffer = ""
#         self.initUI()

#     def initUI(self):
#         self.scroll = QScrollArea()
#         self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
#         self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

#         self.setWindowTitle('Serial Port Reader')
#         self.setGeometry(100, 100, 400, 300)

#         layout = QVBoxLayout()

#         self.outputLabel = QLabel('Reading data from serial port\n')
#         self.outputLabel.setWordWrap(True)  # Ensure text wraps within the label
#         self.scroll.setWidget(self.outputLabel)
#         self.scroll.setWidgetResizable(True)  

#         layout.addWidget(self.scroll)
#         self.setLayout(layout)

#         self.thread = SerialReadThread(self.serial_connection)
#         self.thread.newData.connect(self.updateOutput)
#         self.thread.start()

#     # Buggy
#     def updateOutput(self, data):
#         self.serial_buffer += data  # Append incoming data to the buffer
#         while '\n' in self.serial_buffer:  # Check for complete lines
#             line, self.serial_buffer = self.serial_buffer.split('\n', 1)
#             line = line.strip()  # Remove leading and trailing whitespace
#             print(line)  # Prints to terminal
#             self.outputLabel.setText(self.outputLabel.text() + line + '\n')


#     def closeEvent(self, event):
#         self.thread.stop()
#         event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # General settings
        self.calibration_options = {
            "Full": "dd-70>rc>ec",
            "Drop": "dd-70",
            'Rotation': "rc0",
            "Elevation - manual": "ec0",
            "Elevation - auto": "ec1",
        }

        self.command_mapping = {
            "elevation_up": "es1",
            "elevation_down": "es0",
            "rotation_left": "rs0",
            "rotation_right": "rs1",
            "drop": "dd-70"
        }

        self.user_commands = {
            Qt.Key_1: self.command_mapping["elevation_up"],
            Qt.Key_2: self.command_mapping["rotation_right"],
            Qt.Key_3: self.command_mapping["drop"],
            Qt.Key_R: self.command_mapping["drop"]
        }

        self.operator_commands = {
            Qt.Key_W: self.command_mapping["elevation_up"],
            Qt.Key_S: self.command_mapping["elevation_down"],
            Qt.Key_A: self.command_mapping["rotation_left"],
            Qt.Key_D: self.command_mapping["rotation_right"],
        }

        # Initialize serial handler
        self.serial_handler = SerialHandler()

        # Initialize user interface
        self.init_UI()


    def init_UI(self):
         # Create and set central widget once
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Create main layout
        self.mainLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        # Set window properties
        self.setWindowIcon(QIcon(r"brain.png"))
        self.setWindowTitle('BCI Ramp Controls')
        self.setStyleSheet(Styles.WINDOW_BACKGROUND)

        # Create serial controls widget
        self.serial_controls_widget = SerialControlsWidget(self)
        self.serial_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Create operator controls
        self.operator_controls_widget = OperatorControlsWidget()
        self.operator_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create user controls
        self.user_controls_widget = UserControlsWidget()
        self.user_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 

        # Organize main layout
        self.mainLayout.addWidget(self.serial_controls_widget)
        self.mainLayout.addWidget(self.operator_controls_widget)
        self.mainLayout.addWidget(self.user_controls_widget)
        


    #     # Default Serial Commands
    #     self.key_processed = False
    #     self.calibration_options = {
    #         "Full": "dd-70>rc>ec",
    #         "Drop": "dd-70",
    #         'Rotation': "rc0",
    #         "Elevation - manual": "ec0",
    #         "Elevation - auto": "ec1",
    #     }
    #     self.calibrationCommand = self.calibration_options["Full"]	# Default calibration command

    #     self.hold_commands = {
    #         Qt.Key_A: "rs0", # Rotation left
    #         Qt.Key_D: "rs1", # Rotation right
    #         Qt.Key_S: "es0", # Elevation down
    #         Qt.Key_W: "es1", # Elevation up
    #     }

    #     self.toggle_commands = {
    #         Qt.Key_1: "es1",    # Elevation up
    #         Qt.Key_2: "dd-70",  # Drop
    #         Qt.Key_3: "rs1",    # Rotation right   
    #         Qt.Key_R: "dd-70"   # Drop
    #     }

    #     # Create UI window
    #     self.initUI()
    #     self.resize(500, 400)

    # def keyPressEvent(self, event):
    #     if not event.isAutoRepeat():
    #         key = event.key()
            
    #         if (key in self.hold_commands) and (not self.key_processed):
    #             print(f"Operator key pressed: {key}")
    #             command = self.hold_commands[key]
    #             self.sendSerialCode(command)
    #             self.key_processed = True
    #             print(f"Sent press command: {command} to serial port\n")

    #         elif key in self.toggle_commands:
    #             print(f"User key pressed: {key}")
    #             command = self.toggle_commands[key]
    #             self.sendSerialCode(command)
    #             print(f"Sent press command: {command} to serial port\n")
                
    #         event.accept()

    
    # def keyReleaseEvent(self, event):
    #     if not event.isAutoRepeat():
    #         key = event.key()
    #         if (key in self.hold_commands) and (self.key_processed):
    #             print(f"Key released: {key}")
    #             command = self.hold_commands[key]
    #             self.sendSerialCode(command)
    #             self.key_processed = False
    #             print(f"Sent release command: {command} to serial port\n")


    def initUI(self):
        
        ## Rotation speeds as percentages
        self.default_speeds = {
            'rotation': 50,
            'elevation': 50
        }

        self.setWindowIcon(QIcon(r'brain.png'))

        # title and styleimport os
        self.setWindowTitle('BCI Ramp Controls')
        self.setStyleSheet("background-color: #2d2d2d; color: #ffffff;")
        
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        
        # Layouts
        mainLayout = QVBoxLayout()
        buttonsLayout = QGridLayout()
        topRightButtonsLayout = QHBoxLayout()
        
        # Connect Button
        self.connectButton = QPushButton('Connect')
        self.connectButton.setStyleSheet("font-size: 16px; background-color: green; color: #ffffff; padding: 5px; border-radius: 5px; border: 1px solid #ffffff;")
        topRightButtonsLayout.addWidget(self.connectButton)
        topRightButtonsLayout.addStretch()
        self.connectButton.clicked.connect(self.toggleConnection)
        # self.connectButton.clicked.connect(self.connectSerialPort)
        

        # Calibration Drop down
        self.calibrationLabel = QLabel('Calibrate')
        self.calibrationLabel.setStyleSheet("font-size: 16px; color: #a9a9a9;")
        self.calibrationDropDown = QComboBox()
        self.calibrationDropDown.addItems(self.calibration_options.keys())
        self.calibrationDropDown.setStyleSheet("font-size: 16px; width: 130px; background-color: #3c3c3c; color: #ffffff; border-radius: 5px; border: 1px solid #ffffff; padding: 3px;")
        topRightButtonsLayout.addWidget(self.calibrationLabel)
        topRightButtonsLayout.addWidget(self.calibrationDropDown)
        mainLayout.addLayout(topRightButtonsLayout)

        def updateCommand():
            self.calibrationCommand = self.calibration_options[self.calibrationDropDown.currentText()]
        self.calibrationDropDown.currentTextChanged.connect(updateCommand)
        
        # Connection Status Label
        statusLayout = QHBoxLayout()
        self.statusLabel = QLabel('Status: Disconnected')
        self.statusLabel.setStyleSheet("font-size: 16px; color: #a9a9a9;")

        # Port Selection Label and ComboBox
        comLabel = QLabel('PORT')
        comLabel.setStyleSheet("font-size: 16px; color: #a9a9a9;")

        self.comComboBox = QComboBox()
        self.comComboBox.addItems(list_serial_ports())
        self.comComboBox.setStyleSheet("font-size: 16px; width: 70px; background-color: #3c3c3c; color: #ffffff; border-radius: 5px; border: 1px solid #ffffff; padding: 3px;")

        
        statusLayout.addWidget(self.statusLabel)
        statusLayout.addStretch()
        statusLayout.addWidget(comLabel)
        statusLayout.addWidget(self.comComboBox)
        



        
    # USER CONTROLS  -------------------------  
        userLabel = QLabel('USER CONTROLS')
        userLabel.setStyleSheet("QLabel { font: 20px Calibri; color: #b48ead; font-weight: bold;}")

        userCommandsLayout = QGridLayout()
        commandALabel = QLabel('(1) Command A')
        commandALabel.setStyleSheet("QLabel { font: 20px Calibri; color: white;}")
        self.elevationBox = QPushButton('Elevation')
        self.elevationBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border-radius: 5px; border: 1px solid #ffffff; padding: 2px;")
        self.elevationBox.setEnabled(False)
        
        commandBLabel = QLabel('(2) Command B')
        commandBLabel.setStyleSheet("QLabel { font: 20px Calibri; color: white;}")
        self.dropBox = QPushButton('Drop')      
        self.dropBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border-radius: 5px; border: 1px solid #ffffff; padding: 2px;")
        self.dropBox.setEnabled(False)
        
        commandCLabel = QLabel('(3) Command C')
        commandCLabel.setStyleSheet("QLabel { font: 20px Calibri; color: white;}")
        self.rotationBox = QPushButton('Rotation')
        self.rotationBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border-radius: 5px; border: 1px solid #ffffff; padding: 2px;")
        self.rotationBox.setEnabled(False)

        userCommandsLayout.addWidget(commandALabel, 0, 0)
        userCommandsLayout.addWidget(self.elevationBox, 0, 1)
        userCommandsLayout.addWidget(commandBLabel, 1, 0)
        userCommandsLayout.addWidget(self.dropBox, 1, 1)
        userCommandsLayout.addWidget(commandCLabel, 2, 0)
        userCommandsLayout.addWidget(self.rotationBox, 2, 1)

        calibrateButton = QPushButton('Calibrate')
        calibrateButton.setStyleSheet("""
                                        QPushButton {
                                            font-size: 16px;
                                            background-color: #3c3c3c;
                                            color: #ffffff;
                                            border: 1px solid #ffffff;
                                            border-radius: 5px;
                                            padding: 3px;
                                        }
                                        QPushButton:hover {
                                            background-color: #555555;
                                        }
                                    """)
        calibrateButton.clicked.connect(lambda: self.sendSerialCode(self.calibrationCommand))

        serialReadButton = QPushButton('Read Serial')
        serialReadButton.setStyleSheet("""
                                        QPushButton {
                                            font-size: 16px;
                                            background-color: #3c3c3c;
                                            color: #ffffff;
                                            border: 1px solid #ffffff;
                                            border-radius: 5px;
                                            padding: 3px;
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
        mainLayout.addWidget(userLabel)
        mainLayout.addLayout(userCommandsLayout)

        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        mainLayout.addItem(spacer)

        mainLayout.addWidget(calibrateButton)
        mainLayout.addWidget(serialReadButton)
        centralWidget.setLayout(mainLayout)

        mainLayout.setContentsMargins(20, 20, 20, 20)  # left, top, right, bottom

    

 # FUNCTIONS ----------------------------------------

#     def on_combobox_changed(self):
#         self.send_button.setStyleSheet("""
#                                     QPushButton {
#                                         font-size: 16px;
#                                         background-color: green;
#                                         color: #ffffff;
#                                         border: 1px solid #ffffff;
#                                         border-radius: 5px;
#                                         padding: 3px;
#                                     }
#                                     QPushButton:hover {
#                                         background-color: #555555;
#                                     }
#                                 """)
#         self.is_green = True  # Set the flag to indicate the button is green

#     def on_button_clicked(self):
#         if self.is_green:
#             self.send_button.setStyleSheet("""
#                                             QPushButton {
#                                                 font-size: 16px;
#                                                 background-color: #3c3c3c;
#                                                 color: #ffffff;
#                                                 border: 1px solid #ffffff;
#                                                 border-radius: 5px;
#                                                 padding: 3px;
#                                             }
#                                             QPushButton:hover {
#                                                 background-color: #555555;
#                                             }
#                                         """)
#             self.is_green = False  # Reset the flag
#         else:
#             self.send_button.setStyleSheet("""
#                                             QPushButton {
#                                                 font-size: 16px;
#                                                 background-color: green;
#                                                 color: #ffffff;
#                                                 border: 1px solid #ffffff;
#                                                 border-radius: 5px;
#                                                 padding: 3px;
#                                             }
#                                             QPushButton:hover {
#                                                 background-color: #555555;
#                                             }
#                                         """)
#             self.is_green = True  # Set the flag

#     # Update the height label
#     def updateHeightLabel(self):
#         value = self.heightSlider.value()
#         self.heightValueLabel.setText(f'{value}%')

#     # Update the rotation label
#     def updateRotationLabel(self):
#         value = self.rotationSlider.value()
#         self.rotationValueLabel.setText(f'{value}%')

#     # Toggle the connection status
#     def toggleConnection(self):
#         if self.connectButton.text() == 'Connect':
#             self.connectButton.setText('Disconnect')
#             self.connectButton.setStyleSheet("font-size: 16px; background-color: red; color: #ffffff; border-radius: 5px; padding: 5px; border: 1px solid #ffffff;")
#             self.comComboBox.setEnabled(False)
#             self.connectSerialPort()

#             # self.setElevationSpeed()
#             # self.setRotationSpeed()
#             ## Wait 100 msec and then set the speeds
#             # QTimer.singleShot(100, self.setElevationSpeed)
#             # QTimer.singleShot(10, self.setRotationSpeed)
#         else:
#             self.connectButton.setText('Connect')
#             self.connectButton.setStyleSheet("font-size: 16px; background-color: green; color: #ffffff; border-radius: 5px; padding: 5px; border: 1px solid #ffffff;")
#             self.statusLabel.setText('Status: Disconnected')
#             self.comComboBox.setEnabled(True)
#             self.disconnectSerialPort()
            
#     # Connect to the selected serial port
#     def connectSerialPort(self):
#         port = self.comComboBox.currentText()
#         try:
#             self.serial_connection = serial.Serial(port, 9600, timeout=1)
#             self.statusLabel.setText('Status: Connected')
#         except Exception as e:
#             self.statusLabel.setText(f'Status: Disconnected')

#     def disconnectSerialPort(self):
#         if hasattr(self, 'serial_connection') and self.serial_connection.is_open:
#             self.serial_connection.close()
#             self.statusLabel.setText('Status: Disconnected')
#         else:
#             self.statusLabel.setText('Status: No connection to disconnect')

#     # Caclulate and send the Rotation slider value 
#     def setRotationSpeed(self):
#         if hasattr(self, 'serial_connection') and self.serial_connection.is_open:
#             value = int(((self.rotationSlider.value()) / 100) * 1000)
#             serial_command = "rx" + str(value) + "\n"
            
#             try:
#                 self.serial_connection.write(serial_command.encode("utf-8"))
#             except Exception as e:
#                 self.statusLabel.setText(f'Status: Error sending rotation value')
#         else:
#             self.statusLabel.setText('Status: No serial connection')

#     # Caclulate and send the Rotation slider value 
#     def setElevationSpeed(self):
#         if hasattr(self, 'serial_connection') and self.serial_connection.is_open:
#             value = int((self.heightSlider.value() / 100) * 255)
#             serial_command = "ex" + str(value) + "\n"

#             try:
#                 self.serial_connection.write(serial_command.encode("utf-8"))
#             except Exception as e:
#                 self.statusLabel.setText(f'Status: Error sending height value')
#         else:
#             self.statusLabel.setText('Status: No serial connection')

# # SEND SERIAL CODE FUNCTION
#     def sendSerialCode(self, code):
#         if hasattr(self, 'serial_connection') and self.serial_connection.is_open:
#             try:
#                 code_str = str(code) + "\n"
#                 self.serial_connection.write(code_str.encode("utf-8"))
#                 print(f'Status: Code {code_str}\n')
#             except Exception as e:
#                 self.statusLabel.setText('Status: Error sending serial code')
#         else:
#             self.statusLabel.setText('Status: No serial connection')

# # SERIAL READ WINDOW (will be removed)
#     def openSerialReadWindow(self):
#         self.scroll = QScrollArea()    
#         if hasattr(self, 'serial_connection') and self.serial_connection.is_open:
#             self.serialReadWindow = SerialReadWindow(self.serial_connection)
#             self.serialReadWindow.show()
#         else:
#             self.statusLabel.setText('Status: No serial connection')

