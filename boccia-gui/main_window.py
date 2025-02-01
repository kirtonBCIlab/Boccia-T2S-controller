# Standard libraries
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMainWindow,
    QSizePolicy,
)

# Custom libraries
from styles import Styles
from serial_handler import SerialHandler
from key_press_handler import KeyPressHandler
from user_controls_widget import UserControlsWidget
from serial_controls_widget import SerialControlsWidget
from operator_controls_widget import OperatorControlsWidget
from help_widget import HelpWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()        

        # Initialize serial handler
        self.serial_handler = SerialHandler()

        # Initialize user interface
        self.init_UI()

        # Install event filter for keyboard events
        self.key_press_handler = KeyPressHandler(self.serial_handler)
        self.key_press_handler.installEventFilter(self)
        self.installEventFilter(self.key_press_handler)


    def init_UI(self):
         # Create and set central widget once
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Create main layout
        self.mainLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        # Set window properties
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        self.setWindowIcon(QIcon(fr"{current_file_path}/brain.png"))
        self.setWindowTitle('BCI Ramp Controls')
        self.setStyleSheet(Styles.WINDOW_BACKGROUND)

        # Create help widget
        self.help_widget = HelpWidget()
        self.help_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Create serial controls widget
        self.serial_controls_widget = SerialControlsWidget(self, self.serial_handler)
        self.serial_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Create operator controls
        self.operator_controls_widget = OperatorControlsWidget(self.serial_handler)
        self.operator_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create user controls
        self.user_controls_widget = UserControlsWidget(self.serial_handler)
        self.user_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 

        # Organize main layout
        self.mainLayout.addWidget(self.help_widget)
        self.mainLayout.addWidget(self.serial_controls_widget)
        self.mainLayout.addWidget(self.operator_controls_widget)
        self.mainLayout.addWidget(self.user_controls_widget)


    def closeEvent(self, event):
        # Safely disconnect from serial port
        if self.serial_handler.get_current_connection_status() == "Connected":
            self.serial_handler.disconnect()

        event.accept()