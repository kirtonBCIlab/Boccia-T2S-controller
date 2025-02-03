
# Standard libraries
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
from user_controls_widget import UserControlsWidget
from serial_controls_widget import SerialControlsWidget
from operator_controls_widget import OperatorControlsWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()        

        # Initialize serial handler
        self.serial_handler = SerialHandler()

        # Initialize commands
        self.commands = Commands()

        # Initialize user interface
        self.init_UI()

        # Install event filter for keyboard events
        self.key_press_handler = KeyPressHandler(self.serial_handler, self.commands)
        self.key_press_handler.installEventFilter(self)
        self.installEventFilter(self.key_press_handler)
        self.commands.set_key_press_handler(self.key_press_handler)

        self.set_up_event_connections()


    def init_UI(self):
         # Create and set central widget once
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Create main layout
        self.mainLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        # Set window properties
        self.setWindowIcon(QIcon(r"brain.png"))
        self.setWindowTitle('BCI Ramp Controls')
        self.setStyleSheet(Styles.WINDOW_BACKGROUND)

        # Create serial controls widget
        self.serial_controls_widget = SerialControlsWidget(self, self.serial_handler)
        self.serial_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Create operator controls
        self.operator_controls_widget = OperatorControlsWidget(self.serial_handler)
        self.operator_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create user controls
        self.user_controls_widget = UserControlsWidget(self.serial_handler, self.commands)
        self.user_controls_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.commands.set_user_controls_widget(self.user_controls_widget) 

        # Organize main layout
        self.mainLayout.addWidget(self.serial_controls_widget)
        self.mainLayout.addWidget(self.operator_controls_widget)
        self.mainLayout.addWidget(self.user_controls_widget)


    def set_up_event_connections(self):
        self.key_press_handler.key_service_flag_changed.connect(self.user_controls_widget._on_key_toggled)
        self.user_controls_widget.button_service_flag_changed.connect(self.key_press_handler.toggle_service_flag)


    def closeEvent(self, event):
        # Safely disconnect from serial port
        if self.serial_handler.get_current_connection_status() == "Connected":
            self.serial_handler.disconnect()

        event.accept()