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
    server = BluetoothServer("E8:9C:25:5D:AA:42")
    try:
        server.accept_client()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    finally:
        server.close()