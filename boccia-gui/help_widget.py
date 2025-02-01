from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget
import webbrowser
from styles import Styles


class HelpWidget(QWidget):
    HELP_URL = "http://example.com/help"

    def __init__(self, parent=None):
        super(HelpWidget, self).__init__(parent)

        # Create the help button
        self.help_button = QPushButton("Help")

        # Apply the same style as other buttons
        self.help_button.setStyleSheet(Styles.BUTTON_BASE)

        # Create a layout and add the button to it
        layout = QHBoxLayout()
        layout.addStretch()  # Add a stretch to push the button to the right
        layout.addWidget(self.help_button)

        # Set the layout for the widget
        self.setLayout(layout)
        self.help_button.clicked.connect(self.open_help_url)

    def open_help_url(self):
        webbrowser.open(self.HELP_URL)
