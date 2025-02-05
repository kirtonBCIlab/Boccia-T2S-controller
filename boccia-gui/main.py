import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1200, 800) # Scaled up by 2x from the previous (600, 400)
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
