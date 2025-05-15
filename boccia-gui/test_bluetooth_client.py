import socket

class BluetoothClient:
    def __init__(self, address):
        self.address = address
        self.client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    def start_connection(self):
        self.client.connect((self.address, 4))
        print(f"Connected to server")
        self.run()
    
    def run(self):
        try:
            while True:
                message = input("Enter message:")
                client.send(message.encode("utf-8"))
                data = client.recv(1024)
                if not data:
                    break
                print(f"Message: {data.decode('utf-8')}")
        except OSError as e:
            pass

    def close(self):
        self.client.close()
        print("Connection closed")

if __name__ == "__main__":
    client = BluetoothClient("E8:9C:25:5D:AA:42")
    client.start_connection()
    client.close()


