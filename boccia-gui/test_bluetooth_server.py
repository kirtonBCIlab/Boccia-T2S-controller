import socket


class BluetoothServer:
    def __init__(self, address):
        self.address = address
        self.server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.server.bind((self.address, 4))
        self.server.listen(1)

    def accept_client(self):
        self.client, self.client_address = self.server.accept()
        print(f"Accepted connection from client")

    def send_message(self, message):
        try:
            data = self.client.recv(1024)
            if not data:
                return
            print(f"Message: {data.decode('utf-8')}")
            self.client.send(message.encode("utf-8"))
        except OSError as e:
            print(f"Error sending message: {e}")

    def close(self):
        if hasattr(self, 'client'):
            self.client.close()
        self.server.close()

if __name__ == "__main__":
    server = BluetoothServer("E8:9C:25:5D:AA:42")
    server.accept_client()

    key = input("Press 1 to send message: ")
    if key == '1':
        server.send_message("Test message from server")
    else:
        print("Invalid key pressed")
        
    server.close()