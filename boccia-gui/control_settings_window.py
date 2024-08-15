from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QFont


class ControlSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(400, 200)  # Set the default window size to 400x200

        # Initialize instance variables to store selected values
        self.commandA = 'Elevation'
        self.commandB = 'Drop'

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
        commandALabel = QLabel('Command - 1')
        self.commandAComboBox = QComboBox()
        self.commandAComboBox.addItems(['Elevation', 'Rotation'])
        self.commandAComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        #self.commandAComboBox.currentIndexChanged.connect(self.updateCommandA)
        self.update_command()  # Initial command update
        self.commandAComboBox.currentIndexChanged.connect(self.update_command)

        commandBLabel = QLabel('Command - 2')
        self.commandBComboBox = QComboBox()
        self.commandBComboBox.addItems(['Drop'])
        self.commandBComboBox.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        # self.commandBComboBox.currentIndexChanged.connect(self.updateCommandB)
        self.update_command()  # Initial command update
        self.commandBComboBox.currentIndexChanged.connect(self.update_command)
        

        userCommandsLayout.addWidget(commandALabel, 0, 0)
        userCommandsLayout.addWidget(self.commandAComboBox, 0, 1)
        userCommandsLayout.addWidget(commandBLabel, 1, 0)
        userCommandsLayout.addWidget(self.commandBComboBox, 1, 1)

        # Save Button
        # saveButton = QPushButton('Save Settings')
        # saveButton.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #ffffff;")
        # saveButton.clicked.connect(self.saveSettings)

        # Adding everything to the control settings layout
        controlSettingsLayout.addWidget(userLabel)
        controlSettingsLayout.addLayout(userCommandsLayout)
        # controlSettingsLayout.addWidget(saveButton)  # Add the save button to the layout

        # Adding user settings and control settings layouts to the main layout
        mainLayout.addLayout(userSettingsLayout)
        mainLayout.addLayout(controlSettingsLayout)

        self.setLayout(mainLayout)


    def update_command(self):
        selected_text = self.commandAComboBox.currentText()

        if selected_text == "Rotation":
            self.commandA = '7120'
        elif selected_text == "Elevation":
            self.commandA = '7210'

        print(f"ControlSettingsWindow - Command A: {self.commandA}")
    
        if self.parent():
            self.parent().update_toggle_commands()

    #     # Slots to update instance variables
    # def updateCommandA(self):
    #     self.commandA = self.commandAComboBox.currentText()
    #     self.settings['commandA'] = self.commandA
    #     print(f"Command A selected: {self.commandA}")

    # def updateCommandB(self):
    #     self.commandB = self.commandBComboBox.currentText()
    #     self.settings['commandB'] = self.commandB
    #     print(f"Command B selected: {self.commandB}")

    # def get_selected_settings(self):
    #     print('SETTINGS', self.settings)
    #     return self.settings
        
    # def saveSettings(self):
    #     self.settings['commandA'] = self.commandAComboBox.currentText()
    #     self.settings['commandB'] = self.commandBComboBox.currentText()
    #     print(f"Settings saved: {self.settings}")

    
