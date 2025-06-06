from PyQt5.QtCore import QThread, pyqtSignal
import socket
from bt_devices import BluetoothDevices

class BluetoothServer(QThread):
    
    server_status_changed = pyqtSignal(str)
    command_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.bluetooth_devices = BluetoothDevices()
        self._running = False

    def run(self):
        self._running = True
        self.run_bluetooth_server()

    def run_bluetooth_server(self):
        # Retrieve the bluetooth adapter of the local machine
        self.server_status_changed.emit("Initializing")
        self.local_bluetooth_adapter = self.bluetooth_devices.get_local_bluetooth_adapter()
        if not self.local_bluetooth_adapter:
            self.server_status_changed.emit("Error")
            # print("No local Bluetooth adapters found")
            return
        
        # Initialize the server with the first item of the list
        # Note: There should only be one adapter if get_local_bluetooth_adapter() worked correctly
        name, mac, desc = self.local_bluetooth_adapter[0]
        self.server = self.initialize_server(str(mac))

        if not self.server:
            self.server_status_changed.emit("Error")
            # print("Failed to initialize Bluetooth server")
            return
        
        try:
            if self._running:
                self.server_status_changed.emit("Waiting")
            self.accept_client()
            self.read_commands()
        except Exception as e:
            if self._running:
                self.server_status_changed.emit("Error")
                # print(f"Bluetooth Server Error: {e}")
        finally:
            if self._running:
                self.stop()
    
    def initialize_server(self, address):
        try:
            server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            server.bind((address, 4))
            server.listen(1)
            return server
        except OSError as e:
            self.server_status_changed.emit("Error")
            # print(f"Error initializing Bluetooth server: {e}")
            return # None

    def accept_client(self):
        try:
            if self._running:
                self.client, self.client_address = self.server.accept()
                self.server_status_changed.emit("Connected")
        except OSError:
            pass

    def read_commands(self):
        try:
            while self._running:
                try:
                    data = self.client.recv(1024)
                    if not data:
                        break
                    command = data.decode('utf-8')

                    # Stop if disconnect command is received
                    if command == "Disconnect":
                        break
                    
                    # Otherwise emit the command
                    # print(f"Received command: {command}")
                    self.command_received.emit(command)
                except (OSError, ConnectionAbortedError) as e:
                    if self._running:
                        self.server_status_changed.emit("Error")
                        # print(f"Could not receive commands: {e}")
                    break
        except Exception as e:
            if self._running:
                self.server_status_changed.emit("Error")
                # print(f"Error receiving command: {e}")

    def send_command(self, command_text: str):
        if hasattr(self, 'client') and self.client:
            try:
                self.client.send(command_text.encode("utf-8"))
                # print(f"Sent command: {command_text}")
            except OSError as e:
                self.server_status_changed.emit("Error")
                # print(f"Error sending command: {e}")

    def stop(self):
        if not self._running:
            return
        
        self._running = False

        if hasattr(self, 'client') and self.client:
            # Send disconnect command
            try:
                self.client.send("Disconnect".encode("utf-8"))
            except Exception:
                self.server_status_changed.emit("Error")
                # print("Failed to send disconnect command")
            # Close client
            try:
                self.client.close()
            except Exception:
                self.server_status_changed.emit("Error")
                # print("Failed to close client")
            self.client = None
        
        if hasattr(self, 'server') and self.server:
            try:
                self.server.close()
            except Exception:
                self.server_status_changed.emit("Error")
                # print("Failed to close server")
            self.server = None

        self.server_status_changed.emit("Disconnected")
        # print("Bluetooth server stopped")