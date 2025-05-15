import socket

class BluetoothClient:
    def __init__(self, address):
        self.address = address
        self.client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    def start_connection(self):
        self.client.connect((self.address, 4))
        print(f"Connected to server")

    def send_message(self, message):
        try:
            self.client.send(message.encode("utf-8"))
            data = self.client.recv(1024)
            if not data:
                return
            print(f"Message: {data.decode('utf-8')}")
        except OSError as e:
            print(f"Error sending message: {e}")

    def close(self):
        self.client.close()
        print("Connection closed")

if __name__ == "__main__":
    client = BluetoothClient("E8:9C:25:5D:AA:42")
    client.start_connection()

    key = input("Press 1to send message: ")
    if key == '1':
        client.send_message("Test message from client")
    else:
        print("Invalid key pressed")

    client.close()


