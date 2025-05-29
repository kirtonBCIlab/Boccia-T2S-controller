from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QComboBox,
)

# Custom libraries
from styles import Styles
from commands import Commands
from custom_combo_box import CustomComboBox

class MultiplayerControlsDevice1(QWidget):
    def __init__(self, bluetooth_server = None):
        super().__init__()
        
        # Get access to Bluetooth server object
        self.bluetooth_server_thread = bluetooth_server

        self.connection_status = "Disconnected"

        self.connect_button_styles = {
            "connect": Styles.create_button_style("green"),
            "disconnect": Styles.create_button_style("red"),
            "error": Styles.create_button_style("orange")
        }

        # Main label section
        self.main_label = QLabel('MULTIPLAYER CONTROLS')
        self.main_label.setStyleSheet(Styles.MAIN_LABEL)

        self._create_multiplayer_mode_section()
        self._create_connection_section()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.main_label)
        self.main_layout.addLayout(self.multiplayer_mode_section_layout) 
        self.main_layout.addLayout(self.connection_section_layout)

    def _create_multiplayer_mode_section(self):
        self.multiplayer_mode_button = QPushButton("Turn ON Multiplayer Mode")
        self.multiplayer_mode_button.setStyleSheet(Styles.HOVER_BUTTON)
        self.multiplayer_mode_button.clicked.connect(self._multiplayer_mode_clicked)
        self.multiplayer_mode_button.setCheckable(True)

        self.multiplayer_mode_section_layout = QVBoxLayout()
        self.multiplayer_mode_section_layout.addWidget(self.multiplayer_mode_button)
    
    def _create_connection_section(self):
        # Create the Connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
        self.connect_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.scaled_margin = int(5 * Styles.SCALE_FACTOR)
        self.connect_button.setContentsMargins(self.scaled_margin, self.scaled_margin, self.scaled_margin, self.scaled_margin)
        self.connect_button.clicked.connect(self._toggle_connection_status)
        self.connect_button.setEnabled(False)

        button_container = QHBoxLayout()
        button_container.addWidget(self.connect_button)
        button_container.addStretch()

        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setStyleSheet(Styles.LABEL_TEXT)

        self.connection_section_layout = QVBoxLayout()
        self.connection_section_layout.addLayout(button_container)
        self.connection_section_layout.addWidget(self.status_label)

    def _multiplayer_mode_clicked(self):
        if self.multiplayer_mode_button.isChecked():
            self.multiplayer_mode_button.setText("Turn OFF Multiplayer Mode")
            self.connect_button.setEnabled(True)
            self.status_label.setText("Status: Ready to setup")
        else:
            self.multiplayer_mode_button.setText("Turn ON Multiplayer Mode")
            self.connect_button.setEnabled(False)
            self.status_label.setText("Status: Off")

    def _toggle_connection_status(self):
        if self.connection_status == "Disconnected":
            self.bluetooth_server_thread.start()
        else:
            self.bluetooth_server_thread.stop()

    def _handle_server_status_change(self, message: str):
        if message == "Error":
            self.connect_button.setText("Error")
            self.connect_button.setStyleSheet(self.connect_button_styles["error"])
            self.status_label.setText("Status: Error")
            self.connection_status = "Error"

        if message == "Initializing":
            self.connect_button.setText("Cancel")
            self.connect_button.setStyleSheet(self.connect_button_styles["disconnect"])
            self.status_label.setText("Status: Setting up Device 1...")
            self.connection_status = "Initializing"

        if message == "Waiting":
            self.connect_button.setText("Cancel")
            self.connect_button.setStyleSheet(self.connect_button_styles["disconnect"])
            self.status_label.setText("Status: Waiting for Device 2...")
            self.connection_status = "Waiting"
        
        if message == "Connected":
            self.connect_button.setText("Disconnect")
            self.connect_button.setStyleSheet(self.connect_button_styles["disconnect"])
            self.status_label.setText("Status: Connected")
            self.connection_status = "Connected"

        if message == "Disconnected":
            self.connect_button.setText("Connect")
            self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
            self.status_label.setText("Status: Disconnected")
            self.connection_status = "Disconnected"

class MultiplayerControlsDevice2(QWidget):
    def __init__(self, bluetooth_client = None):
        super().__init__()

        # Get access to Bluetooth client object
        self.bluetooth_client_thread = bluetooth_client

        self.bluetooth_client_thread.client_status_changed.connect(self._handle_client_status_change)

        self.connect_button_styles = {
            "connect": Styles.create_button_style("green"),
            "disconnect": Styles.create_button_style("red"),
            "error": Styles.create_button_style("orange")
        }

        # Main label section
        self.main_label = QLabel('MULTIPLAYER CONTROLS')
        self.main_label.setStyleSheet(Styles.MAIN_LABEL)

        self._create_device_selection_section()
        self._create_connection_section()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.main_label)

        self.main_layout.addLayout(self.device_selection_layout)
        self.main_layout.addLayout(self.connection_section_layout)
    
    def _create_device_selection_section(self):
        # Create the Get Devices button
        self.get_devices_button = QPushButton("Get paired devices")
        self.get_devices_button.setStyleSheet(Styles.HOVER_BUTTON)
        self.get_devices_button.clicked.connect(self.bluetooth_client_thread.get_paired_devices)

        # Create combobox label
        self.device_dropdown_label = QLabel("Select device to connect to:")
        self.device_dropdown_label.setStyleSheet(Styles.LABEL_TEXT)

        # Create custom combobox
        self.device_combo_box = CustomComboBox(parent=self, on_mouse_press=self._populate_devices)
        self.device_combo_box.setStyleSheet(f"{Styles.COMBOBOX_BASE} width: {130 * Styles.SCALE_FACTOR}px;")
        self.device_combo_box.currentIndexChanged.connect(self._on_device_selected)

        self.device_selection_layout = QHBoxLayout()
        self.device_selection_layout.addWidget(self.device_dropdown_label)
        self.device_selection_layout.addWidget(self.device_combo_box)

    def _create_connection_section(self):
        # Create the Connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
        self.connect_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.scaled_margin = int(5 * Styles.SCALE_FACTOR)
        self.connect_button.setContentsMargins(self.scaled_margin, self.scaled_margin, self.scaled_margin, self.scaled_margin)
        self.connect_button.clicked.connect(self._toggle_connection_status)
        self.connect_button.setCheckable(True)
        self.connect_button.setEnabled(False)

        button_container = QHBoxLayout()
        button_container.addWidget(self.connect_button)
        button_container.addStretch()

        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setStyleSheet(Styles.LABEL_TEXT)

        self.connection_section_layout = QVBoxLayout()
        self.connection_section_layout.addLayout(button_container)
        self.connection_section_layout.addWidget(self.status_label)

    def _populate_devices(self):
        self.device_combo_box.clear()
        self.bluetooth_client_thread.get_paired_devices()
        devices = self.bluetooth_client_thread.paired_device_names

        if devices is not None:
            self.device_combo_box.addItems(devices)
            # Default to the first device if available
            self.device_combo_box.setCurrentIndex(0)

    def _on_device_selected(self):
        selected_device_name = self.device_combo_box.currentText()
        self.bluetooth_client_thread.get_selected_device_address(selected_device_name)

        self.connect_button.setEnabled(True)
    
    def _toggle_connection_status(self):
        if self.connect_button.isChecked():
            self.bluetooth_client_thread.start()
        else:
            self.bluetooth_client_thread.stop()
    
    def _handle_client_status_change(self, message: str):
        if message == "Error":
            self.connect_button.setText("Error")
            self.connect_button.setStyleSheet(self.connect_button_styles["error"])
            self.status_label.setText("Status: Error")
        
        if message == "Connected":
            self.connect_button.setText("Disconnect")
            self.connect_button.setStyleSheet(self.connect_button_styles["disconnect"])
            self.status_label.setText("Status: Connected")

        if message == "Disconnected":
            self.connect_button.setText("Connect")
            self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
            self.status_label.setText("Status: Disconnected")
