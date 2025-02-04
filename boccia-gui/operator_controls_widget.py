# Standard libraries
from PyQt5.QtCore import Qt, pyqtSignal
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
from commands import Commands

class OperatorControlsWidget(QWidget):
    hold_button_service_flag_changed = pyqtSignal(bool)

    def __init__(self, serial_handler = None, commands = None):
        super().__init__()

        self.serial_handler = serial_handler
        self.commands = commands

        self.default_speeds = {
            "elevation": 50,
            "rotation": 50
        }

        self.operator_buttons = []
        
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

        for button in self.operator_buttons:
            button.installEventFilter(self)

        self.service_flag = False


    def _create_operator_controls(self):
        """ Initialize UI elements for operator controls"""

        # Create buttons
        up_button = self._create_hold_button('W ↑')
        down_button = self._create_hold_button('S ↓')
        left_button = self._create_hold_button('A ←')
        right_button = self._create_hold_button('→ D')
        drop_button = self._create_drop_button('Drop \n(R)')
        
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
    

    def _create_hold_button(self, button_text:str = ""):
        """ Returns the operator buttons for the hold commands """

        button_style = f"{Styles.HOVER_BUTTON} width: 50px; height: 50px;"
        button = QPushButton(button_text)
        button.setStyleSheet(button_style)
        self.operator_buttons.append(button)
        # button.setEnabled(False)

        return button
    

    def _create_drop_button(self, button_text:str = ""):
        """ Returns the drop button for the operator controls """

        button_style = f"{Styles.HOVER_BUTTON} width: 50px; height: 50px;"
        button = QPushButton(button_text)
        button.setStyleSheet(button_style)
        button.clicked.connect(self._handle_drop_click)

        return button

    def eventFilter(self, obj, event):
        if obj in self.operator_buttons:
            # Block mouse events if buttons are disabled
            if not obj.isEnabled():
                if event.type() in {event.MouseButtonPress, event.MouseButtonRelease}:
                    return True # Block mouse events if buttons are disabled
                return False
            
            if (event.type() == event.MouseButtonPress):
                # print(f"Operator button pressed: {obj.text()}")
                self._handle_button_event(obj, True)
                return True
            elif (event.type() == event.MouseButtonRelease):
                # print(f"Operator button released: {obj.text()}")
                self._handle_button_event(obj, False)
                return True
        
        return super().eventFilter(obj, event)
    
    def _handle_button_event(self, button, is_pressed):
        button_text = button.text()

        if (button_text in Commands.OPERATOR_COMMANDS):
            # Send the command
            command = Commands.OPERATOR_COMMANDS.get(button.text())
            self.serial_handler.send_command(command)

            # Update service flag
            self._update_service_flag(is_pressed)

            command_action = "Start" if is_pressed else "Stop"
            print(f"{command_action} {command} command")


    def _handle_drop_click(self):
        # print("Operator drop button clicked")
        # Send the command
        command = Commands.OPERATOR_COMMANDS.get("Drop \n(R)")
        self.serial_handler.send_command(command)
        # print(f"Sent command: {command}")

        # Update service flag
        self._update_service_flag(True)

        self.commands.drop_delay_timer()
        self._toggle_all_buttons(False)
        
    
    def _toggle_all_buttons(self, is_enable):
        for button in self.findChildren(QPushButton):
            button.setEnabled(is_enable)
            self._update_button_style(button)

    def _reset_buttons_and_flag(self):
        self._toggle_all_buttons(True)
        self._update_service_flag(False)

    
    def _update_button_style(self, button):
        """ Update the button style based on its enabled state """
        if button.isEnabled():
            button_style = f"{Styles.HOVER_BUTTON} width: 50px; height: 50px;"
            button.setStyleSheet(button_style)
        else:
            button_style = f"{Styles.DISABLED_BUTTON} width: 50px; height: 50px;"
            button.setStyleSheet(button_style)


    def _receive_service_flag(self, flag):
        self.service_flag = flag
        self._toggle_all_buttons(not flag)

    
    def _update_service_flag(self, flag):
        self.service_flag = flag
        self.hold_button_service_flag_changed.emit(self.service_flag)

    def _change_slider_label(self, slider, label):
        """ Update the slider value label """
        label.setText(f"{slider.value()} %")


    def _handle_slider_released(self, slider, name):
        """ Send the slider value to the serial port """
        if self.serial_handler.get_current_connection_status() == "Connected":
            if name == "elevation":
                speed_command = self._set_elevation_speed(slider.value())
            elif name == "rotation":
                speed_command = self._set_rotation_accel(slider.value())

            self.serial_handler.send_command(f"{speed_command}")
        pass


    def _set_rotation_accel(self, value):
        """ Set the rotation acceleration [steps/sec^2] """
        MAX_ACCEL = 30 # Maximum recommended [steps/sec^2]

        speed = int((value / 100) * MAX_ACCEL)
        speed_command = f"rx{speed}"

        return speed_command


    def _set_elevation_speed(self, value):
        """ 
            Set the elevation speed [steps/sec]. The speed is mapped the value 
            to the range [51 - 255] i.e. 20-100% of the speed range because
            the motor does not move if pulses are below 20% of max speed.
        """
        MAX_SPEED = 255 # Maximum speed 8-bit PWM
        MIN_SPEED = MAX_SPEED * 0.2 # Minimum speed (20% of the max speed)

        speed_range = MAX_SPEED - MIN_SPEED
        input_value_range = 100

        mapped_speed = int(MIN_SPEED + (speed_range / input_value_range) * value)

        speed_command = f"ex{mapped_speed}"
        
        return speed_command