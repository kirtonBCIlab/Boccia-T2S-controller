# Import libraries
from styles import Styles
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,    
    QVBoxLayout,
    QLabel,
    QPushButton,
    )


class UserControlsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

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
        command1 = self._create_command_label("Command 1:")
        command2 = self._create_command_label("Command 2:")
        command3 = self._create_command_label("Command 3:")
        
        command_label_layout = QVBoxLayout()
        command_label_layout.addWidget(command1)
        command_label_layout.addWidget(command2)
        command_label_layout.addWidget(command3)

        # Create commands buttons
        command1_button = self._create_command_button("Elevation up")
        command2_button = self._create_command_button("Rotation right")
        command3_button = self._create_command_button("Drop")

        command_button_layout = QVBoxLayout()
        command_button_layout.addWidget(command1_button)
        command_button_layout.addWidget(command2_button)
        command_button_layout.addWidget(command3_button)

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

        # Disable all buttons except the one clicked
        sender = self.sender()
        for button in self.findChildren(QPushButton):
            if button != sender:
                button.setEnabled(not button.isEnabled())
        pass