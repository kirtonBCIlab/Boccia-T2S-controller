import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from multiplayer_devices_window import MultiplayerDevicesWindow

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    mainWindow = MultiplayerDevicesWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()