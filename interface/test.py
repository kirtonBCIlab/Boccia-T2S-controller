import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QComboBox, QGridLayout, QMainWindow, QAction
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ControlSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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
        commandAComboBox.addItems(['Up'])
        commandAComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        
        commandBLabel = QLabel('Command B')
        commandBComboBox = QComboBox()
        commandBComboBox.addItems(['Down'])
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
        
        # Status and COM port
        statusLayout = QHBoxLayout()
        statusLabel = QLabel('Status: connected')
        statusLabel.setStyleSheet("font-size: 16px; color: #a9a9a9;")
        comLabel = QLabel('COM PORT')
        comLabel.setStyleSheet("font-size: 16px; color: #a9a9a9;")
        comComboBox = QComboBox()
        comComboBox.addItems(['3', '4', '5'])
        comComboBox.setStyleSheet("font-size: 16px; width: 20px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        
        statusLayout.addWidget(statusLabel)
        statusLayout.addStretch()
        statusLayout.addWidget(comLabel)
        statusLayout.addWidget(comComboBox)
        

        # Controls
        controlsLayout = QHBoxLayout()  # Change this to QHBoxLayout
        speedLabel = QLabel('Speed')
        speedLabel.setStyleSheet("font-size: 16px; color: #2c2c2c;")
      
        heightLabel = QLabel('Height Speed')
        heightLabel.setStyleSheet("QLabel { font: 20px Calibri; color: #b48ead;}")
        heightSlider = QSlider(Qt.Horizontal)
        heightSlider.setValue(70)
        heightSlider.setStyleSheet("QSlider::groove:horizontal {background: #3c3c3c; height: 10px;}"
                                   "QSlider::handle:horizontal {background: #ffffff; width: 20px;}")
        
        rotationLabel = QLabel('Rotation Speed')
        rotationLabel.setStyleSheet("QLabel { font: 20px Calibri; color: #b48ead;}")
        rotationSlider = QSlider(Qt.Horizontal)
        rotationSlider.setValue(85)
        rotationSlider.setStyleSheet("QSlider::groove:horizontal {background: #3c3c3c; height: 10px;}"
                                     "QSlider::handle:horizontal {background: #ffffff; width: 20px;}")
        
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
        upButton = QPushButton('Up')
        #upButton.setStyleSheet("QPushButton { width: 50px; height: 50px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;}")
        downButton = QPushButton('Down')
        #downButton.setStyleSheet("QPushButton { width: 50px; height: 50px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;}")
        leftButton = QPushButton('Left')
        #leftButton.setStyleSheet("QPushButton { width: 50px; height: 50px; background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;}")
        rightButton = QPushButton('Right')
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

        slidersLayout.addWidget(heightLabel)
        slidersLayout.addWidget(heightSlider)
        slidersLayout.addWidget(rotationLabel)
        slidersLayout.addWidget(rotationSlider)

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

    def openControlSettings(self):
        self.controlSettingsWindow = ControlSettingsWindow()
        self.controlSettingsWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.resize(500, 400)
    mainWin.show()
    sys.exit(app.exec_())