from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
)

# Custom libraries
from styles import Styles

class MultiplayerInstructionsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Main label section
        self.instructions_label = QLabel('INSTRUCTIONS')
        self.instructions_label.setStyleSheet(Styles.MAIN_LABEL)

        # Content section
        self._create_instructions_section()

        # Organize layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.instructions_label)
        self.main_layout.addLayout(self.instructions_section_layout)

    def _create_instructions_section(self):
        self.instructions_title = QLabel("Follow these steps to setup the devices for Multiplayer Mode:")
        self.instructions_title.setStyleSheet(Styles.INSTRUCTIONS_TEXT)

        instructions_text = (
            "1. Pair the devices in Bluetooth settings.<br>"
            "2. Make sure Bluetooth remains turned on for all devices.<br>"
            "3. In the Main Device app:<br>"
            "&nbsp;&nbsp;&nbsp;a) Click 'Turn ON Multiplayer Mode'.<br>"
            "&nbsp;&nbsp;&nbsp;b) Select the number of players in the dropdown menu.<br>"
            "&nbsp;&nbsp;&nbsp;c) Click 'Connect'.<br>"
            "&nbsp;&nbsp;&nbsp;d) Wait until the status says 'Waiting for other devices'.<br>"
            "4. In the Multiplayer Device app (this app):<br>"
            "&nbsp;&nbsp;&nbsp;a) Click the dropdown menu to see the list of paired Bluetooth devices. "
            "Please wait a few seconds for the list to update.<br>"
            "&nbsp;&nbsp;&nbsp;b) Select the name of the Main Device.<br>"
            "&nbsp;&nbsp;&nbsp;c) Click 'Connect'."
        )
        self.instructions = QLabel(instructions_text)
        self.instructions.setStyleSheet(Styles.INSTRUCTIONS_TEXT)
        self.instructions.setTextFormat(Qt.RichText)
        self.instructions.setWordWrap(True)

        self.instructions_section_layout = QVBoxLayout()
        self.instructions_section_layout.addWidget(self.instructions_title)
        self.instructions_section_layout.addWidget(self.instructions)