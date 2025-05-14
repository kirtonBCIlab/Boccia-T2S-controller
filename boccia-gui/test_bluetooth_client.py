from PyQt5.QtCore import QObject, QTimer, QCoreApplication
from PyQt5.QtBluetooth import QBluetoothSocket, QBluetoothUuid, QBluetoothServiceInfo, QBluetoothAddress
from PyQt5.QtWidgets import QApplication

class BluetoothClient(QObject):
    def __init__(self, address):
        super().__init__()
        self.socket = QBluetoothSocket(QBluetoothServiceInfo.RfcommProtocol)
        self.socket.readyRead.connect(self.on_data_received)
        self.socket.connected.connect(self.on_connected)
        self.socket.error.connect(lambda error: print(f"Socket error: {error}"))

        bluetooth_address = QBluetoothAddress(address)
        self.socket.connectToService(bluetooth_address, QBluetoothUuid.SerialPort)
        print("Connecting to Bluetooth device...")

    def on_connected(self):
        print("Connected to server")
        self.socket.write(b"Test message\n")

    def on_data_received(self):
        while self.socket.canReadLine():
            data = self.socket.readLine().data().decode().strip()
            print(f"Received data: {data}")

if __name__ == "__main__":
    app = QCoreApplication([])
    server_address = "E8:9C:25:5D:AA:42"
    client = BluetoothClient(server_address)

    QTimer.singleShot(10000, app.quit)  # Auto-quit after 10 seconds for testing purposes
    
    app.exec_()