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
from commands import Commands
from styles import Styles
from bluetooth_client import BluetoothClient
from multiplayer_controls_widget import MultiplayerControlsDevice2
from key_press_handler import KeyPressHandlerDevice2

class Device2Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize commands
        self.commands = Commands()

        # Initialize Bluetooth client
        self.bluetooth_client = BluetoothClient()

        # Initialize user interface
        self.init_UI()

        # Install event filter for keyboard events
        self.key_press_handler = KeyPressHandlerDevice2(
                self,
                self.bluetooth_client,
                self.commands
                )

        self.key_press_handler.installEventFilter(self)
        self.installEventFilter(self.key_press_handler)

        # Set up event connections
        self.set_up_event_connections()

        # Set window size
        width = 600 * Styles.SCALE_FACTOR
        height = 150 * Styles.SCALE_FACTOR
        self.resize(width, height)


    def init_UI(self):
        # Create and set central widget once
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create main layout
        self.mainLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        # Set window properties
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        self.setWindowIcon(QIcon(fr"{current_file_path}/brain.png"))
        self.setWindowTitle('Boccia T2S Controller: Device 2')
        self.setStyleSheet(Styles.WINDOW_BACKGROUND)

        # Create multiplayer controls widget
        self.multiplayer_controls_widget = MultiplayerControlsDevice2(self.bluetooth_client)
        self.multiplayer_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.mainLayout.addWidget(self.multiplayer_controls_widget)
    
    def set_up_event_connections(self):
        self.bluetooth_client.client_status_changed.connect(self.multiplayer_controls_widget._handle_client_status_change)