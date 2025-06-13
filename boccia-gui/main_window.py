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
from serial_handler import SerialHandler
from key_press_handler import KeyPressHandler
from bluetooth_server import BluetoothServer
from user_controls_widget import UserControlsWidget
from serial_controls_widget import SerialControlsWidget
from operator_controls_widget import OperatorControlsWidget
from multiplayer_controls_widget_main_device import MultiplayerControlsMainDevice


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()        

        # Initialize serial handler
        self.serial_handler = SerialHandler()

        # Initialize commands
        self.commands = Commands()

        # Initialize bluetooth classes
        self.bluetooth_server = BluetoothServer()

        # Initialize user interface
        self.init_UI()

        # Install event filter for keyboard events
        self.key_press_handler = KeyPressHandler(
               self,
               self.serial_handler, 
               self.commands
               )
        
        self.key_press_handler.installEventFilter(self)
        self.installEventFilter(self.key_press_handler)
        self.commands.set_key_press_handler(self.key_press_handler)

        # Set up event connections
        self.set_up_event_connections()

        # Set window size
        width = 600 * Styles.SCALE_FACTOR
        height = 400 * Styles.SCALE_FACTOR
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
        self.setWindowTitle('Boccia T2S Controller')
        self.setStyleSheet(Styles.WINDOW_BACKGROUND)

        # Create serial controls widget
        self.serial_controls_widget = SerialControlsWidget(self, self.serial_handler)
        self.serial_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Create multiplayer controls widget
        self.multiplayer_controls_widget = MultiplayerControlsMainDevice(self.bluetooth_server)
        self.multiplayer_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Create operator controls
        self.operator_controls_widget = OperatorControlsWidget(self.serial_handler, self.commands)
        self.operator_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.commands.set_operator_controls_widget(self.operator_controls_widget)

        # Create user controls
        self.user_controls_widget = UserControlsWidget(self.serial_handler, self.commands)
        self.user_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.commands.set_user_controls_widget(self.user_controls_widget) 

        # Organize main layout
        self.mainLayout.addWidget(self.serial_controls_widget)
        self.mainLayout.addWidget(self.multiplayer_controls_widget)
        self.mainLayout.addWidget(self.operator_controls_widget)
        self.mainLayout.addWidget(self.user_controls_widget)


    def set_up_event_connections(self):
        # KeyPressHandler sends service flag
        self.key_press_handler.key_service_flag_changed.connect(self.user_controls_widget._receive_service_flag)
        self.key_press_handler.key_service_flag_changed.connect(self.operator_controls_widget._receive_service_flag)

        # UserControlsWidget sends service flag  
        self.user_controls_widget.button_service_flag_changed.connect(self.key_press_handler.toggle_service_flag)
        self.user_controls_widget.button_service_flag_changed.connect(self.operator_controls_widget._receive_service_flag)

         # OperatorControlsWidget sends service flag
        self.operator_controls_widget.hold_button_service_flag_changed.connect(self.key_press_handler.toggle_service_flag)
        self.operator_controls_widget.hold_button_service_flag_changed.connect(self.user_controls_widget._receive_service_flag)

        # Bluetooth server events
        self.bluetooth_server.server_status_changed.connect(self.multiplayer_controls_widget._handle_server_status_change)
        self.bluetooth_server.command_received.connect(self.command_received_from_multiplayer_device)

    def command_received_from_multiplayer_device(self, player_number, command_text):
        """ Handles a command received from a multiplayer device. """
        self.key_press_handler.toggle_key_pressed(player_number, command_text)

    def closeEvent(self, event):
        # Safely disconnect from serial port
        if self.serial_handler.get_current_connection_status() == "Connected":
            self.serial_handler.disconnect()

        event.accept()