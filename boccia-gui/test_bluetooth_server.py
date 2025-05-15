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
        self.run()

    def run(self):
        try:
            while True:
                data = self.client.recv(1024)
                if not data:
                    break
                print(f"Message: {data.decode('utf-8')}")
                message = input("Enter message:")
                self.client.send(message.encode("utf-8"))
        except OSError as e:
            pass

    def close(self):
        if hasattr(self, 'client'):
            self.client.close()
        self.server.close()

if __name__ == "__main__":
    server = BluetoothServer("E8:9C:25:5D:AA:42")
    server.accept_client()
    server.close()