# Standard libraries
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    )

# Custom libraries
from styles import Styles

class OperatorControlsWidget(QWidget):
    def __init__(self, serial_handler = None):
        super().__init__()

        self.serial_handler = serial_handler

        self.default_speeds = {
            "elevation": 50,
            "rotation": 50
        }
        
        # Main label section   
        self.controls_label = QLabel('OPERATOR CONTROLS')
        self.controls_label.setStyleSheet(Styles.MAIN_LABEL)
        
        # Content section
        self.operator_controls_layout = self._create_operator_controls()
        self.speed_controls_layout = self._create_speed_controls()

        self.content_layout = QHBoxLayout()
        self.content_layout.addLayout(self.operator_controls_layout)
        self.content_layout.addLayout(self.speed_controls_layout)

        # Organize layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.controls_label)
        self.main_layout.addLayout(self.content_layout)


    def _create_operator_controls(self):
        """ Initialize UI elements for operator controls"""

        # Create buttons
        up_button = self._create_static_button('W ↑')
        down_button = self._create_static_button('S ↓')
        left_button = self._create_static_button('A ←')
        right_button = self._create_static_button('→ D')
        drop_button = self._create_static_button('Drop \n(R)')
        
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


    def _create_speed_controls(self):
        """ create UI elements and widgets for speed controls"""

        # Create layouts
        height_layout = self._create_slider_layout("elevation")
        rotation_layout = self._create_slider_layout("rotation")

        # Organize layouts
        speed_controls_layout = QVBoxLayout()
        speed_controls_layout.addLayout(height_layout)
        speed_controls_layout.addLayout(rotation_layout)

        return speed_controls_layout


    def _create_slider_layout(self, name):
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
        slider.setStyleSheet(Styles.SLIDER)
        
        # Slider actions
        slider.valueChanged.connect(lambda: self._change_slider_label(slider, value_label))
        slider.sliderReleased.connect(lambda: self._handle_slider_released(slider, name))

        # Organize layout
        slider_layout = QVBoxLayout()
        slider_layout.addLayout(slider_label_layout)
        slider_layout.addWidget(slider)

        return slider_layout
    

    def _create_static_button(self, button_text):
        """ Returns a static button """

        button_style = f"{Styles.BUTTON_BASE} width: 50px; height: 50px;"

        button = QPushButton(button_text)
        button.setStyleSheet(button_style)
        button.setEnabled(False)

        return button
    

    def _change_slider_label(self, slider, label):
        """ Update the slider value label """
        label.setText(f"{slider.value()} %")


    def _handle_slider_released(self, slider, name):
        """ Send the slider value to the serial port """
        if self.serial_handler.get_current_connection_status() == "Connected":
            if name == "elevation":
                speed_command = self._set_elevation_speed(slider.value())
            elif name == "rotation":
                speed_command = self._set_rotation_speed(slider.value())

            self.serial_handler.send_command(f"{speed_command}")
        pass


    def _set_rotation_speed(self, value):
        """ Set the rotation speed [steps/sec] """
        MAX_SPEED = 1000 # Maximum recommended [steps/sec]

        speed = int((value / 100) * MAX_SPEED)
        speed_command = f"rx{speed}"

        return speed_command


    def _set_elevation_speed(self, value):
        """ Set the elevation speed [0 - 255] """
        MAX_SPEED = 255 # Maximum speed 8-bit PWM

        speed = int((value / 100) * MAX_SPEED)
        speed_command = f"ex{speed}"
        
        return speed_command