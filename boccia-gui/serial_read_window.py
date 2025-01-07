# Standard libraries
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QScrollArea,
    QLabel,
    QVBoxLayout
    )

class SerialReadWindow(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()
        self.show()
        self.exec_()

    def init_ui(self):
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setWindowTitle('Serial Port Reader')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.output_label = QLabel('Reading data from serial port\n')
        self.output_label.setWordWrap(True)  # Ensure text wraps within the label
        self.scroll.setWidget(self.output_label)
        self.scroll.setWidgetResizable(True)  # Ensure the scroll area resizes with the content

        layout.addWidget(self.scroll)
        self.setLayout(layout)

        self.parent.serial_handler.new_data.connect(self.update_output)
        self.parent.serial_handler.start()
        self.parent.serial_controls_widget.toggle_read_serial()


    def update_output(self, data):
        print(data)  # Print to terminal
        self.output_label.setText(self.output_label.text() + data + '\n')


    def closeEvent(self, event):
        self.parent.serial_controls_widget.toggle_read_serial()
        self.parent.serial_handler.stop()
        event.accept()
