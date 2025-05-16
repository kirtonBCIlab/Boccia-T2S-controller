import socket
import subprocess
import re

from commands import Commands

class BluetoothServer:
    def __init__(self, commands = None):
        # Initialize the class
        self.address = None
        self.server = None

        self.commands = commands

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

    def get_bluetooth_mac_address(self):
        try:
            output = subprocess.check_output("getmac /v /fo list", shell=True, text=True)
            for block in output.split("\n\n"):
                if "Bluetooth" in block:
                    match = re.search(r"Physical Address: ([\w-]+)", block)
                    if match:
                        address = match.group(1).replace("-", ":")
                        self.commands.set_bluetooth_detail("address", address)
                        return address
        except Exception as e:
            print(f"Error retrieving Bluetooth MAC address: {e}")
        return None

if __name__ == "__main__":
    
    commands = Commands()
    server = BluetoothServer(commands) 
    mac_address = server.get_bluetooth_mac_address()
    print(f"Bluetooth MAC address: {mac_address}")

    if not mac_address:
        print("No Bluetooth MAC address found")
        exit(1)

    address_from_commands = commands.get_bluetooth_detail("address")
    server.initialize_server(mac_address)

    try:
        server.accept_client()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    finally:
        server.close()