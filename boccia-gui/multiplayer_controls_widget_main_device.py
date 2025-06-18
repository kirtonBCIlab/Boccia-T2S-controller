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

class MultiplayerControlsMainDevice(QWidget):
    """ Class for the multiplayer controls widget, part of the main device app.
    
    This class is for the main device app (the device connected to the ramp).
    
    It handles the UI for the multiplayer controls.
    """
    def __init__(self, bluetooth_server = None):
        """ Initializes the MultiplayerControlsMainDevice class. """
        super().__init__()
        
        # Get access to Bluetooth server object
        self.bluetooth_server_thread = bluetooth_server

        # Initialize multiplayer mode indicator
        self.multiplayer_mode = False
        # Initialize connection status
        self.connection_status = "Disconnected" # Tracks connection status
        # Initialize count of connected devices
        self.connected_devices_count = 0

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
        self._create_multiplayer_mode_section()
        self._create_connection_section()

        # Organize layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.main_label)
        self.main_layout.addLayout(self.multiplayer_mode_section_layout) 
        self.main_layout.addLayout(self.connection_section_layout)

    def _create_multiplayer_mode_section(self):
        """ Creates the UI for the multiplayer mode section. """
        # Create button to toggle multiplayer mode on/off
        self.multiplayer_mode_button = QPushButton("Turn ON Multiplayer Mode")
        self.multiplayer_mode_button.setStyleSheet(Styles.HOVER_BUTTON)
        self.multiplayer_mode_button.clicked.connect(self._multiplayer_mode_clicked)

        # Create combobox to set the number of players
        self.num_players_label = QLabel("Number of players:")
        self.num_players_label.setStyleSheet(Styles.LABEL_TEXT)
        self.num_players_box = QComboBox()
        self.num_players_box.setStyleSheet( f"{Styles.COMBOBOX_BASE} width: {50 * Styles.SCALE_FACTOR}px;")
        # Add numbers in the range from min to max number of players defined in Commands (inclusive)
        for i in range(Commands.MIN_MULTIPLAYERS, Commands.MAX_MULTIPLAYERS + 1):
            self.num_players_box.addItem(str(i))
        self.num_players_box.setEnabled(False) # Disable by default
        self.num_players_box.currentIndexChanged.connect(self._set_num_players)
        self._set_num_players() # Set the default number of players

        # Organize layout
        self.multiplayer_mode_section_layout = QHBoxLayout()
        self.multiplayer_mode_section_layout.addWidget(self.multiplayer_mode_button)
        self.multiplayer_mode_section_layout.addStretch()
        self.multiplayer_mode_section_layout.addWidget(self.num_players_label)
        self.multiplayer_mode_section_layout.addWidget(self.num_players_box)
    
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

    def _multiplayer_mode_clicked(self):
        """ Toggles multiplayer mode on/off. """
        # If multiplayer mode is off, turn it on
        if self.multiplayer_mode == False:
            self.multiplayer_mode = True # Toggle multiplayer mode
            self.multiplayer_mode_button.setText("Turn OFF Multiplayer Mode")
            self.num_players_box.setEnabled(True) # Enable the number of players dropdown
            self.connect_button.setEnabled(True) # Enable the connect button
            self.connect_button.setText("Connect") # Make sure button says "Connect"
            self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
            self.status_label.setText("Status: Ready to setup") # Change status

        # If multiplayer mode is on, turn it off
        else:
            self.multiplayer_mode = False # Toggle multiplayer mode
            self.multiplayer_mode_button.setText("Turn ON Multiplayer Mode")
            self.bluetooth_server_thread.stop() # Stop the Bluetooth server thread
            self.connection_status = "Disconnected" # Reset connection status
            self.num_players_box.setEnabled(False) # Disable the number of players box
            self.connect_button.setEnabled(False) # Disable the connect button
            self.connect_button.setStyleSheet(Styles.DISABLED_BUTTON)
            self.connect_button.setText("Connect") # Make sure button says "Connect"
            self.status_label.setText("Status: Off") # Change status

    def _toggle_connection_status(self):
        """ Toggles connection status. 

        This is called when the Connect button is clicked.
        """
        # If disconnected, start the server
        if self.connection_status == "Disconnected":
            self.bluetooth_server_thread.start()

        # If it's any other status (i.e. "Initializing", "Waiting", "Connected", "Error"),
        # stop the server
        else:
            self.bluetooth_server_thread.stop()

    def _set_num_players(self):
        """ Sets the number of players in multiplayer mode. 
        
        This is called when the dropdown is created, and whenever its value is changed.
        """
        # Convert the number of players to an integer and set it in the Bluetooth server
        self.bluetooth_server_thread.set_num_clients(int(self.num_players_box.currentText()))

    def _handle_server_status_change(self, message: str):
        """ Handles server connection status changes to update the UI accordingly. """

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
            # Get the number of players currently set in the GUI
            num_players = int(self.num_players_box.currentText())

            # Check if enough devices are connected
            # The number of connected devices needs to be (num_players - 1)
            # Since the server device (this device) counts as Player 1
            if self.connected_devices_count == (num_players - 1):
                # Update status to "Connected" if all players are connected
                self.connect_button.setText("Disconnect")
                self.connect_button.setStyleSheet(self.connect_button_styles["disconnect"])
                self.status_label.setText("Status: Connected")
                self.connection_status = "Connected"

        if message == "Disconnected":
            # ("Disconnected" message means all devices are disconnected)
            self.connected_devices_count = 0 # Reset number of connected devices
            self.connect_button.setText("Connect")
            self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
            self.status_label.setText("Status: Disconnected")
            self.connection_status = "Disconnected"