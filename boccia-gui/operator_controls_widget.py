# Import libraries
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QGridLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    )
from styles import Styles

class OperatorControlsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.default_speeds = {
            "elevation": 50,
            "rotation": 50
        }
        
        # Main label section   
        self.controls_label = QLabel('OPERATOR CONTROLS')
        self.controls_label.setStyleSheet(Styles.MAIN_LABEL)
        
        # Content section
        self.operator_controls_layout = self.create_operator_controls()
        self.speed_controls_layout = self.create_speed_controls()

        self.content_layout = QHBoxLayout()
        self.content_layout.addLayout(self.operator_controls_layout)
        self.content_layout.addLayout(self.speed_controls_layout)

        # Organize layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.controls_label)
        self.main_layout.addLayout(self.content_layout)
        self.setLayout(self.main_layout)


    def create_operator_controls(self):
        """ Initialize UI elements for operator controls"""

        # Create buttons
        up_button = self.create_static_button('W ↑')
        down_button = self.create_static_button('S ↓')
        left_button = self.create_static_button('A ←')
        right_button = self.create_static_button('→ D')
        drop_button = self.create_static_button('Drop \n(R)')
        
        # Organize buttons in grid layout
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        buttons_layout = QGridLayout()
        buttons_layout.addItem(spacer, 0, 3)

        buttons_layout.addWidget(up_button, 0, 1)
        buttons_layout.addWidget(down_button, 2, 1)
        buttons_layout.addWidget(left_button, 1, 0)
        buttons_layout.addWidget(right_button, 1, 2)
        buttons_layout.addWidget(drop_button, 1, 1)

        buttons_layout.setColumnStretch(0, 2)
        buttons_layout.setColumnStretch(1, 2)
        buttons_layout.setColumnStretch(2, 2)

        # Adding the buttons to the layout
        return buttons_layout


    def create_speed_controls(self):
        """ create UI elements and widgets for speed controls"""

        # Create layouts
        height_layout = self.create_slider_layout("elevation")
        rotation_layout = self.create_slider_layout("rotation")

        # Organize layouts
        speed_controls_layout = QVBoxLayout()
        speed_controls_layout.addLayout(height_layout)
        speed_controls_layout.addLayout(rotation_layout)

        return speed_controls_layout


    def create_slider_layout(self, name):
        """Initialize slider with common settings"""
        
        # Labels section
        slider_label = QLabel(f"{name.capitalize()} speed:")
        slider_label.setStyleSheet(Styles.SUB_LABEL)
        
        value_label = QLabel(f"{self.default_speeds[name]} %")
        value_label.setStyleSheet(Styles.VALUE_TEXT)

        slider_label_layout = QHBoxLayout()
        slider_label_layout.addWidget(slider_label)
        slider_label_layout.addWidget(value_label)
        
        # Slider section
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(self.default_speeds[name])
        slider.setStyleSheet(
            "QSlider::groove:horizontal {background: #3c3c3c; height: 10px;}"
            "QSlider::handle:horizontal {background: #b48ead; width: 20px; margin: -5px 0;}"
            )
        
        slider.valueChanged.connect(lambda: self.change_slider_label(slider, value_label))

        # Organize layout
        slider_layout = QVBoxLayout()
        slider_layout.addLayout(slider_label_layout)
        slider_layout.addWidget(slider)

        return slider_layout
    

    def create_static_button(self, button_text):
        """ Returns a static button """

        button_style = """
        QPushButton {
            width: 50px;
            height: 50px;
            background-color: #3c3c3c;
            color: #ffffff;
            border-radius: 5px;
            border: 1px solid #ffffff;
        }
        QPushButton:hover {
            background-color: #5c5c5c;
        }
        QPushButton:pressed {
            background-color: #7c7c7c;
        }
        """

        button = QPushButton(button_text)
        button.setStyleSheet(button_style)
        button.setEnabled(False)

        return button
    

    def change_slider_label(self, slider, label):
        """ Update the slider value label """
        label.setText(f"{slider.value()} %")


    def slider_released(self, slider):
        """ Set the speed of the motor """
        pass