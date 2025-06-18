from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
)

# Custom libraries
from styles import Styles
from custom_combo_box import CustomComboBox

class MultiplayerControlsSecondaryDevices(QWidget):
    """ Class for the multiplayer controls widget for secondary devices.
    
    This class is for the app running on the other devices (the devices NOT connected to the ramp).
    
    It handles the UI for the multiplayer controls.
    """
    def __init__(self, bluetooth_client = None):
        super().__init__()

        # Get access to Bluetooth client object
        self.bluetooth_client_thread = bluetooth_client

        # Initialize connection status
        self.connection_status = "Disconnected"

        # Button styles for the connect button
        self.connect_button_styles = {
            "connect": Styles.create_button_style("green"),
            "disconnect": Styles.create_button_style("red"),
            "error": Styles.create_button_style("orange")
        }

        # Main label section
        self.main_label = QLabel('MULTIPLAYER CONTROLS')
        self.main_label.setStyleSheet(Styles.MAIN_LABEL)

        # Content section
        self._create_device_selection_section()
        self._create_connection_section()

        # Organize layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.main_label)
        self.main_layout.addLayout(self.device_selection_layout)
        self.main_layout.addLayout(self.connection_section_layout)
    
    def _create_device_selection_section(self):
        """ Creates the UI for the device selection section. """
        # Create combobox label
        self.device_dropdown_label = QLabel("Select device to connect to:")
        self.device_dropdown_label.setStyleSheet(Styles.LABEL_TEXT)

        # Create custom combobox for the user to select a paired device
        self.device_combo_box = CustomComboBox(parent=self, on_mouse_press=self._populate_devices)
        self.device_combo_box.setStyleSheet(f"{Styles.COMBOBOX_BASE}")
        self.device_combo_box.setMinimumWidth(130 * Styles.SCALE_FACTOR)
        dropdown_view = self.device_combo_box.view()
        dropdown_view.setStyleSheet(f"{Styles.COMBOBOX_DROPDOWN}")
        
        # Connect combobox signal
        self.device_combo_box.currentIndexChanged.connect(self._on_device_selected)

        # Organize layout
        self.device_selection_layout = QHBoxLayout()
        self.device_selection_layout.addWidget(self.device_dropdown_label)
        self.device_selection_layout.addWidget(self.device_combo_box)

    def _create_connection_section(self):
        """ Creates the UI for the connection section. """
        # Create the Connect button, initialized as disabled
        self.connect_button = QPushButton("Connect")
        self.connect_button.setStyleSheet(Styles.DISABLED_BUTTON)
        self.connect_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.scaled_margin = int(5 * Styles.SCALE_FACTOR)
        self.connect_button.setContentsMargins(self.scaled_margin, self.scaled_margin, self.scaled_margin, self.scaled_margin)
        self.connect_button.clicked.connect(self._toggle_connection_status)
        self.connect_button.setEnabled(False)

        # Container for the button
        button_container = QHBoxLayout()
        button_container.addWidget(self.connect_button)
        button_container.addStretch()

        # Status label
        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setStyleSheet(Styles.LABEL_TEXT)

        # Organize layout
        self.connection_section_layout = QVBoxLayout()
        self.connection_section_layout.addLayout(button_container)
        self.connection_section_layout.addWidget(self.status_label)

    def _populate_devices(self):
        """ Populates the dropdown with paired devices. """
        # Clear the dropdown
        self.device_combo_box.clear()

        # Get the list of Bluetooth devices paired to this device
        # Call the method from the BluetoothClient class
        # Store the list of paired device names
        self.bluetooth_client_thread.get_paired_devices()
        devices = self.bluetooth_client_thread.paired_device_names

        if devices is not None:
            # Add the devices to the dropdown
            self.device_combo_box.addItems(devices)
            # Default to the first device if available
            self.device_combo_box.setCurrentIndex(0)

    def _on_device_selected(self):
        """ Called when a device is selected in the combobox. """        
        # Get the name of the selected device
        selected_device_name = self.device_combo_box.currentText()

        # Return if no device is selected (i.e. it's empty)
        if selected_device_name == "":
            return
        
        # Call the method from the BluetoothClient class to set the address of the selected device
        self.bluetooth_client_thread.set_selected_device_address(selected_device_name)
        
        # Enable the connect button now that a device is selected
        self.connect_button.setEnabled(True)
        self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
    
    def _toggle_connection_status(self):
        """ Toggles the connection status. 
        
        This is called when the Connect button is clicked.
        """
        # If disconnected, disable the device selection dropdown and start the client
        if self.connection_status == "Disconnected":
            self.device_combo_box.setEnabled(False) # Disable the dropdown while connected
            self.bluetooth_client_thread.start()
        
        # If it's any other status (i.e. "Initializing", "Waiting", "Connected", "Error"),
        # stop the client
        else:
            self.device_combo_box.setEnabled(True) # Re-enable the dropdown
            self.bluetooth_client_thread.stop()
    
    def _handle_client_status_change(self, message: str):
        """ Handles client connection status changes to update the UI accordingly. """
        
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
