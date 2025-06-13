# Import libraries
from PyQt5.QtCore import QThread, pyqtSignal
import socket

from bt_devices import BluetoothDevices
from commands import Commands

class BluetoothClient(QThread):
    """ Class that handles Bluetooth client operations.
    Inherits from QThread to run in a separate thread.
    Connects the device as a client to the BluetoothServer.
    Sends commands to the server.
    """
    # Signal to indicate the status of the client
    # This signal is emitted when the client status changes (e.g. connected, disconnected, error)
    client_status_changed = pyqtSignal(str)

    def __init__(self):
        """ Initializes BluetoothClient class.
        
        Parameters
        ----------
        None

        Returns
        -------
        None

        Attributes
        ----------
        bluetooth_devices : BluetoothDevices
            Instance of the BluetoothDevices class.
        _running : bool
            Indicates whether the client is running.
        _paired_devices : list
            List of paired Bluetooth devices.
        paired_device_names : list 
            List of the names of paired Bluetooth devices.
            Used to populate the device selection dropdown in the GUI.
        server_address : str
            The MAC address of the server device to connect to.
        """
        super().__init__()

        # Initialize BluetoothDevices instance
        self.bluetooth_devices = BluetoothDevices()

        # Initialize attributes
        self._running = False
        self._paired_devices = None
        self.paired_device_names = []
        self.server_address = None

    def run(self):
        """ This method is called when a client thread is started.

        To call this method (i.e. to start the client):
        1. Create an instance of the BluetoothClient class.
        2. Call the start() method on the instance. 
            - start() is a method of QThread that starts the thread and calls the thread's run() method.

        Sets the _running flag to True and calls the _run_bluetooth_client method.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Set the _running flag to True
        self._running = True
        # Call the method that runs the Bluetooth client
        self._run_bluetooth_client()

    def _run_bluetooth_client(self):
        """ Runs the Bluetooth client.

        Calls the method to initialize the Bluetooth client.
        Calls the method to connect to a server device.
        Calls the method to read information from the server.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Attributes
        ----------
        client : socket.socket
            The Bluetooth client socket.
        """
        # Initialize the Bluetooth client
        self.client = self._initialize_client()

        # Emit signal and exit if client was not initialized
        if not self.client:
            self.client_status_changed.emit("Error") # Emit signal to indicate an error
            # print("Failed to initialize Bluetooth client") # For debugging purposes
            return
        
        # Connect and check if the connection was successful
        connection = self._start_connection()
        if not connection:
            return

        # Start reading data from the server
        try:
            self._read_from_server()
        except Exception as e:
            if self._running:
                self.client_status_changed.emit("Error") # Emit signal to indicate an error
            # print(f"Bluetooth Client Error: {e}") # For debugging purposes
        finally:
            # Call the stop method
            if self._running:
                self.stop()

    def get_paired_devices(self):
        """ Retrieves the list of paired Bluetooth devices from the BluetoothDevices class.
        Populates the paired_device_names list with the names of the paired devices.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Clear the variables used to store paired devices
        self._paired_devices = None
        self.paired_device_names = []
        
        # Retrieve the list of paired Bluetooth devices
        self._paired_devices = self.bluetooth_devices.get_paired_bluetooth_devices()

        # Exit if no paired devices are found
        if not self._paired_devices:
            # print("No paired Bluetooth devices found.") # For debugging purposes
            return
        
        # Populate the paired_device_names list with the names of the paired devices
        for name, _, _ in self._paired_devices:
            self.paired_device_names.append(name)

    def set_selected_device_address(self, device_name):
        """ Retrieves the MAC address of a selected device based on its name.
        Sets the server_address attribute.

        Called when a device is selected from the device selection dropdown.

        Parameters
        ----------
        device_name : str
            The name of the device to get the MAC address for.

        Returns
        -------
        None
        """
        # Get the address of a device based on its name from the paired_devices list
        # Set the server_address attribute to that address
        self.server_address = self._paired_devices[self.paired_device_names.index(device_name)][1]
    
    def _initialize_client(self):
        """ Initializes the Bluetooth client socket.
        Creates a Bluetooth client socket using the RFCOMM protocol.

        Parameters
        ----------
        None

        Returns
        -------
        client : socket.socket
            The Bluetooth client socket.
        """
        client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        return client

    def _start_connection(self):
        """ Tries to connect the client to the Bluetooth server device.
        Uses the server_address attribute.
        Uses the RFCOMM channel defined in the Commands class.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True if the connection was successful, False otherwise.
        """
        try:
            self.client.connect((self.server_address, Commands.BLUETOOTH_VARIABLES["RFCOMM_channel"]))
            return True
        except Exception as e:
            self.client_status_changed.emit("Error") # Emit signal to indicate an error
            # print(f"Error connecting to main device: {e}") # For debugging purposes
            return False
        
    def _read_from_server(self):
        """ Reads and processes data/messages from the Bluetooth server.

        Reads the initial message from the server to verify connection.
        Continues to listen for commands until disconnected or an error occurs.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        try:
            # Check the initial message from the server to verify connection was successful
            data = self.client.recv(Commands.BLUETOOTH_VARIABLES["bytes"])
            if data:
                # Decode the received data
                message = data.decode(Commands.BLUETOOTH_VARIABLES["data_format"])

                # Check if the message indicates max clients are connected
                # (which means enough devices are connected to correspond to the selected number of players)
                # If so, close the client
                if message == Commands.BLUETOOTH_VARIABLES["max_clients_message"]:
                    self.client_status_changed.emit("Error") # Emit signal to indicate an error
                    self.client.close() # Close the client socket
                    return
                # Or, check if connection was successful and emit signal
                elif message == "Connected":
                    self.client_status_changed.emit("Connected")
            
            # If no data is received, emit an error signal and close the client
            elif not data:
                self.client_status_changed.emit("Error")
                # print("Could not connect to server") # For debugging purposes
                self.client.close() # Close the client socket
                return
            
            # Start continously listening for commands
            while self._running:
                # Receive data from server
                    data = self.client.recv(Commands.BLUETOOTH_VARIABLES["bytes"])
                    if not data:
                        break # Stop if no data is received
                    # Decode the received data
                    command = data.decode(Commands.BLUETOOTH_VARIABLES["data_format"])

                    # Stop if disconnect command is received from the server
                    if command == Commands.BLUETOOTH_VARIABLES["disconnect_command"]:
                        self.stop()
                        return
                    
        except Exception as e:
            if self._running:
                self.client_status_changed.emit("Error") # Emit signal to indicate an error
                # print(f"Error receiving command: {e}") # For debugging purposes

    def send_command(self, command_text: str):
        """ Sends commands to the Bluetooth server.
        This is called in the KeyPressHandlerMultiplayer class.
        Sends Toggle commands (i.e. 1, 2, or 3) to the server.

        Parameters
        ----------
        command_text : str
            The command to send to the server.
        
        Returns
        -------
        None
        """
        try:
            # Encode the command text and send it to the server
            self.client.send(command_text.encode(Commands.BLUETOOTH_VARIABLES["data_format"]))
        
        # Catch any errors
        except Exception as e:
            if self._running:
                self.client_status_changed.emit("Error") # Emit signal to indicate an error
                # print(f"Error sending command: {e}") # For debugging purposes

    def stop(self):
        """ Stops the Bluetooth client thread.
        Sets the _running flag to False.
        Emits a signal to indicate the client has disconnected.
        Sends the disconnect command to the server.
        Makes sure the client socket is closed.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Exit if already stopped
        if not self._running:
            return
        
        self._running = False # Reset the _running flag to False

        # Emit Disconnected signal
        self.client_status_changed.emit("Disconnected")

        if self.client:
            try:
                # Send the disconnect command to the server
                self.send_command(Commands.BLUETOOTH_VARIABLES["disconnect_command"])
                # Close the client socket
                self.client.close()

            # Catch any errors
            except Exception:
                self.client_status_changed.emit("Error") # Emit signal to indicate an error
                # print(f"Error closing client: {e}") # For debugging purposes
            self.client = None


