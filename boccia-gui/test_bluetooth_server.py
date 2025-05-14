from PyQt5.QtCore import QObject, QCoreApplication, QTimer, pyqtSlot
from PyQt5.QtBluetooth import QBluetoothServer, QBluetoothServiceInfo, QBluetoothUuid, QBluetoothLocalDevice
from PyQt5.QtWidgets import QApplication

class BluetoothServer(QObject):
    def __init__(self):
        super().__init__()
        self.local_device = QBluetoothLocalDevice()
        self.local_device.powerOn()

        self.bluetooth_server = QBluetoothServer(QBluetoothServiceInfo.RfcommProtocol)
        self.bluetooth_server.newConnection.connect(self.handle_new_connection)

        self.service_info = QBluetoothServiceInfo()
        self.service_info.setServiceUuid(QBluetoothUuid(QBluetoothUuid.SerialPort))
        self.service_info.setServiceName("Bluetooth Test Server")
        self.service_info.setServiceDescription("Testing Bluetooth server")
        self.service_info.setServiceProvider("PyQt5")
        self.service_info.setDevice(self.local_device.address())
        self.service_info.setServiceUuid(QBluetoothUuid(QBluetoothUuid.SerialPort))
        
        self.bluetooth_server.listen(self.local_device.address())
        self.service_info.registerService(self.local_device.address())
        
        print("Bluetooth server started...")
        
    @pyqtSlot()
    def handle_new_connection(self):
        self.socket = self.bluetooth_server.nextPendingConnection()
        self.socket.readyRead.connect(self.read_data)
        print("New connection established")

    def read_data(self, socket):
        while self.socket.canReadLine():
            data = bytes(self.socket.readLine()).decode("utf-8").strip()
            print(f"Received data: {data}")
        
if __name__ == "__main__":
    app = QApplication([])
    server = BluetoothServer()

    QTimer.singleShot(60000, app.quit)  # Auto-quit after 60 seconds for testing purposes

    app.exec_()