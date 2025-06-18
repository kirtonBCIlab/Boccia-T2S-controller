# Standard libraries
from PyQt5.QtWidgets import QComboBox

class CustomComboBox(QComboBox):
    def __init__(self, parent=None, on_mouse_press = None):
        super().__init__(parent)

        self.on_mouse_press = on_mouse_press

    def mousePressEvent(self, event):
        """
            Override the mousePressEvent method to populate the ports list
            when the user clicks on the combo box.
        """
        if self.on_mouse_press is not None:
            self.on_mouse_press()
        super().mousePressEvent(event)