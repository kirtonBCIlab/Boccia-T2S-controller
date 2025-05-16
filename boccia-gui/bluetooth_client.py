import socket

from commands import Commands

class BluetoothClient:
    def __init__(self, commands = None):
        # Initialize the class
        self.address = None
        self.server = None

        self.commands = commands

    def initialize_client(self, address):
        self.address = address
        self.client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    def start_connection(self):
        self.client.connect((self.address, 4))
        print(f"Connected to server")

    def send_message(self, message):
        try:
            self.client.send(message.encode("utf-8"))
            print(f"Sent message: {message}")
            # data = self.client.recv(1024)
            # if not data:
            #     return
            # print(f"Message: {data.decode('utf-8')}")
        except OSError as e:
            print(f"Error sending message: {e}")

    def close(self):
        self.client.close()
        print("Connection closed")

if __name__ == "__main__":
    
    commands = Commands()
    client = BluetoothClient(commands)
    server_address = commands.get_bluetooth_detail("address")
    if server_address is None:
        print("Bluetooth server address not found")
        exit(1)
    
    client.initialize_client(server_address)
    client.start_connection()

    try:
        while True:
            key = input("Press a key: ")
            if key == "1":
                client.send_message("Test message 1")
            elif key == "2":
                client.send_message("Test message 2")
            elif key.lower() == "q":
                break
            else:
                print("Invalid key")
    finally:
        client.close()


