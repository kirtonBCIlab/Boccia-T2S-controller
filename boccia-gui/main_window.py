import sys, serial, serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QComboBox, QGridLayout, QMainWindow, QAction
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

from control_settings_window import ControlSettingsWindow

# Function to list available serial ports
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    available_ports = [port.device for port in ports]
    return available_ports

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

        # Add the top right buttons layout to the main layout
        mainLayout.addLayout(topRightButtonsLayout)

        # Status
        statusLayout = QHBoxLayout()
        self.statusLabel = QLabel('Status: Disconnected')
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
        
        # Slider for height
        self.heightSlider = QSlider(Qt.Horizontal)
        self.heightSlider.setMinimum(0)
        self.heightSlider.setMaximum(100) # actual value = 255
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
        
        rotationLayout = QHBoxLayout()
        rotationLabel = QLabel('Rotation Speed: ')
        rotationLabel.setStyleSheet("QLabel { font: 20px Calibri; color: #b48ead;}")
        self.rotationSlider = QSlider(Qt.Horizontal)
        self.rotationSlider.setMinimum(0)
        self.rotationSlider.setMaximum(100) # actual value = 999
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
        # upButton.setStyleSheet("QPushButton { width: 50px; height: 50px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;}")
        downButton = QPushButton('↓')
        # downButton.setStyleSheet("QPushButton { width: 50px; height: 50px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;}")
        leftButton = QPushButton('←')
        # leftButton.setStyleSheet("QPushButton { width: 50px; height: 50px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;}")
        rightButton = QPushButton('→')
        # rightButton.setStyleSheet("QPushButton { width: 50px; height: 50px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;}")

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

        # Adding everything to the main layout
        mainLayout.addLayout(statusLayout)
        mainLayout.addWidget(controlsLabel)
        mainLayout.addLayout(controlsLayout)
        mainLayout.addWidget(speedLabel)
        mainLayout.addWidget(settingsButton)

        centralWidget.setLayout(mainLayout)

    def updateHeightLabel(self):
        value = self.heightSlider.value()
        self.heightValueLabel.setText(f'{value}%')

    def updateRotationLabel(self):
        value = self.rotationSlider.value()
        self.rotationValueLabel.setText(f'{value}%')

    def toggleConnection(self):
        if self.connectButton.text() == 'Connect':
            self.connectButton.setText('Disconnect')
            self.connectButton.setStyleSheet("font-size: 16px; background-color: red; color: #ffffff; padding: 5px; border: 1px solid #ffffff;")
            self.statusLabel.setText('Status: Connected')
        else:
            self.connectButton.setText('Connect')
            self.connectButton.setStyleSheet("font-size: 16px; background-color: green; color: #ffffff; padding: 5px; border: 1px solid #ffffff;")
            self.statusLabel.setText('Status: Disconnected')
            
    def connectSerialPort(self):
        port = self.comComboBox.currentText()
        try:
            self.serial_connection = serial.Serial(port, 9600, timeout=1)
            self.statusLabel.setText('Status: Connected')
        except Exception as e:
            self.statusLabel.setText(f'Status: Failed to connect')

    def sendCalibrationCode(self):
        if hasattr(self, 'serial_connection') and self.serial_connection.is_open:
            try:
                self.serial_connection.write(b'8700\n')
            except Exception as e:
                self.statusLabel.setText(f'Status: Error sending calibration code')
        else:
            self.statusLabel.setText('Status: No serial connection')

    def sendRotationValue(self):
        if hasattr(self, 'serial_connection') and self.serial_connection.is_open:
            value = ((self.rotationSlider.value())/100) * 1000
            serial_value = f'{value:03d}\n'.encode()
            try:
                self.serial_connection.write(serial_value)
            except Exception as e:
                self.statusLabel.setText(f'Status: Error sending rotation value')
        else:
            self.statusLabel.setText('Status: No serial connection')

    def sendHeightValue(self):
        if hasattr(self, 'serial_connection') and self.serial_connection.is_open:
            value = ((self.heightSlider.value())/100) * 255
            serial_value = f'{value:03d}\n'.encode()
            try:
                self.serial_connection.write(serial_value)
            except Exception as e:
                self.statusLabel.setText(f'Status: Error sending height value')
        else:
            self.statusLabel.setText('Status: No serial connection')


    def openControlSettings(self):
        self.controlSettingsWindow = ControlSettingsWindow()
        self.controlSettingsWindow.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
