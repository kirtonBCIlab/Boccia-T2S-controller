from PyQt5.QtCore import QThread, pyqtSignal
import socket
from bt_devices import BluetoothDevices

class BluetoothClient(QThread):
    client_status_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
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
            print("Failed to initialize Bluetooth client")
            return
        
        connection = self.start_connection()
        if not connection:
            return

        try:
            self.read_commands()
        except Exception as e:
            if self._running:
                self.client_status_changed.emit("Error")
            print(f"Bluetooth Client Error: {e}")
        finally:
            if self._running:
                self.stop()

    def get_paired_devices(self):
        # Look for a server to connect to
        self.paired_devices = self.bluetooth_devices.get_paired_bluetooth_devices()
        if not self.paired_devices:
            self.client_status_changed.emit("No devices found")
            print("No paired Bluetooth devices found")
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
            self.client_status_changed.emit("Connected")
            return True
        except (OSError, TimeoutError) as e:
            self.client_status_changed.emit("Error")
            print(f"Error connecting to Device 1: {e}")
            return False
        
    def read_commands(self):
        try:
            while self._running:
                try:
                    data = self.client.recv(1024)
                    if not data:
                        break
                    command = data.decode('utf-8')

                    if command == "Disconnect":
                        break
                except (OSError, ConnectionAbortedError) as e:
                    print(f"Error receiving command: {e}")
                    break

        except Exception as e:
            print(f"Unexpected error receiving command: {e}")

    def send_command(self, command_text: str):
        try:
            self.client.send(command_text.encode("utf-8"))
            print(f"Sent command: {command_text}")
        except OSError as e:
            if self._running:
                print(f"Error sending command: {e}")

    def stop(self):
        self._running = False
        self.client_status_changed.emit("Disconnected")
        if self.client:
            try:
                self.send_command("Disconnect")
            except Exception:
                pass
            try:
                self.client.close()
            except Exception:
                pass
            self.client = None


