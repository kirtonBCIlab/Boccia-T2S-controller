from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QFont


class ControlSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(400, 200)  # Set the default window size to 400x200
        self.settings = {}

        # Initialize instance variables to store selected values
        self.commandA = None
        self.commandB = None

    def get_selected_settings(self):
        # Return the current settings
        return self.settings

    def initUI(self):
        self.setWindowTitle('BCI Boccia Ramp Control - Settings')
        self.setStyleSheet("background-color: #2d2d2d; color: #ffffff;")
        
        # Layouts
        mainLayout = QHBoxLayout()
        
        # Create the layouts for the user settings and control settings
        userSettingsLayout = QVBoxLayout()
        controlSettingsLayout = QVBoxLayout()
        font = QFont("Calibri")

        # Operator and User Controls
        userLabel = QLabel('User Controls')
        userLabel.setStyleSheet("QLabel { font: 20px Calibri; color: #b48ead;}")

        # User Commands
        userCommandsLayout = QGridLayout()
        commandALabel = QLabel('Enter')
        self.commandAComboBox = QComboBox()
        self.commandAComboBox.addItems(['Rotation', 'Elevation'])
        self.commandAComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        self.commandAComboBox.currentIndexChanged.connect(self.updateCommandA)

        commandBLabel = QLabel('Space Bar')
        self.commandBComboBox = QComboBox()
        self.commandBComboBox.addItems(['Drop'])
        self.commandBComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        self.commandBComboBox.currentIndexChanged.connect(self.updateCommandB)

        userCommandsLayout.addWidget(commandALabel, 0, 0)
        userCommandsLayout.addWidget(self.commandAComboBox, 0, 1)
        userCommandsLayout.addWidget(commandBLabel, 1, 0)
        userCommandsLayout.addWidget(self.commandBComboBox, 1, 1)

        # Adding everything to the control settings layout
        controlSettingsLayout.addWidget(userLabel)
        controlSettingsLayout.addLayout(userCommandsLayout)

        # Adding user settings and control settings layouts to the main layout
        mainLayout.addLayout(userSettingsLayout)
        mainLayout.addLayout(controlSettingsLayout)

        self.setLayout(mainLayout)

    # Slots to update instance variables
    def updateCommandA(self):
        self.commandA = self.commandAComboBox.currentText()
        print(f"Command A selected: {self.commandA}")

    def updateCommandB(self):
        self.commandB = self.commandBComboBox.currentText()
        print(f"Command B selected: {self.commandB}")
