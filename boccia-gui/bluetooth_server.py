from PyQt5.QtCore import QThread, pyqtSignal
import socket
from bt_devices import BluetoothDevices

class BluetoothServer(QThread):
    
    server_status_changed = pyqtSignal(str)

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
            print("Failed to initialize Bluetooth server")
            return
        
        try:
            self.server_status_changed.emit("Waiting")
            self.accept_client()
            self.read_data()
        except Exception as e:
            self.server_status_changed.emit("Error")
            print(f"Bluetooth Server Error: {e}")
        finally:
            self.close()
    
    def initialize_server(self, address):
        server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        server.bind((address, 4))
        server.listen(1)
        return server

    def accept_client(self):
        self.client, self.client_address = self.server.accept()
        self.server_status_changed.emit("Connected")

    def read_data(self):
        try:
            while self._running:
                data = self.client.recv(1024)
                if not data:
                    break
                print(f"Received message: {data.decode('utf-8')}")
        except OSError as e:
            print(f"Error receiving message: {e}")

    def stop(self):
        self._running = False
        self.server_status_changed.emit("Disconnected")

        if hasattr(self, 'client'):
            self.client.close()
        self.server.close()

        print("Bluetooth server stopped")