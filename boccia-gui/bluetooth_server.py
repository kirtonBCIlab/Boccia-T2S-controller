from PyQt5.QtCore import QThread, pyqtSignal
import socket
import threading
from bt_devices import BluetoothDevices

class BluetoothServer(QThread):
    
    server_status_changed = pyqtSignal(str)
    command_received = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.bluetooth_devices = BluetoothDevices()
        self._running = False
        self.connected_clients = [] # List of tuples (client, client_address)
        
        # Number of players (i.e. additional devices connected)
        self.player_count = 1 # Start at 1 since Player 1 is the local device (server)

        # Number of clients allowed to connect
        self.num_clients = 1 # Default to 1 (for a minimum 2 players total)
    
    def set_num_clients(self, num_players: int):
        # Equals 1 less than the total number of players
        self.num_clients = num_players - 1
        # print(f"Number of clients set to {self.num_clients}")

    def run(self):
        self._running = True
        self.run_bluetooth_server()

    def run_bluetooth_server(self):
        self.server = self.initialize_server()

        if not self.server:
            self.server_status_changed.emit("Error")
            # print("Failed to initialize Bluetooth server")
            return
        
        try:
            if self._running:
                self.server_status_changed.emit("Waiting")
            connection_thread = threading.Thread(target=self.accept_clients)
            connection_thread.start()
            connection_thread.join()
        except Exception as e:
            if self._running:
                self.server_status_changed.emit("Error")
                # print(f"Bluetooth Server Error: {e}")
    
    def initialize_server(self):
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
            server.bind((address, 4))

            # Listen for incoming connections for a max of num_clients
            server.listen(self.num_clients)
            return server
        
        except Exception as e:
            self.server_status_changed.emit("Error")
            # print(f"Error initializing Bluetooth server: {e}")
            return

    def accept_clients(self):
        while self._running and len(self.connected_clients) < self.num_clients:
            try:
                client, client_address = self.server.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client, client_address))
                client_thread.start()
            except Exception:
                break

    def handle_client(self, client, client_address):
        # Add client and client address to the list
        self.connected_clients.append((client, client_address))
        
        # Increment player count
        self.player_count += 1
        player_number = "Player " + str(self.player_count)
        print(f"{player_number} connected")
        self.server_status_changed.emit("Connected")

        try:
            while self._running:
                # Receive message from client
                data = client.recv(1024)
                if not data:
                    break
                command = data.decode('utf-8')

                # Stop if disconnect command is received
                if command == "Disconnect":
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
            if (client, client_address) in self.connected_clients:
                self.connected_clients.remove((client, client_address))
            if not self.connected_clients:
                self.server_status_changed.emit("Disconnected")

    def send_command(self, command_text: str):
        # Sends a command to all connected clients
        for client, _ in self.connected_clients:
            try:
                client.send(command_text.encode("utf-8"))
                # print(f"Sent command: {command_text}")
            except Exception as e:
                self.server_status_changed.emit("Error")
                # print(f"Error sending command: {e}")

    def stop(self):
        if not self._running:
            return
        
        self._running = False
        self.player_count = 1 # Reset player count

        # Make sure all clients are closed
        for client, _ in self.connected_clients:
            try:
                client.send("Disconnect".encode("utf-8"))
                client.close()
            except Exception:
                self.server_status_changed.emit("Error")
                # print("Failed to disconnect clients")
        self.connected_clients.clear()
        
        # Close the server
        if hasattr(self, 'server') and self.server:
            try:
                self.server.close()
            except Exception:
                self.server_status_changed.emit("Error")
                # print("Failed to close server")
            self.server = None

        self.server_status_changed.emit("Disconnected")
        print("Bluetooth server stopped")