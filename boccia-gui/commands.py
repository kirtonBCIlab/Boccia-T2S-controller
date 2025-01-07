from PyQt5.QtCore import Qt

class Commands():
    CALIBRATION = "calibration"
    HOLD = "hold"
    TOGGLE = "toggle"

    CALIBRATION_COMMANDS = {
        "Full": "dd70>rc>ec",
        "Drop": "dd70",
        "Rotation": "rc0",
        "Elevation - manual": "ec0",
        "Elevation - auto": "ec1",
        }

    HOLD_COMMANDS = {
        Qt.Key_A: "rs0",    # Rotation Left
        Qt.Key_D: "rs1",    # Rotation Right
        Qt.Key_W: "es0",    # Elevation Up
        Qt.Key_S: "es1",    # Elevation Down
        }

    TOGGLE_COMMANDS = {
        Qt.Key_1: "es1",    # Elevation up
        Qt.Key_2: "rs1",    # Rotation right
        Qt.Key_3: "dd-70",  # Drop - T2S activated
        Qt.Key_R: "dd-70",  # Drop - Keyboard activated
        }
    
    BUTTON_COMMANDS = {
        "Elevation up": "es1",
        "Rotation right": "rs1",
        "Drop": "dd-70",
        }