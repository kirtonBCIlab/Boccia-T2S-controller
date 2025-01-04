# Import libraries
from enum import Enum
from PyQt5.QtCore import Qt

class commands(Enum):
    CALIBRATION = "calibration"
    HOLD = "hold"
    TOGGLE = "toggle"

    CALIBRATION_COMMANDS = {
        "Full": "dd-70>rc>ec",
        "Drop": "dd-70",
        "Rotation": "rc0",
        "Elevation - manual": "ec0",
        "Elevation - automatic": "ec1",
    }

    HOLD_COMMANDS = {
        Qt.Key_A: "rs0",    # Rotation Left
        Qt.Key_D: "rs1",    # Rotation Right
        Qt.Key_W: "es0",    # Elevation Up
        Qt.Key_S: "es1",    # Elevation Down
    }

    TOGGLE_COMMANDS = {
        Qt.Key_1: "es1",    # Elevation up
        Qt.Key_2: "rs0",    # Rotation right
        Qt.Key_3: "dd-70",  # Drop - T2S activated
        Qt.Key_R: "dd-70",  # Drop - Keyboard activated
    }