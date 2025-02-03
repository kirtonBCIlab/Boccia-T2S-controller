# Import libraries
import webbrowser
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    )

# Custom libraries
from styles import Styles
from commands import Commands
from custom_combo_box import CustomComboBox
from serial_read_window import SerialReadWindow


class SerialControlsWidget(QWidget):
    HELP_URL = "https://github.com/kirtonBCIlab/Boccia-T2S-controller/wiki"

    def __init__(self, parent = None, serial_handler = None):
        super().__init__()
        
        # Get acces to serial handler object
        self.parent = parent
        self.serial_handler = serial_handler

        # Suscribe to external events
        self.serial_handler.connection_changed.connect(self._handle_connection_change)
        
        # Settings
        self.connect_button_styles = {
            "connect": Styles.create_button_style("green"),
            "disconnect": Styles.create_button_style("red"),
            "error": Styles.create_button_style("orange")
            }
    
        # Main label section
        self.main_label = QLabel('SERIAL CONNECTION')
        self.main_label.setStyleSheet(Styles.MAIN_LABEL)

        self.help_button = QPushButton("Help")
        self.help_button.setStyleSheet(Styles.HOVER_BUTTON)
        self.help_button.clicked.connect(self._open_help_url)

        self.main_label_layout = QHBoxLayout()
        self.main_label_layout.addWidget(self.main_label)
        self.main_label_layout.addStretch()
        self.main_label_layout.addWidget(self.help_button)
        
        
        # Content section
        self._create_connect_and_status_section()
        self._create_calibration_and_port_section()
        self._create_serial_actions()

        self.content_layout = QHBoxLayout()
        self.content_layout.addLayout(self.connection_section_layout)
        self.content_layout.addLayout(self.calibration_and_port_layout)

        # Organize layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.main_label_layout)
        self.main_layout.addLayout(self.content_layout)
        self.main_layout.addLayout(self.serial_actions_container)

    
    def toggle_read_serial(self):
        if self.read_serial_button.isEnabled():
            self.read_serial_button.setEnabled(False)
            self.read_serial_button.setStyleSheet(Styles.DISABLED_BUTTON)
        else:
            self.read_serial_button.setEnabled(True)
            self.read_serial_button.setStyleSheet(Styles.HOVER_BUTTON)


    def _create_connect_and_status_section(self):
        # Button section
        self.connect_button = QPushButton('Connect')
        self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
        self.connect_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.connect_button.setContentsMargins(5, 5, 5, 5)  # Add small padding around text
        self.connect_button.clicked.connect(self._toggle_connection_status)

        button_container = QHBoxLayout()
        button_container.addWidget(self.connect_button)
        button_container.addStretch()

        # Status section
        self.connection_status_label = QLabel('Status: Disconnected')
        self.connection_status_label.setStyleSheet(Styles.LABEL_TEXT)

        self.connection_section_layout = QVBoxLayout()
        self.connection_section_layout.addLayout(button_container)
        self.connection_section_layout.addWidget(self.connection_status_label)
       

    def _create_calibration_and_port_section(self):
        # Calibration selection
        self.calibration_label = QLabel('Calibrate')
        self.calibration_label.setStyleSheet(Styles.LABEL_TEXT)

        self.calibration_combo_box = QComboBox()
        self.calibration_combo_box.setStyleSheet( f"{Styles.COMBOBOX_BASE} width: 130px;")
        self.calibration_combo_box.addItems(Commands.CALIBRATION_COMMANDS.keys())

        self.calibration_section = QHBoxLayout()
        self.calibration_section.addWidget(self.calibration_label)
        self.calibration_section.addWidget(self.calibration_combo_box)

        # Port selection
        self.port_label = QLabel('COM Port')
        self.port_label.setStyleSheet(Styles.LABEL_TEXT)

        self.port_combo_box = CustomComboBox()
        self.port_combo_box.setStyleSheet( f"{Styles.COMBOBOX_BASE} width: 70px;")
        self._populate_ports()


        self.port_section = QHBoxLayout()
        self.port_section.addWidget(self.port_label)
        self.port_section.addWidget(self.port_combo_box)

        # Organize layout   
        self.calibration_and_port_layout = QVBoxLayout()
        self.calibration_and_port_layout.addLayout(self.calibration_section)
        self.calibration_and_port_layout.addLayout(self.port_section)


    def _create_serial_actions(self):
        # Calibrate button
        self.calibrate_button = QPushButton('Calibrate')
        self.calibrate_button.setStyleSheet(Styles.HOVER_BUTTON)
        self.calibrate_button.clicked.connect(self._send_calibration_command)
        self.calibrate_button.setEnabled(False)

        # Read serial button
        self.read_serial_button = QPushButton('Read serial')
        self.read_serial_button.setStyleSheet(Styles.HOVER_BUTTON)
        self.read_serial_button.clicked.connect(self._read_serial_data)
        self.read_serial_button.setEnabled(False)

        # Organize layout
        self.serial_actions_container = QVBoxLayout()
        self.serial_actions_container.addWidget(self.calibrate_button)
        self.serial_actions_container.addWidget(self.read_serial_button)
        

    def _toggle_connection_status(self):
        self.serial_handler.port = self.port_combo_box.currentText()
        self.serial_handler.toggle_serial_connection()
        

    def _send_calibration_command(self):
        current_calibration = self.calibration_combo_box.currentText()
        self.serial_handler.send_command(Commands.CALIBRATION_COMMANDS[current_calibration])
        pass


    def _read_serial_data(self):
        if self.serial_handler.get_current_connection_status() != "Connected":
            return
        
        SerialReadWindow(self.parent)
        pass


    def _handle_connection_change(self, message: str):
        """ Handle connection status changes """
        # Change status label
        self.connection_status_label.setText(f"Status: {message}")

        if message == "Connected":
            self.connect_button.setText("Disconnect")
            self.connect_button.setStyleSheet(self.connect_button_styles["disconnect"])
            self._actions_enabled(True)

        elif message == "Error":
            self.connect_button.setText("Error")
            self.connect_button.setStyleSheet(self.connect_button_styles["error"])
            self._actions_enabled(False)

        elif message == "Disconnected":
            self.connect_button.setText("Connect")
            self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
            self._actions_enabled(False)


    def _populate_ports(self):
        """ Populate the port combo box with available ports """
        # Store current port selection
        current_port = self.port_combo_box.currentText()

        # Clear and populate port combo box
        self.port_combo_box.clear()
        ports = self.serial_handler.list_serial_ports()
        self.port_combo_box.addItems(ports)

        # Restore previous selection if available
        index = self.port_combo_box.findText(current_port)
        if index >= 0:
            self.port_combo_box.setCurrentIndex(index)
        elif ports:  # Default to first port if available
            self.port_combo_box.setCurrentIndex(0)


    def _actions_enabled(self, status: bool):
        """ Enable or disable action buttons, port combo box != status """
        self.calibrate_button.setEnabled(status)
        self.read_serial_button.setEnabled(status)
        
        self.port_combo_box.setEnabled(not status)

    def _open_help_url(self):
        webbrowser.open(self.HELP_URL)
        pass
