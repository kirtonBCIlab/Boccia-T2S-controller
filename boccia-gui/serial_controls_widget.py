# Import libraries
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QPushButton

class SerialConnectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        self.statusLabel = QLabel('Status: Disconnected')
        self.statusLabel.setStyleSheet("font-size: 16px; color: #a9a9a9;")

        comLabel = QLabel('PORT')
        comLabel.setStyleSheet("font-size: 16px; color: #a9a9a9;")

        self.comComboBox = QComboBox()
        self.comComboBox.setStyleSheet("font-size: 16px; width: 70px; background-color: #3c3c3c; color: #ffffff; border-radius: 5px; border: 1px solid #ffffff; padding: 3px;")

        self.connectButton = QPushButton('Connect')
        self.connectButton.setStyleSheet("font-size: 16px; background-color: green; color: #ffffff; padding: 5px; border-radius: 5px; border: 1px solid #ffffff;")

        layout.addWidget(self.statusLabel)
        layout.addStretch()
        layout.addWidget(comLabel)
        layout.addWidget(self.comComboBox)
        layout.addWidget(self.connectButton)

        self.setLayout(layout)