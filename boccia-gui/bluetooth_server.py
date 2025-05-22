import socket
import subprocess
import re
from bt_devices import BluetoothDevices

class BluetoothServer:
    def __init__(self):
        # Initialize the class
        self.address = None
        self.server = None

    def initialize_server(self, address):
        self.address = address
        self.server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.server.bind((self.address, 4))
        self.server.listen(1)

    def accept_client(self):
        self.client, self.client_address = self.server.accept()
        print(f"Accepted connection from client")
        self.read_data()

    def read_data(self):
        try:
            while True:
                data = self.client.recv(1024)
                if not data:
                    break
                print(f"Received message: {data.decode('utf-8')}")
        except OSError as e:
            print(f"Error receiving message: {e}")

    def close(self):
        if hasattr(self, 'client'):
            self.client.close()
        self.server.close()

if __name__ == "__main__":
    
    server = BluetoothServer() 
    bluetooth_devices = BluetoothDevices()

    local_bluetooth_adapter = bluetooth_devices.get_local_bluetooth_adapter()
    if not local_bluetooth_adapter:
        print("No local Bluetooth adapters found.")
    else:
        print("Local Bluetooth adapter:")
        for name, mac, desc in local_bluetooth_adapter:
            print(f"Adapter Name: {name}, MAC Address: {mac}, Description: {desc}")
            server.initialize_server(mac)

    try:
        server.accept_client()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    finally:
        server.close()