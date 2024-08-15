from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.send_button = QPushButton('Update Controls')
        self.send_button.setStyleSheet("""
                                        QPushButton {
                                            font-size: 16px;
                                            background-color: #3c3c3c;
                                            color: #ffffff;
                                            border: 1px solid #ffffff;
                                        }
                                        QPushButton:hover {
                                            background-color: #555555;
                                        }
                                    """)

        self.commandAcombobox = QComboBox()
        self.commandAcombobox.addItems(['Option 1', 'Option 2', 'Option 3'])

        self.commandAcombobox.currentIndexChanged.connect(self.on_combobox_changed)
        self.send_button.clicked.connect(self.on_button_clicked)

        self.is_green = False  # Flag to track the button's color state

        layout = QVBoxLayout()
        layout.addWidget(self.commandAcombobox)
        layout.addWidget(self.send_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_combobox_changed(self):
        self.send_button.setStyleSheet("""
                                        QPushButton {
                                            font-size: 16px;
                                            background-color: green;
                                            color: #ffffff;
                                            border: 1px solid #ffffff;
                                        }
                                        QPushButton:hover {
                                            background-color: #555555;
                                        }
                                    """)
        self.is_green = True  # Set the flag to indicate the button is green

    def on_button_clicked(self):
        if self.is_green:
            self.send_button.setStyleSheet("""
                                            QPushButton {
                                                font-size: 16px;
                                                background-color: #3c3c3c;
                                                color: #ffffff;
                                                border: 1px solid #ffffff;
                                            }
                                            QPushButton:hover {
                                                background-color: #555555;
                                            }
                                        """)
            self.is_green = False  # Reset the flag
        else:
            self.send_button.setStyleSheet("""
                                            QPushButton {
                                                font-size: 16px;
                                                background-color: green;
                                                color: #ffffff;
                                                border: 1px solid #ffffff;
                                            }
                                            QPushButton:hover {
                                                background-color: #555555;
                                            }
                                        """)
            self.is_green = True  # Set the flag

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()