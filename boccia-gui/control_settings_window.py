from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QFont


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

