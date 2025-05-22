import socket
from bt_devices import BluetoothDevices

class BluetoothClient:
    def __init__(self):
        # Initialize the class
        self.address = None
        self.server = None

    def initialize_client(self, server_address):
        self.address = server_address
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
    
    client = BluetoothClient()
    bluetooth_devices = BluetoothDevices()

    paired_devices = bluetooth_devices.get_paired_bluetooth_devices()
    if not paired_devices:
        print("No paired Bluetooth devices found.")
        exit(1)
    else:
        print("Paired Bluetooth devices:")
        for index, (name, mac, desc) in enumerate(paired_devices):
            print(f"{index + 1}. Device Name: {name}, MAC Address: {mac}, Description: {desc}")
        
        device_selection = int(input("Select a device by number: "))
        selected_device_mac = paired_devices[device_selection-1][1]
        client.initialize_client(str(selected_device_mac))
        client.start_connection()
        print(f"Connected to Device {selected_device_mac}")

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


