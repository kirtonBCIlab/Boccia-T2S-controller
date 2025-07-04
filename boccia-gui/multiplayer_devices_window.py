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
from multiplayer_controls_widget_secondary_devices import MultiplayerControlsSecondaryDevices
from multiplayer_instructions_widget import MultiplayerInstructionsWidget
from key_press_handler import KeyPressHandlerMultiplayer

class MultiplayerDevicesWindow(QMainWindow):
    """ Class for the main window of the app for the multiplayer devices.
    
    This class is for the app running on the other devices (the devices NOT connected to the ramp).
    """
    def __init__(self):
        """ Initializes the MultiplayerDevicesWindow class. """
        super().__init__()

        # Initialize instance of the Commands class
        self.commands = Commands()

        # Initialize instance of the Bluetooth client class
        self.bluetooth_client = BluetoothClient()

        # Initialize user interface
        self.init_UI()

        # Initialize key press handler
        # (Specifically the multiplayer key press handler)
        self.key_press_handler = KeyPressHandlerMultiplayer(
                self,
                self.bluetooth_client,
                self.commands
                )

        # Install event filter for keyboard events
        self.key_press_handler.installEventFilter(self)
        self.installEventFilter(self.key_press_handler)

        # Set up event connections
        self.set_up_event_connections()

        # Set window size
        width = 450 * Styles.SCALE_FACTOR
        height = 150 * Styles.SCALE_FACTOR
        self.resize(width, height)

    def init_UI(self):
        """ Initializes the user interface. """
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
        self.setWindowTitle('Boccia T2S Controller: Multiplayer App')
        self.setStyleSheet(Styles.WINDOW_BACKGROUND)

        # Create multiplayer controls widget
        self.multiplayer_controls_widget = MultiplayerControlsSecondaryDevices(self.bluetooth_client)
        self.multiplayer_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create instructions widget
        self.multiplayer_instructions_widget = MultiplayerInstructionsWidget()
        self.multiplayer_instructions_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Organize main layout
        self.mainLayout.addWidget(self.multiplayer_controls_widget)
        self.mainLayout.addWidget(self.multiplayer_instructions_widget)
    
    def set_up_event_connections(self):
        """ Sets up event connections. """
        # Connect the client status changed signal
        self.bluetooth_client.client_status_changed.connect(self.multiplayer_controls_widget._handle_client_status_change)