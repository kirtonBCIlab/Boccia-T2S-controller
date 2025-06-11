import sys
from PyQt5.QtWidgets import QApplication
from multiplayer_devices_window import MultiplayerDevicesWindow

def main():
    app = QApplication(sys.argv)
    mainWindow = MultiplayerDevicesWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()