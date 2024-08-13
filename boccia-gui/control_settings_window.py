from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QFont


class ControlSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(400, 200)  # Set the default window size to 800x600
        self.settings = {}

        
        # Initialize instance variables to store selected values
        self.leftKey = None
        self.rightKey = None
        self.upKey = None
        self.downKey = None
        self.commandA = None
        self.commandB = None

    def get_selected_settings(self):
        # Return the current settings
        return self.settings

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
        self.leftComboBox = QComboBox()
        self.leftComboBox.addItems(['A', '<'])
        self.leftComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        self.leftComboBox.currentIndexChanged.connect(self.updateLeftKey)
        
        rightLabel = QLabel('Right')
        self.rightComboBox = QComboBox()
        self.rightComboBox.addItems(['D', '>'])
        self.rightComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        self.rightComboBox.currentIndexChanged.connect(self.updateRightKey)
        
        upLabel = QLabel('Up')
        self.upComboBox = QComboBox()
        self.upComboBox.addItems(['W', '^'])
        self.upComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        self.upComboBox.currentIndexChanged.connect(self.updateUpKey)
        
        downLabel = QLabel('Down')
        self.downComboBox = QComboBox()
        self.downComboBox.addItems(['S', 'v'])
        self.downComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        self.downComboBox.currentIndexChanged.connect(self.updateDownKey)
        
        keysLayout.addWidget(leftLabel, 0, 0)
        keysLayout.addWidget(self.leftComboBox, 0, 1)
        keysLayout.addWidget(rightLabel, 1, 0)
        keysLayout.addWidget(self.rightComboBox, 1, 1)
        keysLayout.addWidget(upLabel, 2, 0)
        keysLayout.addWidget(self.upComboBox, 2, 1)
        keysLayout.addWidget(downLabel, 3, 0)
        keysLayout.addWidget(self.downComboBox, 3, 1)
        
        # User Commands
        userCommandsLayout = QGridLayout()
        commandALabel = QLabel('Command A')
        self.commandAComboBox = QComboBox()
        self.commandAComboBox.addItems(['A', 'W', 'D','S'])
        self.commandAComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        
        commandBLabel = QLabel('Command B')
        self.commandBComboBox = QComboBox()
        self.commandBComboBox.addItems(['W', 'D','S', 'A'])
        self.commandBComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        
        userCommandsLayout = QGridLayout()
        userCommandsLayout.addWidget(commandALabel, 0, 0)
        userCommandsLayout.addWidget(self.commandAComboBox, 0, 1)
        userCommandsLayout.addWidget(commandBLabel, 1, 0)
        userCommandsLayout.addWidget(self.commandBComboBox, 1, 1)
        
        userSettingsLayout.addWidget(operatorLabel)
        userSettingsLayout.addLayout(keysLayout)
        
        # Adding everything to the control settings layout
        controlSettingsLayout.addWidget(userLabel)
        controlSettingsLayout.addLayout(userCommandsLayout)
        
        # Adding user settings and control settings layouts to the main layout
        mainLayout.addLayout(userSettingsLayout)
        mainLayout.addLayout(controlSettingsLayout)
        
        self.setLayout(mainLayout)

        
    # Slots to update instance variables
    def updateLeftKey(self):
        self.leftKey = self.leftComboBox.currentText()
        print(f"Left key selected: {self.leftKey}")

    def updateRightKey(self):
        self.rightKey = self.rightComboBox.currentText()
        print(f"Right key selected: {self.rightKey}")

    def updateUpKey(self):
        self.upKey = self.upComboBox.currentText()
        print(f"Up key selected: {self.upKey}")

    def updateDownKey(self):
        self.downKey = self.downComboBox.currentText()
        print(f"Down key selected: {self.downKey}")
    
    def updateCommandA(self):
        self.commandA = self.commandAComboBox.currentText()
        print(f"Command A selected: {self.commandA}")

    def updateCommandB(self):
        self.commandB = self.commandBComboBox.currentText()
        print(f"Command B selected: {self.commandB}")

