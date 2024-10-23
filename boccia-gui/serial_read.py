import sys
import threading
from PyQt5.QtWidgets import QDialog, QScrollArea, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QObject

class SerialReadThread(QObject, threading.Thread):
    newData = pyqtSignal(str)

    def __init__(self, serial_connection):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        self.serial_connection = serial_connection
        self._running = True

    def run(self):
        while self._running and self.serial_connection.is_open:
            data = self.serial_connection.readline().decode('utf-8').strip()
            if data:
                self.newData.emit(data)

    def stop(self):
        self._running = False

class SerialReadWindow(QDialog):
    def __init__(self, serial_connection):
        super().__init__()
        self.serial_connection = serial_connection
        self.initUI()

    def initUI(self):
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setWindowTitle('Serial Port Reader')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.outputLabel = QLabel('Reading data from serial port\n')
        self.outputLabel.setWordWrap(True)  # Ensure text wraps within the label
        self.scroll.setWidget(self.outputLabel)
        self.scroll.setWidgetResizable(True)  # Ensure the scroll area resizes with the content

        layout.addWidget(self.scroll)
        self.setLayout(layout)

        self.thread = SerialReadThread(self.serial_connection)
        self.thread.newData.connect(self.updateOutput)
        self.thread.start()

    def updateOutput(self, data):
        print(data)  # Print to terminal
        self.outputLabel.setText(self.outputLabel.text() + data + '\n')

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()
