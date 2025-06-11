# Standard libraries
from PyQt5.QtCore import Qt, QTimer

class Commands():
    CALIBRATION = "calibration"
    HOLD = "hold"
    TOGGLE = "toggle"

    CALIBRATION_COMMANDS = {
        "Full": "dd-70>rc>ec",
        "Drop": "dd-70",
        "Rotation": "rc0",
        "Elevation - manual": "ec0",
        "Elevation - auto": "ec1",
        }

    HOLD_COMMANDS = {
        Qt.Key_A: "rs0",    # Rotation Left
        Qt.Key_D: "rs1",    # Rotation Right
        Qt.Key_W: "es1",    # Elevation Up
        Qt.Key_S: "es0",    # Elevation Down
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
    
    OPERATOR_COMMANDS = {
        "A ←": "rs0",
        "→ D": "rs1",
        "W ↑": "es1",
        "S ↓": "es0",
        "Drop \n(R)": "dd-70",
    }

    # Min and max number of players for multiplayer mode
    MIN_MULTIPLAYERS = 2
    MAX_MULTIPLAYERS = 4
    
    HELP_URL = "https://github.com/kirtonBCIlab/Boccia-T2S-controller/wiki"
    
    def __init__(self):
        
        self.timer = None # Timer for the drop delay
        self.drop_delay = 15000 # [msec]
        self.drop_delay_active = None

        self.user_controls_widget = None
        self.key_press_handler = None
        self.operator_controls_widget = None

        self.toggle_command_active = False

    def set_user_controls_widget(self, user_controls_widget):
        self.user_controls_widget = user_controls_widget

    def set_key_press_handler(self, key_press_handler):
        self.key_press_handler = key_press_handler

    def set_operator_controls_widget(self, operator_controls_widget):
        self.operator_controls_widget = operator_controls_widget

    def drop_delay_timer(self):
        
        # Stop timer if it exists
        if self.timer:
            self.timer.stop()

        # Disable user control buttons
        self.drop_delay_active = True # Set the flag

        # Start the timer
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: self.timer_over())
        self.timer.start(self.drop_delay)
        #print("Drop delay timer started")

    def timer_over(self):
        #print("\nDrop delay over")
        self.drop_delay_active = False # Reset the drop delay flag
        self.key_press_handler.reset_flags()
        self.user_controls_widget._reset_buttons_and_flags()
        self.operator_controls_widget._reset_buttons_and_flag()

    def get_drop_delay_active(self):
        return self.drop_delay_active

    def get_key_from_hold_command(self, command):
        for key, value in self.HOLD_COMMANDS.items():
            if value == command:
                # print(f"Key from hold command: {key}")
                return key
            
    def get_key_from_toggle_command(self, command):
        for key, value in self.TOGGLE_COMMANDS.items():
            if value == command:
                # print(f"Key from toggle command: {key}")
                return key