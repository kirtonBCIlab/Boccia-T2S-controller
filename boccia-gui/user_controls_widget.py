# Standard libraries
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,    
    QVBoxLayout,
    QLabel,
    QPushButton,
    )

# Custom libraries
from styles import Styles
from commands import Commands


class UserControlsWidget(QWidget):
    button_service_flag_changed = pyqtSignal(bool)
    remap_target_selected = pyqtSignal(str, str)

    def __init__(self, serial_handler = None, commands = None):
        super().__init__()

        self.serial_handler = serial_handler
        self.commands = commands

        self.remap_mode_active = False
        self.command_buttons = []
        self.command_button_actions = {}
        self.command_button_labels = {}

        # Main label section
        self.controls_label = QLabel('USER CONTROLS')
        self.controls_label.setStyleSheet(Styles.MAIN_LABEL)

        # Content section
        self._create_commands_section()

        # Organize layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.controls_label)
        self.main_layout.addLayout(self.commands_section_layout)

        self.service_flag = False

    def _create_commands_section(self):
        # Create commands labels
        command_label_layout = QVBoxLayout()
        command_button_layout = QVBoxLayout()

        action_map = {
            "Elevation up": "elevation_up",
            "Rotation right": "rotation_right",
            "Drop": "drop",
            }

        for [c, command_text] in enumerate(Commands.BUTTON_COMMANDS.keys()):
            action = action_map.get(command_text, "")
            command_label = self._create_command_label(self._format_command_label(action, c + 1))
            command_button = self._create_command_button(command_text, action)
            command_label_layout.addWidget(command_label)
            command_button_layout.addWidget(command_button)
            self.command_buttons.append(command_button)
            self.command_button_actions[command_button] = action
            self.command_button_labels[command_button] = command_label

        # Organize layout
        self.commands_section_layout = QHBoxLayout()
        self.commands_section_layout.addLayout(command_label_layout)
        self.commands_section_layout.addLayout(command_button_layout)


    def _create_command_label(self, label_text:str = ""):
        """ Create a QLabel for the command  and sets the default style """
        label = QLabel(label_text)
        label.setStyleSheet(Styles.LABEL_TEXT)
        return label
    
    
    def _create_command_button(self, button_text:str = "", action:str = ""):
        """ Create a QPushButton for the command and sets the default style """
        button = QPushButton(button_text)
        button.setStyleSheet(Styles.HOVER_BUTTON)
        button.clicked.connect(self._handle_command_click)

        return button
    

    def _handle_command_click(self):
        """ Handle the command button click """
        sender = self.sender()
        command = Commands.BUTTON_COMMANDS.get(sender.text())
        # print(f"\nUser button clicked: {sender.text()}")

        action = self.command_button_actions.get(sender)
        if self.remap_mode_active and action:
            self.remap_target_selected.emit("toggle", action)
            return

        # If the command is in the list, send it
        if command:
            self.serial_handler.send_command(command)

        # If the command is "Drop", disable all buttons
        if sender.text() == "Drop":
            # Update service flag
            self._update_service_flag(True)

            self.commands.drop_delay_timer() # Start the drop delay timer
            self._toggle_all_buttons(False)

        # If elevation or rotation, toggle the service flag and the other buttons
        else:
            self._update_service_flag(not self.service_flag)

            command_action = "Start" if self.service_flag else "Stop"
            #print(f"{command_action} {command} command")
            
            for button in self.command_buttons:
                if button != sender:
                    button.setEnabled(not button.isEnabled())

                self._update_button_style(button)

    def _update_button_style(self, button):
        """ Update the button style based on its enabled state """
        if button.isEnabled():
            button.setStyleSheet(Styles.HOVER_BUTTON)
        else:
            button.setStyleSheet(Styles.DISABLED_BUTTON)
    
    def _toggle_all_buttons(self, value):
        for button in self.command_buttons:
            button.setEnabled(value)
            self._update_button_style(button)

    def _receive_service_flag(self, flag: bool):
        self.service_flag = flag # toggle the service flag
        self._toggle_all_buttons(not flag) # toggle the buttons
        # print(f"User controls service flag: {self.service_flag}")

    def _reset_buttons_and_flags(self):
        self._toggle_all_buttons(True) # Re-enable the buttons
        self.service_flag = False # Reset the service flag

    def _update_service_flag(self, flag: bool):
        self.service_flag = flag
        self.button_service_flag_changed.emit(flag)
        # print(f"User controls service flag: {self.service_flag}")

    def set_remap_mode_active(self, is_active: bool):
        self.remap_mode_active = is_active

    def refresh_key_labels(self):
        for button, label in self.command_button_labels.items():
            action = self.command_button_actions.get(button)
            label.setText(self._format_command_label(action))

    def _format_command_label(self, action, fallback_index=None):
        key_text = self.commands.get_key_text(self.commands.get_toggle_key_for_action(action))
        if key_text == "?" and fallback_index is not None:
            return f"Command: {fallback_index}"
        return f"Command: {key_text}"