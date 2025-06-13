# Import libraries
from PyQt5.QtCore import QThread, pyqtSignal
import socket
import threading

from bt_devices import BluetoothDevices
from commands import Commands

class BluetoothServer(QThread):
    """ Class that handles Bluetooth server operations.
    Inherits from QThread to run the server in a separate thread.
    Accepts connections from Bluetooth clients.
    Handles commands received from clients.
    """
    # Signal to indicate the status of the server
    # This signal is emitted when the server status changes (e.g. connected, disconnected, error)
    server_status_changed = pyqtSignal(str)

    # Signal to indicate a command received from a client
    # Emits the player number (i.e. which client sent it) and the command
    command_received = pyqtSignal(str, str)

    def __init__(self):
        """ Initializes BluetoothServer class.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Attributes
        ----------
        bluetooth_devices : BluetoothDevices
            Instance of BluetoothDevices class.
        _running : bool
            Indicates whether the server is running.
        _connected_clients : list
            List of tuples (client, client_address) for the connected clients.
        _player_count : int
            Number of players.
        _num_clients : int
            Number of clients to connect to (corresponds to the number of players).
        """
        super().__init__()

        # Initialize BluetoothDevices instance
        self.bluetooth_devices = BluetoothDevices()

        # Initialize attributes
        self._running = False
        self._connected_clients = [] 
        self._player_count = 1 # Start at 1 since Player 1 is the server (i.e. this device)
        self._num_clients = 1 # Default to 1 (for a minimum of 1 device connected)
    
    def set_num_clients(self, num_players: int):
        """ Sets the number of clients to connect to.

        Parameters
        ----------
        num_players : int
            Total number of players in the game (including the server).
            This value comes from the number of players set in the GUI.

        Returns
        -------
        None
        """
        # Equals 1 less than the total number of players
        # Since the server device (this device) counts as Player 1
        self._num_clients = num_players - 1

    def run(self):
        """ This method is called when the server thread is started.

        To call this method (i.e. to start the server):
        1. Create an instance of the BluetoothServer class.
        2. Call the start() method on the instance.
            - start() is a method of QThread that starts the thread and calls the thread's run() method.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Set the _running flag to True
        self._running = True
        # Call the method that runs the Bluetooth server
        self._run_bluetooth_server()

    def _run_bluetooth_server(self):
        """ Runs the Bluetooth server.

        Calls the method to initialize the Bluetooth server.
        Starts a thread to run separately to accept client connections.
        
        Parameters
        ----------
        None

        Returns
        -------
        None

        Attributes
        ----------
        server : socket.socket
            The Bluetooth server socket.
        """
        # Initialize the Bluetooth server
        self.server = self._initialize_server()

        # Emit signal and exit if server was not initialized
        if not self.server:
            self.server_status_changed.emit("Error") # Emit signal to indicate error
            # print("Failed to initialize Bluetooth server") # For debugging purposes
            return
        
        try:
            if self._running:
                # Emit signal to indicate the server is waiting for connections
                self.server_status_changed.emit("Waiting")
            # Start a thread to accept client connections
            connection_thread = threading.Thread(target=self._accept_clients)
            connection_thread.start()
            connection_thread.join()
        except Exception as e:
            if self._running:
                self.server_status_changed.emit("Error") # Emit signal to indicate error
                # print(f"Bluetooth Server Error: {e}") # For debugging purposes
    
    def _initialize_server(self):
        """ Initializes the Bluetooth server socket.
        Gets the address of the Bluetooth adapter of the local machine.
        Uses the RFCOMM channel defined in the Commands class.

        Parameters
        ----------
        None

        Returns
        -------
        socket.socket
            The Bluetooth server socket.
        """
        # Emit signal to indicate the server is initializing
        self.server_status_changed.emit("Initializing")

        # Get the address of the Bluetooth adapter of the local machine
        # Call the method in the BluetoothDevices class
        # This is the server address since this device is the server
        self.local_bluetooth_adapter = self.bluetooth_devices.get_local_bluetooth_adapter()

        # Return if no adapters are found
        if not self.local_bluetooth_adapter:
            self.server_status_changed.emit("Error") # Emit signal to indicate error
            return
        
        # Use the first adapter in the list
        # (There should only be one item in the list if get_local_bluetooth_adapter() worked correctly)
        _, address, _ = self.local_bluetooth_adapter[0]

        try:
            # Create a Bluetooth server socket
            server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            server.bind((address, Commands.BLUETOOTH_VARIABLES["RFCOMM_channel"]))

            # Set max number of connections that can be queued
            # Setting to the same value as _num_clients
            server.listen(self._num_clients)

            # Return the server socket
            return server
        
        except Exception as e:
            self.server_status_changed.emit("Error") # Emit signal to indicate error
            # print(f"Error initializing Bluetooth server: {e}") # For debugging purposes
            return

    def _accept_clients(self):
        """ Accepts client connections.
        Notifies the client if the max number of clients has been reached.

        Starts a thread to handle each client separately.
        (Using threads allows multiple clients to connect at the same time.)

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        while self._running:
            try:
                # Accept client connection
                client, client_address = self.server.accept()

                # Check if the max number of clients has been reached
                if len(self._connected_clients) >= self._num_clients:
                    # Send message to client indicating max clients are connected
                    self._send_to_client(client, Commands.BLUETOOTH_VARIABLES["max_clients_message"])
                    client.close() # Close the client socket since enough clients are connected
                    continue

                # Otherwise, send message to client indicating connection was successful
                self._send_to_client(client, "Connected")
                # Start a thread to handle the client separately
                client_thread = threading.Thread(target=self._handle_client, args=(client, client_address))
                client_thread.start()

            except Exception as e:
                # print(f"Error accepting client connection: {e}") # For debugging purposes
                break

    def _handle_client(self, client, client_address):
        """ Handles communication with a client.

        Assigns a player number to the client, depending on the count of connected players.
        Handles commands received from clients.
        Calls the stop() method if the disconnect command is received.

        Parameters
        ----------
        client : socket.socket
            The client socket.
        client_address : tuple
            The address informationof the client.

        Returns
        -------
        None
        """
        # Add client and client address to the list of connected clients
        self._connected_clients.append((client, client_address))
        
        # Increment player count
        self._player_count += 1
        # Assign player number to this client based on player count
        player_number = "Player " + str(self._player_count)
        # print(f"{player_number} connected") # For debugging purposes

        # Emit Connected signal
        self.server_status_changed.emit("Connected") 

        # Handle commands from client
        try:
            while self._running:
                # Receive message from client
                data = client.recv(Commands.BLUETOOTH_VARIABLES["bytes"])
                if not data:
                    break # Stop if no data is received
                # Decode the received data
                command = data.decode(Commands.BLUETOOTH_VARIABLES["data_format"])

                # Stop if disconnect command is received from the client
                if command == Commands.BLUETOOTH_VARIABLES["disconnect_command"]:
                    self.stop()
                    return

                # Otherwise emit the player number and command
                self.command_received.emit(player_number, command)

        # Catch any errors
        except Exception as e:
            self.server_status_changed.emit("Error") # Emit signal to indicate error
            # print(f"Error receiving command from client: {e}") # For debugging purposes
        
        # Close the client to clean up
        finally:
            client.close()
            if (client, client_address) in self._connected_clients:
                # Remove the client and client address from the list
                self._connected_clients.remove((client, client_address))
            if not self._connected_clients:
                # Emit Disconnected signal if no clients are connected anymore
                self.server_status_changed.emit("Disconnected")

    def _send_to_client(self, client, command_text: str):
        """ Sends a command to a specific client.

        Parameters
        ----------
        client : socket.socket
            The client socket.
        command_text : str
            The command to send.

        Returns
        -------
        None
        """
        # Make sure server is running before proceeding
        if not self._running:
            return
        
        try:
            # Encode the command text and send it to the client
            client.send(command_text.encode(Commands.BLUETOOTH_VARIABLES["data_format"]))
        
        # Catch any errors
        except Exception as e:
            self.server_status_changed.emit("Error") # Emit signal to indicate error
            # print(f"Error sending command: {e}") # For debugging purposes

    def stop(self):
        """ Stops the Bluetooth server thread, and ensures all clients are closed.
        Sets the _running flag to False.
        Sends the disconnect command to all connected clients, and closes all client sockets.
        Clears the list of connected clients.
        Closes the server socket.
        Emits a signal to indicate the server has disconnected.

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
        self._player_count = 1 # Reset player count

        # Close all connected client sockets
        for client, _ in self._connected_clients:
            try:
                # Send the disconnect command to the client
                disconnect_command = Commands.BLUETOOTH_VARIABLES["disconnect_command"]
                client.send(disconnect_command.encode(Commands.BLUETOOTH_VARIABLES["data_format"]))
                client.close() # Close the client socket

            except Exception:
                self.server_status_changed.emit("Error") # Emit signal to indicate error
        
        # Clear the list of connected clients
        self._connected_clients.clear()
        
        # Close the server
        if hasattr(self, 'server') and self.server:
            try:
                self.server.close()

            # Catch any errors
            except Exception:
                self.server_status_changed.emit("Error") # Emit signal to indicate error
                # print(f"Error closing server: {e}") # For debugging purposes
            self.server = None

        # Emit Disconnected signal
        self.server_status_changed.emit("Disconnected")
        # print("Bluetooth server stopped") # For debugging purposes