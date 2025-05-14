from PyQt5.QtCore import QObject, QTimer, QCoreApplication
from PyQt5.QtBluetooth import QBluetoothSocket, QBluetoothUuid, QBluetoothServiceInfo, QBluetoothAddress
from PyQt5.QtWidgets import QApplication

class BluetoothClient(QObject):
    def __init__(self, address):
        super().__init__()
        self.socket = QBluetoothSocket(QBluetoothServiceInfo.RfcommProtocol)
        self.socket.connected.connect(self.send_test_message)
        self.socket.error.connect(self.handle_error)

        print(f"Connecting to {address}...")
        self.socket.connectToService(address, QBluetoothUuid.SerialPort)

    def send_test_message(self):
        message = "Test message sent from client\n"
        print(f"Sending: {message}")
        QTimer.singleShot(2000, QCoreApplication.quit)  # Auto-quit after sending the message

    def handle_error(self, error):
        print(f"Error: {self.socket.errorString()}")
        QCoreApplication.quit()

if __name__ == "__main__":
    app = QCoreApplication([])
    address = "48:E7:DA:81:33:68"
    client = BluetoothClient(address)

    QTimer.singleShot(60000, app.quit)  # Auto-quit after 60 seconds for testing purposes
    
    app.exec_()