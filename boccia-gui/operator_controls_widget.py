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

class OperatorControlsWidget(QWidget):
    hold_button_service_flag_changed = pyqtSignal(bool)
    remap_mode_requested = pyqtSignal()
    remap_target_selected = pyqtSignal(str, str)

    def __init__(self, serial_handler = None, commands = None):
        super().__init__()

        self.serial_handler = serial_handler
        self.commands = commands

        self.default_speeds = {
            "elevation": 50,
            "rotation": 50
        }

        self.action_buttons = []
        self.operator_button_actions = {}
        self.remap_mode_active = False
        
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

        for button in self.action_buttons:
            button.installEventFilter(self)

        self.service_flag = False


    def _create_operator_controls(self):
        """ Initialize UI elements for operator controls"""

        # Create buttons
        up_button = self._create_operator_button(self._format_hold_button_text("elevation_up"), "elevation_up")
        down_button = self._create_operator_button(self._format_hold_button_text("elevation_down"), "elevation_down")
        left_button = self._create_operator_button(self._format_hold_button_text("rotation_left"), "rotation_left")
        right_button = self._create_operator_button(self._format_hold_button_text("rotation_right"), "rotation_right")
        drop_button = self._create_drop_button(self._format_drop_button_text(), "drop")
        
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

        self.config_controls_button = QPushButton("Configure Controls")
        self.config_controls_button.setStyleSheet(Styles.HOVER_BUTTON)
        self.config_controls_button.clicked.connect(self._handle_config_button_clicked)

        operator_controls_layout = QVBoxLayout()
        operator_controls_layout.addLayout(buttons_layout)
        operator_controls_layout.addWidget(self.config_controls_button)

        # Adding the buttons to the layout
        return operator_controls_layout


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
    

    def _create_operator_button(self, button_text:str = "", action:str = ""):
        """ Returns the operator buttons for the hold commands """

        button_style = f"{Styles.HOVER_BUTTON} width: {50 * Styles.SCALE_FACTOR}px; height: {50 * Styles.SCALE_FACTOR}px;"
        button = QPushButton(button_text)
        button.setStyleSheet(button_style)
        button.clicked.connect(self._handle_button_clicked)
        self.action_buttons.append(button)
        self.operator_button_actions[button] = action

        return button
    

    def _create_drop_button(self, button_text:str = "", action:str = ""):
        """ Returns the drop button for the operator controls """

        button_style = f"{Styles.HOVER_BUTTON} width: {50 * Styles.SCALE_FACTOR}px; height: {50 * Styles.SCALE_FACTOR}px;"
        button = QPushButton(button_text)
        button.setStyleSheet(button_style)
        button.clicked.connect(self._handle_drop_click)
        self.action_buttons.append(button)
        self.operator_button_actions[button] = action

        return button
    

    def _handle_button_clicked(self):
        """ Handle the operator button click """
        sender = self.sender()
        action = self.operator_button_actions.get(sender)
        if self.remap_mode_active and action:
            self.remap_target_selected.emit("hold", action)
            return

        command = self.commands.get_hold_command_for_action(action)
        # print(f"\nOperator button clicked: {sender.text()}")

        # If the command is in the list, send it
        if command:
            self.serial_handler.send_command(command)

        # Update service flag
        self._update_service_flag(not self.service_flag)

        command_action = "Start" if self.service_flag else "Stop"
        #print(f"{command_action} {command} command")

        for button in self.action_buttons:
            if button != sender:
                button.setEnabled(not button.isEnabled())

            self._update_button_style(button)


    def _handle_drop_click(self):
        if self.remap_mode_active:
            self.remap_target_selected.emit("toggle", "drop")
            return
        # print("Operator drop button clicked")
        # Send the command
        command = self.commands.get_toggle_command_for_action("drop")
        self.serial_handler.send_command(command)
        # print(f"Sent command: {command}")

        # Update service flag
        self._update_service_flag(True)

        self.commands.drop_delay_timer()
        self._toggle_all_buttons(False)
        
    
    def _toggle_all_buttons(self, is_enable):
        for button in self.action_buttons:
            button.setEnabled(is_enable)
            self._update_button_style(button)


    def _update_button_style(self, button):
        """ Update the button style based on its enabled state """
        if button.isEnabled():
            button_style = f"{Styles.HOVER_BUTTON} width: {50 * Styles.SCALE_FACTOR}px; height: {50 * Styles.SCALE_FACTOR}px;"
            button.setStyleSheet(button_style)
        else:
            button_style = f"{Styles.DISABLED_BUTTON} width: {50 * Styles.SCALE_FACTOR}px; height: {50 * Styles.SCALE_FACTOR}px;"
            button.setStyleSheet(button_style)


    def set_remap_mode_active(self, is_active: bool):
        self.remap_mode_active = is_active
        if is_active:
            self.config_controls_button.setText("Configure Controls (On)")
        else:
            self.config_controls_button.setText("Configure Controls")


    def refresh_key_labels(self):
        for button, action in self.operator_button_actions.items():
            if action == "drop":
                button.setText(self._format_drop_button_text())
            else:
                button.setText(self._format_hold_button_text(action))


    def _format_hold_button_text(self, action):
        arrow_map = {
            "elevation_up": "↑",
            "elevation_down": "↓",
            "rotation_left": "←",
            "rotation_right": "→",
            }
        key_text = self.commands.get_key_text(self.commands.get_hold_key_for_action(action))
        arrow = arrow_map.get(action, "")
        return f"{key_text} {arrow}".strip()


    def _format_drop_button_text(self):
        key_text = self.commands.get_key_text(self.commands.get_toggle_key_for_action("drop"))
        return f"Drop \n({key_text})"


    def _handle_config_button_clicked(self):
        self.remap_mode_requested.emit()


    def _receive_service_flag(self, flag: bool):
        self.service_flag = flag # toggle the service flag
        self._toggle_all_buttons(not flag) # toggle the buttons
        # print(f"Operator controls service flag: {self.service_flag}")


    def _reset_buttons_and_flag(self):
        self._toggle_all_buttons(True)
        self._update_service_flag(False)

    
    def _update_service_flag(self, flag: bool):
        self.service_flag = flag
        self.hold_button_service_flag_changed.emit(self.service_flag)
        # print(f"Operator controls service flag: {self.service_flag}")


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