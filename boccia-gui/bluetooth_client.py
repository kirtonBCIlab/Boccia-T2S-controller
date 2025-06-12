from PyQt5.QtCore import QThread, pyqtSignal
import socket
from bt_devices import BluetoothDevices

class BluetoothClient(QThread):
    client_status_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Initialize BluetoothDevices object
        self.bluetooth_devices = BluetoothDevices()
        self._running = False

        self.paired_devices = None
        self.paired_device_names = None

    def run(self):
        self._running = True
        self.run_bluetooth_client()

    def run_bluetooth_client(self):
        self.client = self.initialize_client()

        if not self.client:
            self.client_status_changed.emit("Error")
            # print("Failed to initialize Bluetooth client")
            return
        
        connection = self.start_connection()
        if not connection:
            return

        try:
            self.read_from_server()
        except Exception as e:
            if self._running:
                self.client_status_changed.emit("Error")
            # print(f"Bluetooth Client Error: {e}")
        finally:
            if self._running:
                self.stop()

    def get_paired_devices(self):
        # Look for a server to connect to
        self.paired_devices = self.bluetooth_devices.get_paired_bluetooth_devices()
        if not self.paired_devices:
            self.client_status_changed.emit("No devices found")
            # print("No paired Bluetooth devices found.")
            return
        
        self.paired_device_names = []
        for name, mac, desc in self.paired_devices:
            self.paired_device_names.append(name)

    def get_selected_device_address(self, device_name):
        # Get the MAC address of a device based on its name from the paired_devices list
        self.server_address = self.paired_devices[self.paired_device_names.index(device_name)][1]
    
    def initialize_client(self):
        client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        return client

    def start_connection(self):
        try:
            self.client.connect((self.server_address, 4))
            return True
        except Exception as e:
            self.client_status_changed.emit("Error")
            # print(f"Error connecting to main device: {e}")
            return False
        
    def read_from_server(self):
        try:
            # Check the initial message from the server to verify connection was successful
            data = self.client.recv(1024)
            if data:
                message = data.decode('utf-8')
                if message == "Max clients reached":
                    self.client_status_changed.emit("Error")
                    self.client.close()
                    return
                elif message == "Connected":
                    self.client_status_changed.emit("Connected")
            
            elif not data:
                self.client_status_changed.emit("Error")
                # print("Could not connect to server")
                self.client.close()
                return
            
            # Start listening for commands
            while self._running:
                # Receive message from server
                    data = self.client.recv(1024)
                    if not data:
                        break
                    command = data.decode('utf-8')

                    # Stop if disconnect command is received
                    if command == "Disconnect":
                        self.stop()
                        return
                    
        except Exception as e:
            if self._running:
                self.client_status_changed.emit("Error")
                # print(f"Error receiving command: {e}")

    def send_command(self, command_text: str):
        try:
            self.client.send(command_text.encode("utf-8"))
            # print(f"Sent command: {command_text}")
        except Exception as e:
            if self._running:
                self.client_status_changed.emit("Error")
                # print(f"Error sending command: {e}")

    def stop(self):
        if not self._running:
            return
        
        self._running = False

        self.client_status_changed.emit("Disconnected")
        if self.client:
            try:
                self.send_command("Disconnect")
            except Exception:
                self.client_status_changed.emit("Error")
            try:
                self.client.close()
            except Exception:
                self.client_status_changed.emit("Error")
            self.client = None


