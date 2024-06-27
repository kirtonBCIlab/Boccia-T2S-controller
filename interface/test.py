import sys, serial, serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QComboBox, QGridLayout, QMainWindow, QAction
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


# Function to list available serial ports
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    available_ports = [port.device for port in ports]
    return available_ports

class ControlSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(400, 200)  # Set the default window size to 800x600


    def initUI(self):
        self.setWindowTitle('BCI Boccia Ramp Control - Settings')
        self.setStyleSheet("background-color: #2d2d2d; color: #ffffff;")
        
        # Layouts
        mainLayout = QHBoxLayout()  # Changed from QVBoxLayout to QHBoxLayout
        
        # Create the layouts for the user settings and control settings
        userSettingsLayout = QVBoxLayout()
        controlSettingsLayout = QVBoxLayout()
        font = QFont("Calibri")  # Replace "Arial" with the name of the font you want to use


        # Operator and User Controls
        operatorLabel = QLabel('Operator Controls')
        operatorLabel.setStyleSheet("QLabel { font: 20px Calibri; color: #b48ead;}")
        userLabel = QLabel('User Controls')
        userLabel.setStyleSheet("QLabel { font: 20px Calibri; color: #b48ead;}")
        
        # Control keys
        keysLayout = QGridLayout()
        leftLabel = QLabel('Left')
        leftComboBox = QComboBox()
        leftComboBox.addItems(['A', '<'])
        leftComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        
        rightLabel = QLabel('Right')
        rightComboBox = QComboBox()
        rightComboBox.addItems(['D', '>'])
        rightComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        
        upLabel = QLabel('Up')
        upComboBox = QComboBox()
        upComboBox.addItems(['W', '^'])
        upComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        
        downLabel = QLabel('Down')
        downComboBox = QComboBox()
        downComboBox.addItems(['S', 'v'])
        downComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        
        keysLayout.addWidget(leftLabel, 0, 0)
        keysLayout.addWidget(leftComboBox, 0, 1)
        keysLayout.addWidget(rightLabel, 1, 0)
        keysLayout.addWidget(rightComboBox, 1, 1)
        keysLayout.addWidget(upLabel, 2, 0)
        keysLayout.addWidget(upComboBox, 2, 1)
        keysLayout.addWidget(downLabel, 3, 0)
        keysLayout.addWidget(downComboBox, 3, 1)
        
        # User Commands
        userCommandsLayout = QGridLayout()
        commandALabel = QLabel('Command A')
        commandAComboBox = QComboBox()
        commandAComboBox.addItems(['A', 'W', 'D','S'])
        commandAComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        
        commandBLabel = QLabel('Command B')
        commandBComboBox = QComboBox()
        commandBComboBox.addItems(['W', 'D','S', 'A'])
        commandBComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        
        userCommandsLayout = QGridLayout()
        userCommandsLayout.addWidget(commandALabel, 0, 0)
        userCommandsLayout.addWidget(commandAComboBox, 0, 1)
        userCommandsLayout.addWidget(commandBLabel, 1, 0)
        userCommandsLayout.addWidget(commandBComboBox, 1, 1)
        
        userSettingsLayout.addWidget(operatorLabel)
        userSettingsLayout.addLayout(keysLayout)
        
        # Adding everything to the control settings layout
        controlSettingsLayout.addWidget(userLabel)
        controlSettingsLayout.addLayout(userCommandsLayout)
        
        # Adding user settings and control settings layouts to the main layout
        mainLayout.addLayout(userSettingsLayout)
        mainLayout.addLayout(controlSettingsLayout)
        
        self.setLayout(mainLayout)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_A:
            self.leftButton.click()  # Simulate a click on the left button
        elif key == Qt.Key_W:
            self.upButton.click()  # Simulate a click on the up button
        elif key == Qt.Key_D:
            self.rightButton.click()  # Simulate a click on the right button
        elif key == Qt.Key_S:
            self.downButton.click()  # Simulate a click on the down button

    def initUI(self):
        self.setWindowTitle('BCI Boccia Ramp Control')
        self.setStyleSheet("background-color: #2d2d2d; color: #ffffff;")
        
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        
        # Layouts
        mainLayout = QVBoxLayout()
        
        # Top right corner buttons layout
        topRightButtonsLayout = QHBoxLayout()
        
        # Connection Button
        self.connectButton = QPushButton('Connect')
        self.connectButton.setStyleSheet("font-size: 16px; background-color: green; color: #ffffff; padding: 5px; border: 1px solid #ffffff;")
        topRightButtonsLayout.addWidget(self.connectButton)  # Add the connect button first to align it to the left

        topRightButtonsLayout.addStretch()  # This will push the subsequent buttons to the right

        self.connectButton.clicked.connect(self.toggleConnection)
        self.connectButton.clicked.connect(self.connectSerialPort)

                
        # Calibration Button
        self.calibrationButton = QPushButton('Calibrate')
        self.calibrationButton.clicked.connect(self.sendCalibrationCode)
        self.calibrationButton.setStyleSheet("font-size: 16px; background-color: #3c3c3c; color: #ffffff; padding: 5px; border: 1px solid #ffffff;")
        topRightButtonsLayout.addWidget(self.calibrationButton)

        # Add the top right buttons layout to the main layout
        mainLayout.addLayout(topRightButtonsLayout)
        

        # Status
        statusLayout = QHBoxLayout()
        self.statusLabel = QLabel('Status: Disonnected')
        self.statusLabel.setStyleSheet("font-size: 16px; color: #a9a9a9;")

        # COM Port
        comLabel = QLabel('PORT')
        comLabel.setStyleSheet("font-size: 16px; color: #a9a9a9;")

        self.comComboBox = QComboBox()
        self.comComboBox.addItems(list_serial_ports())
        self.comComboBox.setStyleSheet("font-size: 16px; width: 70px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")

        statusLayout.addWidget(self.statusLabel)
        statusLayout.addStretch()
        statusLayout.addWidget(comLabel)
        statusLayout.addWidget(self.comComboBox)
        

        # Controls
        controlsLayout = QHBoxLayout()  
        speedLabel = QLabel('Speed')
        speedLabel.setStyleSheet("font-size: 16px; color: #2c2c2c;")
      
        
        heightLayout = QHBoxLayout()
        heightLabel = QLabel('Height Speed: ')
        heightLabel.setStyleSheet("QLabel { font: 20px Calibri; color: #b48ead;}")
        
        #Slider for height
        self.heightSlider = QSlider(Qt.Horizontal)
        self.heightSlider.setMinimum(0)
        self.heightSlider.setMaximum(100) #actual value = 255
        self.heightSlider.setValue(50)
        self.heightSlider.valueChanged.connect(self.updateHeightLabel)
        self.heightSlider.setStyleSheet("QSlider::groove:horizontal {background: #3c3c3c; height: 10px;}"
                                  "QSlider::handle:horizontal {background: #b48ead; width: 20px; margin: -5px 0;}")

        self.heightValueLabel = QLabel('50%')
        self.heightValueLabel.setStyleSheet("font-size: 16px; color: white;")
        
        heightLayout.addWidget(heightLabel)
        heightLayout.addWidget(self.heightSlider)
        heightLayout.addWidget(self.heightValueLabel)
        
        rotationLayout = QHBoxLayout()
        rotationLabel = QLabel('Rotation Speed: ')
        rotationLabel.setStyleSheet("QLabel { font: 20px Calibri; color: #b48ead;}")
        self.rotationSlider = QSlider(Qt.Horizontal)
        self.rotationSlider.setMinimum(0)
        self.rotationSlider.setMaximum(100) # actual value = 999
        self.rotationSlider.setValue(50)
        self.rotationSlider.valueChanged.connect(self.updateRotationLabel)
        self.rotationSlider.setStyleSheet("QSlider::groove:horizontal {background: #3c3c3c; height: 10px;}"
                                  "QSlider::handle:horizontal {background: #b48ead; width: 20px; margin: -5px 0;}")

        self.rotationValueLabel = QLabel('50%')
        self.rotationValueLabel.setStyleSheet("font-size: 16px; color: #ffffff;")

        rotationLayout.addWidget(rotationLabel)
        rotationLayout.addWidget(self.rotationSlider)
        rotationLayout.addWidget(self.rotationValueLabel)

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

        # Movement buttons
        buttonsLayout = QGridLayout()
        upButton = QPushButton('↑')
        #upButton.setStyleSheet("QPushButton { width: 50px; height: 50px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;}")
        downButton = QPushButton('↓')
        #downButton.setStyleSheet("QPushButton { width: 50px; height: 50px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;}")
        leftButton = QPushButton('←')
        #leftButton.setStyleSheet("QPushButton { width: 50px; height: 50px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;}")
        rightButton = QPushButton('→')
        #rightButton.setStyleSheet("QPushButton { width: 50px; height: 50px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;}")
        
        upButton.setStyleSheet(buttonStyle)
        downButton.setStyleSheet(buttonStyle)
        leftButton.setStyleSheet(buttonStyle)
        rightButton.setStyleSheet(buttonStyle)

        # Create a spacer item
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        buttonsLayout.addItem(spacer, 0, 3)

        # Create new layouts for buttons and sliders
        buttonsLayout = QGridLayout()
        slidersLayout = QVBoxLayout()

        # Add widgets to the new layouts
        buttonsLayout.addWidget(upButton, 0, 1)
        buttonsLayout.addWidget(downButton, 2, 1)
        buttonsLayout.addWidget(leftButton, 1, 0)
        buttonsLayout.addWidget(rightButton, 1, 2)

         # Assuming buttonsLayout is your grid layout and you want to adjust the first three columns
        buttonsLayout.setColumnStretch(0, 2)  # Makes the first column twice as wide as the others
        buttonsLayout.setColumnStretch(1, 2)  # Makes the second column twice as wide as the others
        buttonsLayout.setColumnStretch(2, 2)  # Makes the third column twice as wide as the others
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        buttonsLayout.addItem(spacer, 0, 3)

        # Create horizontal layout for height
        heightLayout = QHBoxLayout()
        heightLayout.addWidget(heightLabel)
        heightLayout.addWidget(self.heightValueLabel)
        slidersLayout.addLayout(heightLayout)
        slidersLayout.addWidget(self.heightSlider)

        rotationLayout = QHBoxLayout()
        rotationLayout.addWidget(rotationLabel)
        rotationLayout.addWidget(self.rotationValueLabel)
        slidersLayout.addLayout(rotationLayout)
        slidersLayout.addWidget(self.rotationSlider)

        # Add the new layouts to the main controls layout
        controlsLayout.addLayout(buttonsLayout)
        controlsLayout.addLayout(slidersLayout)
     
        
        # Settings Button
        settingsButton = QPushButton('Control Settings')
        settingsButton.setStyleSheet("font-size: 16px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        settingsButton.clicked.connect(self.openControlSettings)
        
        # Adding everything to the main layout
        mainLayout.addLayout(statusLayout)
        mainLayout.addWidget(controlsLabel)
        mainLayout.addLayout(controlsLayout)
        mainLayout.addWidget(speedLabel)
        mainLayout.addWidget(settingsButton)
        
        centralWidget.setLayout(mainLayout)

        # Assuming this line is where you need to use the selected COM port
        #selected_port = self.comComboBox.currentText()
        #self.serialConnection = serial.Serial(selected_port, 9600, timeout=1)
    
    def connectSerialPort(self):
        selected_port = self.comComboBox.currentText()
        if selected_port:
            try:
                self.serialConnection = serial.Serial(selected_port, 9600, timeout=1)
                self.statusLabel.setText('Status: Connected')
            except serial.SerialException as e:
                self.statusLabel.setText(f'Status: Error connecting to {selected_port}')
                print(f"Error connecting to {selected_port}: {e}")
            except PermissionError as e:
                self.statusLabel.setText(f'Status: Permission denied for {selected_port}')
                print(f"Permission denied for {selected_port}: {e}")
        else:
            self.statusLabel.setText('Status: Please select a COM port')
            print("Please select a COM port before connecting.")

        
    def updateHeightLabel(self, value):
        self.heightValueLabel.setText((f"{value}%"))
        self.heightValueLabel.setStyleSheet("font-size: 16px; color: white;")
          

    def updateRotationLabel(self, value):
        self.rotationValueLabel.setText((f"{value}%"))
        self.rotationValueLabel.setStyleSheet("font-size: 16px; color: white;")
        

    def openControlSettings(self):
        self.controlSettingsWindow = ControlSettingsWindow()
        self.controlSettingsWindow.show()



    def sendCalibrationCode(self):
        code = '8700'
        try:
            if self.serialConnection.isOpen():
                self.serialConnection.write(code.encode())
            else:
                # Attempt to open the serial port
                self.serialConnection.open()
                # Check again if the port is open and send the code
                if self.serialConnection.isOpen():
                    self.serialConnection.write(code.encode())
                else:
                    print("Failed to open serial port.")
        except serial.SerialException as e:
            print(f"Serial error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        # SEE IF NEEDED BASED ON SERIAL CODE
    def toggleConnection(self):
            # Toggle the button's text between 'Connect' and 'Disconnect'
            if self.connectButton.text() == 'Connect':
                self.connectButton.setText('Disconnect')
                self.connectButton.setStyleSheet("font-size: 16px; color: #ffffff; padding: 5px; border: 1px solid #ffffff;")
            else:
                self.connectButton.setText('Connect')
                self.connectButton.setStyleSheet("font-size: 16px; background-color: green; color: #ffffff; padding: 5px; border: 1px solid #ffffff;")
    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.resize(600, 400)
    mainWin.show()
    sys.exit(app.exec_())