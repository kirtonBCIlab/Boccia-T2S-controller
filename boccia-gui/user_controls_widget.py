# Standard libraries
from PyQt5.QtCore import QTimer
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
    def __init__(self, serial_handler = None):
        super().__init__()

        self.serial_handler = serial_handler

        # Main label section
        self.controls_label = QLabel('USER CONTROLS')
        self.controls_label.setStyleSheet(Styles.MAIN_LABEL)

        # Content section
        self._create_commands_section()

        # Organize layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.controls_label)
        self.main_layout.addLayout(self.commands_section_layout)


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

        # If the command is in the list, send it
        if command:
            self.serial_handler.send_command(command)

        # If the command is "Drop", enable all buttons except Drop
        if sender.text() == "Drop":
            for button in self.findChildren(QPushButton):
                if button != sender:
                    button.setEnabled(True)

                else:
                    button.setEnabled(False)
                    self._update_button_style(button)

                    # Re-enable button after 10 second delay
                    timer = QTimer()
                    timer.timeout.connect(lambda: button.setEnabled(True))
                    timer.start(10000) # 10000 ms = 10 seconds

                self._update_button_style(button)

        # If elevation or rotation, toggle all other buttons
        else:
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