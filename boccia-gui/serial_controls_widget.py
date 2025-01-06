# Import libraries
from styles import Styles
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QSizePolicy
    )

class SerialConnectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Settings
        self.connect_button_styles = {
            "connect": f"{Styles.BUTTON_BASE} background-color: green;",
            "disconnect": f"{Styles.BUTTON_BASE} background-color: red;"
        }
    
        # Main label section
        self.main_label = QLabel('SERIAL CONNECTION')
        self.main_label.setStyleSheet(Styles.MAIN_LABEL)
        
        # Content section
        self._create_connect_and_status_section()
        self._create_calibration_and_port_section()
         
        self.content_layout = QHBoxLayout()
        self.content_layout.addLayout(self.connection_section_layout)
        self.content_layout.addLayout(self.calibration_and_port_layout)

        # Organize layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.main_label)
        self.main_layout.addLayout(self.content_layout)


    def _create_connect_and_status_section(self):
        # Button section
        self.connect_button = QPushButton('Connect')
        self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
        self.connect_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.connect_button.setContentsMargins(5, 5, 5, 5)  # Add small padding around text
        self.connect_button.clicked.connect(self._toggle_connection_status)

        button_container = QHBoxLayout()
        button_container.addWidget(self.connect_button)
        button_container.addStretch()

        # Status section
        self.connection_status_label = QLabel('Status: Disconnected')
        self.connection_status_label.setStyleSheet(Styles.LABEL_TEXT)

        self.connection_section_layout = QVBoxLayout()
        self.connection_section_layout.addLayout(button_container)
        self.connection_section_layout.addWidget(self.connection_status_label)
       

    def _create_calibration_and_port_section(self):
        # Calibration selection
        self.calibration_label = QLabel('Calibrate')
        self.calibration_label.setStyleSheet(Styles.LABEL_TEXT)

        self.calibration_combo_box = QComboBox()
        self.calibration_combo_box.setStyleSheet( f"{Styles.COMBOBOX_BASE} width: 130px;")

        self.calibration_section = QHBoxLayout()
        self.calibration_section.addWidget(self.calibration_label)
        self.calibration_section.addWidget(self.calibration_combo_box)

        # Port selection
        self.port_label = QLabel('COM Port')
        self.port_label.setStyleSheet(Styles.LABEL_TEXT)

        self.port_combo_box = QComboBox()
        self.port_combo_box.setStyleSheet( f"{Styles.COMBOBOX_BASE} width: 70px;")

        self.port_section = QHBoxLayout()
        self.port_section.addWidget(self.port_label)
        self.port_section.addWidget(self.port_combo_box)

        # Organize layout   
        self.calibration_and_port_layout = QVBoxLayout()
        self.calibration_and_port_layout.addLayout(self.calibration_section)
        self.calibration_and_port_layout.addLayout(self.port_section)


    def _toggle_connection_status(self):
        if self.connect_button.text() == 'Connect':
            self.connect_button.setText('Disconnect')
            self.connect_button.setStyleSheet(self.connect_button_styles["disconnect"])
            self.port_combo_box.setEnabled(False)
        else:
            self.connect_button.setText('Connect')
            self.connect_button.setStyleSheet(self.connect_button_styles["connect"])
            self.port_combo_box.setEnabled(True)
