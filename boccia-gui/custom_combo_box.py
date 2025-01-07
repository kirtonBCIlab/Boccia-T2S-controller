from PyQt5.QtWidgets import QComboBox

class CustomComboBox(QComboBox):
    def mousePressEvent(self, event):
        """
            Override the mousePressEvent method to populate the ports list
            when the user clicks on the combo box.
        """

        self.parent()._populate_ports()
        super().mousePressEvent(event)