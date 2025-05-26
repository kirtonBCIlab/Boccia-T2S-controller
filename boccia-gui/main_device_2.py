import sys
from PyQt5.QtWidgets import QApplication
from device_2_window import Device2Window

def main():
    app = QApplication(sys.argv)
    mainWindow = Device2Window()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()