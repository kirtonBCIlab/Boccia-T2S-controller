import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow(include_multiplayer_controls=True)
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
