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
            print("No local Bluetooth adapters found")
            return
        
        for name, mac, desc in self.local_bluetooth_adapter:
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
            print(f"Bluetooth Server Error: {e}")
        finally:
            if self._running:
                self.stop()
    
    def initialize_server(self, address):
        try:
            server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            server.bind((address, 4))
            server.listen(1)
            return server
        except OSError:
            self.server_status_changed.emit("Error")

    def accept_client(self):
        try:
            if self._running:
                self.client, self.client_address = self.server.accept()
                self.server_status_changed.emit("Connected")
        except OSError:
            self.server_status_changed.emit("Error")

    def read_commands(self):
        try:
            while self._running:
                data = self.client.recv(1024)
                if not data:
                    break
                command = data.decode('utf-8')
                print(f"Received command: {command}")
                self.command_received.emit(command)
        except OSError as e:
            print(f"Error receiving command: {e}")

    def stop(self):
        self._running = False

        if hasattr(self, 'client') and self.client:
            try:
                self.client.close()
            except Exception as e:
                print(f"Error closing client: {e}")
            self.client = None
        
        if hasattr(self, 'server') and self.server:
            try:
                self.server.close()
            except Exception as e:
                print(f"Error closing server: {e}")
            self.server = None

        self.server_status_changed.emit("Disconnected")
        print("Bluetooth server stopped")