from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QComboBox
)

# Custom libraries
from styles import Styles
from commands import Commands
from custom_combo_box import CustomComboBox

class MultiplayerControlsMainDevice(QWidget):
    def __init__(self, bluetooth_server = None):
        super().__init__()
        
        # Get access to Bluetooth server object
        self.bluetooth_server_thread = bluetooth_server

        # Initialize multiplayer mode indicator
        self.multiplayer_mode = False
        # Initialize connection status
        self.connection_status = "Disconnected"
        # Initialize count of connected devices
        self.connected_devices_count = 0

        self.connect_button_styles = {
            "connect": Styles.create_button_style("green"),
            "disconnect": Styles.create_button_style("red"),
            "error": Styles.create_button_style("orange")
        }

        # Main label section
        self.main_label = QLabel('MULTIPLAYER CONTROLS')
        self.main_label.setStyleSheet(Styles.MAIN_LABEL)

        # Content section
        self._create_multiplayer_mode_section()
        self._create_connection_section()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.main_label)
        self.main_layout.addLayout(self.multiplayer_mode_section_layout) 
        self.main_layout.addLayout(self.connection_section_layout)

    def _create_multiplayer_mode_section(self):
        # Create button to toggle multiplayer mode on/off
        self.multiplayer_mode_button = QPushButton("Turn ON Multiplayer Mode")
        self.multiplayer_mode_button.setStyleSheet(Styles.HOVER_BUTTON)
        self.multiplayer_mode_button.clicked.connect(self._multiplayer_mode_clicked)

        # Create setting for number of players
        self.num_players_label = QLabel("Select number of players:")
        self.num_players_label.setStyleSheet(Styles.LABEL_TEXT)

        self.num_players_box = QComboBox()
        self.num_players_box.setStyleSheet( f"{Styles.COMBOBOX_BASE} width: {50 * Styles.SCALE_FACTOR}px;")
        # Add numbers in the range from min to max number of players in multiplayer mode, inclusive
        for i in range(Commands.MIN_MULTIPLAYERS, Commands.MAX_MULTIPLAYERS + 1):
            self.num_players_box.addItem(str(i))
        self.num_players_box.setEnabled(False)
        self.num_players_box.currentIndexChanged.connect(self._set_num_players)

        self.multiplayer_mode_section_layout = QHBoxLayout()
        self.multiplayer_mode_section_layout.addWidget(self.multiplayer_mode_button)
        self.multiplayer_mode_section_layout.addStretch()
        self.multiplayer_mode_section_layout.addWidget(self.num_players_label)
        self.multiplayer_mode_section_layout.addWidget(self.num_players_box)
    
    def _create_connection_section(self):
        # Create the Connect button, initialized as disabled
        self.connect_button = QPushButton("Connect")
        self.connect_button.setStyleSheet(Styles.DISABLED_BUTTON)
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
        if self.multiplayer_mode == False:
            self.multiplayer_mode = True
            self.multiplayer_mode_button.setText("Turn OFF Multiplayer Mode")
            # Enable the number of players box
            self.num_players_box.setEnabled(True)
            # Enable the connect button
            self.connect_button.setEnabled(True)
            self.connect_button.setText("Connect") # Make sure button says "Connect"
            self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
            self.status_label.setText("Status: Ready to setup")
        else:
            self.multiplayer_mode = False
            self.multiplayer_mode_button.setText("Turn ON Multiplayer Mode")
            self.bluetooth_server_thread.stop() # Stop the thread
            self.connection_status = "Disconnected" # Reset connection status
            # Disable the number of players box
            self.num_players_box.setEnabled(False)
            # Disable the connect button
            self.connect_button.setEnabled(False)
            self.connect_button.setStyleSheet(Styles.DISABLED_BUTTON)
            self.connect_button.setText("Connect") # Make sure button says "Connect"
            self.status_label.setText("Status: Off")

    def _toggle_connection_status(self):
        if self.connection_status == "Disconnected":
            self.bluetooth_server_thread.start()
        else:
            self.bluetooth_server_thread.stop()

    def _set_num_players(self):
        self.bluetooth_server_thread.set_num_clients(int(self.num_players_box.currentText()))

    def _handle_server_status_change(self, message: str):
        if message == "Error":
            self.connect_button.setText("Error")
            self.connect_button.setStyleSheet(self.connect_button_styles["error"])
            self.status_label.setText("Status: Error")
            self.connection_status = "Error"

        if message == "Initializing":
            self.connect_button.setText("Cancel")
            self.connect_button.setStyleSheet(self.connect_button_styles["disconnect"])
            self.status_label.setText("Status: Setting up this device...")
            self.connection_status = "Initializing"

        if message == "Waiting":
            self.connect_button.setText("Cancel")
            self.connect_button.setStyleSheet(self.connect_button_styles["disconnect"])
            self.status_label.setText("Status: Waiting for other devices...")
            self.connection_status = "Waiting"
        
        if message == "Connected":
            # Increment number of connected devices
            self.connected_devices_count += 1
            # Update connection status if all devices are connected
            num_players = int(self.num_players_box.currentText())
            if self.connected_devices_count == (num_players - 1):
                self.connect_button.setText("Disconnect")
                self.connect_button.setStyleSheet(self.connect_button_styles["disconnect"])
                self.status_label.setText("Status: Connected")
                self.connection_status = "Connected"

        if message == "Disconnected":
            # Reset number of connected devices
            self.connected_devices_count = 0
            self.connect_button.setText("Connect")
            self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
            self.status_label.setText("Status: Disconnected")
            self.connection_status = "Disconnected"

class MultiplayerControlsSecondaryDevices(QWidget):
    def __init__(self, bluetooth_client = None):
        super().__init__()

        # Get access to Bluetooth client object
        self.bluetooth_client_thread = bluetooth_client

        # Initialize connection status
        self.connection_status = "Disconnected"

        self.connect_button_styles = {
            "connect": Styles.create_button_style("green"),
            "disconnect": Styles.create_button_style("red"),
            "error": Styles.create_button_style("orange")
        }

        # Multiplayer mode section
        self.main_label = QLabel('MULTIPLAYER CONTROLS')
        self.main_label.setStyleSheet(Styles.MAIN_LABEL)

        # Multiplayer controls content section
        self._create_device_selection_section()
        self._create_connection_section()

        # Instructions section
        self.instructions_section_label = QLabel("INSTRUCTIONS")
        self.instructions_section_label.setStyleSheet(Styles.MAIN_LABEL)

        # Instructions content section
        self._create_instructions_section()

        # Organize layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.main_label)
        self.main_layout.addLayout(self.device_selection_layout)
        self.main_layout.addLayout(self.connection_section_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.instructions_section_label)
        self.main_layout.addLayout(self.instructions_section_layout)

    def _create_instructions_section(self):
        self.instructions_title = QLabel("Follow these steps to setup Bluetooth connection for Multiplayer Mode:")
        self.instructions_title.setStyleSheet(Styles.INSTRUCTIONS_TEXT)

        instructions_text = (
            "1. Pair the devices in Bluetooth settings.<br>"
            "2. Make sure Bluetooth remains turned on for both devices.<br>"
            "3. In the Main Device app:<br>"
            "&nbsp;&nbsp;&nbsp;a) Click 'Turn ON Multiplayer Mode'.<br>"
            "&nbsp;&nbsp;&nbsp;b) Click 'Connect'.<br>"
            "&nbsp;&nbsp;&nbsp;c) Wait until the status says 'Waiting for other devices'.<br>"
            "4. In the Multiplayer Device app (this app):<br>"
            "&nbsp;&nbsp;&nbsp;a) Click the dropdown menu to see the list of paired devices.<br>"
            "&nbsp;&nbsp;&nbsp;b) Select the name of the Main Device.<br>"
            "&nbsp;&nbsp;&nbsp;c) Click 'Connect'."
        )
        self.instructions = QLabel(instructions_text)
        self.instructions.setStyleSheet(Styles.INSTRUCTIONS_TEXT)
        self.instructions.setTextFormat(Qt.RichText)
        self.instructions.setWordWrap(True)

        self.instructions_section_layout = QVBoxLayout()
        self.instructions_section_layout.addWidget(self.instructions_title)
        self.instructions_section_layout.addWidget(self.instructions)
    
    def _create_device_selection_section(self):
        # Create combobox label
        self.device_dropdown_label = QLabel("Select device to connect to:")
        self.device_dropdown_label.setStyleSheet(Styles.LABEL_TEXT)

        # Create custom combobox
        self.device_combo_box = CustomComboBox(parent=self, on_mouse_press=self._populate_devices)
        self.device_combo_box.setStyleSheet(f"""
            {Styles.COMBOBOX_BASE} 
            min-width: {130 * Styles.SCALE_FACTOR}px; 
            QComboBox QAbstractItemView QScrollBar:vertical {{
                width: {10 * Styles.SCALE_FACTOR}px;
                background: #f0f0f0;
            }}
        """)
        self.device_combo_box.currentIndexChanged.connect(self._on_device_selected)

        self.device_selection_layout = QHBoxLayout()
        self.device_selection_layout.addWidget(self.device_dropdown_label)
        self.device_selection_layout.addWidget(self.device_combo_box)

    def _create_connection_section(self):
        # Create the Connect button, initialized as disabled
        self.connect_button = QPushButton("Connect")
        self.connect_button.setStyleSheet(Styles.DISABLED_BUTTON)
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

    def _populate_devices(self):
        self.device_combo_box.clear()

        # Get the list of Bluetooth devices paired with this device
        self.bluetooth_client_thread.get_paired_devices()
        devices = self.bluetooth_client_thread.paired_device_names

        if devices is not None:
            self.device_combo_box.addItems(devices)
            # Default to the first device if available
            self.device_combo_box.setCurrentIndex(0)

    def _on_device_selected(self):        
        selected_device_name = self.device_combo_box.currentText()

        # Return if no device is selected
        if selected_device_name == "":
            return
        
        # Set the address of the selected device
        self.bluetooth_client_thread.get_selected_device_address(selected_device_name)
        # Enable the connect button
        self.connect_button.setEnabled(True)
        self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
    
    def _toggle_connection_status(self):
        if self.connection_status == "Disconnected":
            self.device_combo_box.setEnabled(False) # Disable the combobox while connected
            self.bluetooth_client_thread.start()
        else:
            self.device_combo_box.setEnabled(True)
            self.bluetooth_client_thread.stop()
    
    def _handle_client_status_change(self, message: str):
        if message == "Error":
            self.connect_button.setText("Error")
            self.connect_button.setStyleSheet(self.connect_button_styles["error"])
            self.status_label.setText("Status: Error")
            self.connection_status = "Error"
        
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
