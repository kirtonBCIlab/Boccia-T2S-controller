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

    def __init__(self, serial_handler = None, commands = None):
        super().__init__()

        self.serial_handler = serial_handler
        self.commands = commands

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

        for [c,command_text] in enumerate(Commands.BUTTON_COMMANDS.keys()):
            command_label = self._create_command_label(f"Command: {c+1}")
            command_button = self._create_command_button(command_text)
            command_label_layout.addWidget(command_label)
            command_button_layout.addWidget(command_button)

        # Organize layout
        self.commands_section_layout = QHBoxLayout()
        self.commands_section_layout.addLayout(command_label_layout)
        self.commands_section_layout.addLayout(command_button_layout)


    def _create_command_label(self, label_text:str = ""):
        """ Create a QLabel for the command  and sets the default style """
        label = QLabel(label_text)
        label.setStyleSheet(Styles.LABEL_TEXT)
        return label
    
    
    def _create_command_button(self, button_text:str = ""):
        """ Create a QPushButton for the command and sets the default style """
        button = QPushButton(button_text)
        button.setStyleSheet(Styles.HOVER_BUTTON)
        button.clicked.connect(self._handle_command_click)

        return button
    

    def _handle_command_click(self):
        """ Handle the command button click """
        sender = self.sender()
        command = Commands.BUTTON_COMMANDS.get(sender.text())
        print(f"\nUser button clicked: {sender.text()}")

        # If the command is in the list, send it
        if command:
            self.serial_handler.send_command(command)
            print(f"Sent command: {command}")

        # If the command is "Drop", disable all buttons
        if sender.text() == "Drop":
            self.service_flag = True # Set the service flag
            self._send_service_flag(self.service_flag)

            self.commands.drop_delay_timer() # Start the drop delay timer
            self._toggle_all_buttons(False)

        # If elevation or rotation, toggle the service flag and the other buttons
        else:
            self.service_flag = not self.service_flag # toggle the service flag
            self._send_service_flag(self.service_flag)
            
            for button in self.findChildren(QPushButton):
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
        for button in self.findChildren(QPushButton):
            button.setEnabled(value)
            self._update_button_style(button)

    def _on_key_toggled(self, flag: bool):
        self.service_flag = flag # toggle the service flag
        self._toggle_all_buttons(not flag) # toggle the buttons
        # print(f"User controls service flag: {self.service_flag}")

    def _reset_buttons_and_flags(self):
        self._toggle_all_buttons(True) # Re-enable the buttons
        self.service_flag = False # Reset the service flag

    def _send_service_flag(self, flag: bool):
        # print(f"User controls service flag: {flag}")
        self.button_service_flag_changed.emit(flag)