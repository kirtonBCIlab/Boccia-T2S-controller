import sys
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QSlider, QWidget, QLabel
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 GUI Test")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        layout = QGridLayout()

        self.up_button = QPushButton("Up")
        self.up_button.clicked.connect(self.on_up_button_clicked)

        self.down_button = QPushButton("Down")
        self.down_button.clicked.connect(self.on_down_button_clicked)

        self.left_button = QPushButton("Left")
        self.left_button.clicked.connect(self.on_left_button_clicked)

        self.right_button = QPushButton("Right")
        self.right_button.clicked.connect(self.on_right_button_clicked)

        # Set the sliders
        self.height_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.height_speed_slider.setRange(0, 100)

        self.rotation_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_speed_slider.setRange(0, 100)

        # Set the labels
        self.height_speed_label = QLabel("Height Speed")
        self.rotation_speed_label = QLabel("Rotation Speed")

        # Set the minimum size of the sliders (width, height)
        self.height_speed_slider.setMinimumSize(100, 20)
        self.rotation_speed_slider.setMinimumSize(100, 20)

        # Set the tick position to below the slider (Ticks are the values shown below the slider)        
        layout.addWidget(self.height_speed_label, 5, 0, 1, 3)
        layout.addWidget(self.height_speed_slider, 6, 0, 1, 3)
        layout.addWidget(self.rotation_speed_label, 7, 0, 1, 3)
        layout.addWidget(self.rotation_speed_slider, 8, 0, 1, 3)

        # Add the widgets to the layout (2 rows, 3 columns)
        layout.addWidget(self.up_button, 1, 1)
        layout.addWidget(self.down_button, 3, 1)
        layout.addWidget(self.left_button, 2, 0)
        layout.addWidget(self.right_button, 2, 2)
        layout.addWidget(self.height_speed_slider, 4, 0, 1, 3)
        layout.addWidget(self.rotation_speed_slider, 5, 0, 1, 3)

        # Set the button colors
        self.up_button.setStyleSheet("background-color: white; color: black; font-size: 15px;")
        self.down_button.setStyleSheet("background-color: white; color: black; font-size: 15px;")
        self.left_button.setStyleSheet("background-color: white; color: black; font-size: 15px;")
        self.right_button.setStyleSheet("background-color: white; color: black; font-size: 15px;")

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    
    # Add button click event
    def on_up_button_clicked(self):
        print("Up button clicked")

    def on_down_button_clicked(self):
        print("Down button clicked")

    def on_left_button_clicked(self):
        print("Left button clicked")

    def on_right_button_clicked(self):
        print("Right button clicked")

        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.up_button.click()
        super().keyPressEvent(event)  # Propagate the key event to the super class


    # Add key press event
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.up_action()
        elif event.key() == Qt.Key.Key_Down:
            self.down_action()
        elif event.key() == Qt.Key.Key_Left:
            self.left_action()
        elif event.key() == Qt.Key.Key_Right:
            self.right_action()

    def up_action(self):
        print("Up key pressed")
        # Add your specific action here

    def down_action(self):
        print("Down key pressed")
        # Add your specific action here

    def left_action(self):
        print("Left key pressed")
        # Add your specific action here

    def right_action(self):
        print("Right key pressed")
        # Add your specific action here

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())