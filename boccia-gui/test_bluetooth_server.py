from PyQt5.QtCore import QObject, QCoreApplication
from PyQt5.QtBluetooth import QBluetoothServer, QBluetoothServiceInfo, QBluetoothUuid, QBluetoothLocalDevice
from PyQt5.QtWidgets import QApplication

class BluetoothServer(QObject):
    def __init__(self):
        super().__init__()
        self.bluetooth_server = QBluetoothServer(QBluetoothServer.RfcommProtocol)
        self.bluetooth_server.newConnection.connect(self.handle_new_connection)

        local_adapter = QBluetoothLocalDevice().address()
        if not self.server.listen(local_adapter):
            print("Failed to start Bluetooth server")
            return
        
        print(f"Bluetooth server started on {self.server.serverAddress().toString()}")

    def handle_new_connection(self):
        socket = self.server.nextPendingConnection()
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
    app.exec_()