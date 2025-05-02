from PyQt5.QtCore import QObject, QCoreApplication
from PyQt5.QtBluetooth import QBluetoothServer, QBluetoothServiceInfo, QBluetoothUuid, QBluetoothLocalDevice
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

class BluetoothServer(QObject):
    def __init__(self):
        super().__init__()
        self.bluetooth_server = QBluetoothServer(QBluetoothServiceInfo.RfcommProtocol)
        self.bluetooth_server.newConnection.connect(self.handle_new_connection)

        local_adapter = QBluetoothLocalDevice().address()
        if not self.bluetooth_server.listen(local_adapter):
            print("Failed to start Bluetooth server")
            return
        
        device = QBluetoothLocalDevice()
        address = device.address().toString()
        name = device.name()
        print(f"Device address: {address}")
        print(f"Device name: {name}")
        
        print(f"Bluetooth server started on {self.bluetooth_server.serverAddress().toString()}")

    def handle_new_connection(self):
        socket = self.bluetooth_server.nextPendingConnection()
        socket.readyRead.connect(lambda: self.data_received(socket))
        print("New connection established")

    def data_received(self, socket):
        while socket.canReadLine():
            data = socket.readLine().data().decode().strip()
            print(f"Received data: {data.strip()}")
            socket.write(data.encode() + b'\n')  # Echo back the received data
        
if __name__ == "__main__":
    app = QApplication([])
    server = BluetoothServer()

    QTimer.singleShot(10000, app.quit)  # Auto-quit after 10 seconds for testing purposes

    app.exec_()