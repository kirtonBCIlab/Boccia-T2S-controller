# Import libraries
from styles import Styles
from PyQt5.QtCore import Qt
from serial_read_window import SerialReadWindow
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QSizePolicy
    )

class SerialControlsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Suscribe to external events
        self.parent.serial_handler.connection_changed.connect(self._handle_connection_change)
        
        # Settings
        self.connect_button_styles = {
            "connect": Styles.create_button_style("green"),
            "disconnect": Styles.create_button_style("red"),
            "error": Styles.create_button_style("orange")
        }
    
        # Main label section
        self.main_label = QLabel('SERIAL CONNECTION')
        self.main_label.setStyleSheet(Styles.MAIN_LABEL)
        
        # Content section
        self._create_connect_and_status_section()
        self._create_calibration_and_port_section()
        self._create_serial_actions()

        self.content_layout = QHBoxLayout()
        self.content_layout.addLayout(self.connection_section_layout)
        self.content_layout.addLayout(self.calibration_and_port_layout)

        # Organize layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.main_label)
        self.main_layout.addLayout(self.content_layout)
        self.main_layout.addLayout(self.serial_actions_container)

    
    def toggle_read_serial(self):
        if self.read_serial_button.isEnabled():
            self.read_serial_button.setEnabled(False)
            self.read_serial_button.setStyleSheet(Styles.DISABLED_BUTTON)
        else:
            self.read_serial_button.setEnabled(True)
            self.read_serial_button.setStyleSheet(Styles.BUTTON_BASE)


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
        self.calibration_combo_box.addItems(self.parent.calibration_options.keys())

        self.calibration_section = QHBoxLayout()
        self.calibration_section.addWidget(self.calibration_label)
        self.calibration_section.addWidget(self.calibration_combo_box)

        # Port selection
        self.port_label = QLabel('COM Port')
        self.port_label.setStyleSheet(Styles.LABEL_TEXT)

        self.port_combo_box = QComboBox()
        self.port_combo_box.setStyleSheet( f"{Styles.COMBOBOX_BASE} width: 70px;")
        self.port_combo_box.activated.connect(self._populate_ports)
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

        # Read serial button
        self.read_serial_button = QPushButton('Read serial')
        self.read_serial_button.setStyleSheet(Styles.HOVER_BUTTON)
        self.read_serial_button.clicked.connect(self._read_serial_data)

        # Organize layout
        self.serial_actions_container = QVBoxLayout()
        self.serial_actions_container.addWidget(self.read_serial_button)
        self.serial_actions_container.addWidget(self.calibrate_button)
        

    def _toggle_connection_status(self):
        self.parent.serial_handler.port = self.port_combo_box.currentText()
        self.parent.serial_handler.toggle_serial_connection()
        

    def _send_calibration_command(self):
        print("Calibrating...")
        pass


    def _read_serial_data(self):
        if self.parent.serial_handler.get_current_connection_status() != "Connected":
            return
        
        serial_read_window = SerialReadWindow(self.parent)
        pass


    def _handle_connection_change(self, message: str):
        print(message)
        self.connection_status_label.setText(f"Status: {message}")
        if message == "Connected":
            self.connect_button.setText("Disconnect")
            self.connect_button.setStyleSheet(self.connect_button_styles["disconnect"])
            self.port_combo_box.setEnabled(False)
        elif message == "Error":
            self.connect_button.setText("Error")
            self.connect_button.setStyleSheet(self.connect_button_styles["error"])
            self.port_combo_box.setEnabled(True)
        elif message == "Disconnected":
            self.connect_button.setText("Connect")
            self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
            self.port_combo_box.setEnabled(True)


    def _populate_ports(self):
        # Store current port selection
        current_port = self.port_combo_box.currentText()

        # Clear and populate port combo box
        self.port_combo_box.clear()
        ports = self.parent.serial_handler.list_serial_ports()
        self.port_combo_box.addItems(ports)

        # Restore previous selection if available
        index = self.port_combo_box.findText(current_port)
        if index >= 0:
            self.port_combo_box.setCurrentIndex(index)
        elif ports:  # Default to first port if available
            self.port_combo_box.setCurrentIndex(0)