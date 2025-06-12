from PyQt5.QtCore import QThread, pyqtSignal
import socket
import threading
from bt_devices import BluetoothDevices
from commands import Commands

class BluetoothServer(QThread):
    
    server_status_changed = pyqtSignal(str)
    command_received = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.bluetooth_devices = BluetoothDevices()
        self._running = False
        self._connected_clients = [] # List of tuples (client, client_address)
        
        # Number of players (i.e. additional devices connected)
        self._player_count = 1 # Start at 1 since Player 1 is the local device (server)

        # Number of clients allowed to connect
        self._num_clients = 1 # Default to 1 (for a minimum 2 players total)
    
    def set_num_clients(self, num_players: int):
        # Equals 1 less than the total number of players
        self._num_clients = num_players - 1
        # print(f"Number of clients set to {self._num_clients}")

    def run(self):
        self._running = True
        self._run_bluetooth_server()

    def _run_bluetooth_server(self):
        self.server = self._initialize_server()

        if not self.server:
            self.server_status_changed.emit("Error")
            # print("Failed to initialize Bluetooth server")
            return
        
        try:
            if self._running:
                self.server_status_changed.emit("Waiting")
            connection_thread = threading.Thread(target=self._accept_clients)
            connection_thread.start()
            connection_thread.join()
        except Exception as e:
            if self._running:
                self.server_status_changed.emit("Error")
                # print(f"Bluetooth Server Error: {e}")
    
    def _initialize_server(self):
        self.server_status_changed.emit("Initializing")

        # Get the address of the Bluetooth adapter of the local machine
        self.local_bluetooth_adapter = self.bluetooth_devices.get_local_bluetooth_adapter()

        # Return None if no adapters are found
        if not self.local_bluetooth_adapter:
            self.server_status_changed.emit("Error")
            return
        
        # Use the first adapter in the list
        # (There should only be one item in the list if get_local_bluetooth_adapter() worked correctly)
        _, address, _ = self.local_bluetooth_adapter[0]

        try:
            server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            server.bind((address, Commands.BLUETOOTH_VARIABLES["RFCOMM_channel"]))

            # Set max number of connections that can be queued
            server.listen(self._num_clients)
            return server
        
        except Exception as e:
            self.server_status_changed.emit("Error")
            # print(f"Error initializing Bluetooth server: {e}")
            return

    def _accept_clients(self):
        while self._running:
            try:
                client, client_address = self.server.accept()
                # Check if the max number of clients has been reached
                if len(self._connected_clients) >= self._num_clients:
                    self._send_to_client(client, Commands.BLUETOOTH_VARIABLES["max_clients_message"])
                    client.close()
                    continue
                self._send_to_client(client, "Connected")
                client_thread = threading.Thread(target=self._handle_client, args=(client, client_address))
                client_thread.start()
            except Exception:
                break

    def _handle_client(self, client, client_address):
        # Add client and client address to the list
        self._connected_clients.append((client, client_address))
        
        # Increment player count
        self._player_count += 1
        player_number = "Player " + str(self._player_count)
        # print(f"{player_number} connected")
        self.server_status_changed.emit("Connected")

        try:
            while self._running:
                # Receive message from client
                data = client.recv(Commands.BLUETOOTH_VARIABLES["bytes"])
                if not data:
                    break
                command = data.decode(Commands.BLUETOOTH_VARIABLES["data_format"])

                # Stop if disconnect command is received
                if command == Commands.BLUETOOTH_VARIABLES["disconnect_command"]:
                    self.stop()
                    return

                # Otherwise emit the player number and command
                self.command_received.emit(player_number, command)

        except Exception as e:
            self.server_status_changed.emit("Error")
            # print(f"Error receiving command from client: {e}")
        
        finally:
            # Close the client
            client.close()
            if (client, client_address) in self._connected_clients:
                self._connected_clients.remove((client, client_address))
            if not self._connected_clients:
                self.server_status_changed.emit("Disconnected")

    def _send_to_client(self, client, command_text: str):
        # Sends a command to a specific client

        # Make sure server is running
        if not self._running:
            return
        
        try:
            client.send(command_text.encode(Commands.BLUETOOTH_VARIABLES["data_format"]))
            # print(f"Sent command: {command_text}")
        except Exception as e:
            self.server_status_changed.emit("Error")
            # print(f"Error sending command: {e}")

    def stop(self):
        if not self._running:
            return
        
        self._running = False
        self._player_count = 1 # Reset player count

        # Make sure all clients are closed
        for client, _ in self._connected_clients:
            try:
                disconnect_command = Commands.BLUETOOTH_VARIABLES["disconnect_command"]
                client.send(disconnect_command.encode(Commands.BLUETOOTH_VARIABLES["data_format"]))
                client.close()
            except Exception:
                self.server_status_changed.emit("Error")
        self._connected_clients.clear()
        
        # Close the server
        if hasattr(self, 'server') and self.server:
            try:
                self.server.close()
            except Exception:
                self.server_status_changed.emit("Error")
            self.server = None

        self.server_status_changed.emit("Disconnected")
        # print("Bluetooth server stopped")