# Standard libraries
import json
import os
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeySequence

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

    HOLD_ACTION_COMMANDS = {
        "rotation_left": "rs0",
        "rotation_right": "rs1",
        "elevation_up": "es1",
        "elevation_down": "es0",
        }

    TOGGLE_ACTION_COMMANDS = {
        "elevation_up": "es1",
        "rotation_right": "rs1",
        "drop": "dd-70",
        }

    # Use different keys than the Multiplayer Toggle Keys
    DEFAULT_HOLD_KEYS = {
        "rotation_left": Qt.Key_J,
        "rotation_right": Qt.Key_L,
        "elevation_up": Qt.Key_I,
        "elevation_down": Qt.Key_K,
        }

    DEFAULT_TOGGLE_KEYS = {
        "elevation_up": Qt.Key_1,
        "rotation_right": Qt.Key_2,
        "drop": Qt.Key_3,
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

    # Based on available keyboard mapping in T2S iOS app
    # Each player has a rotation right and drop toggle command
    MULTIPLAYER_TOGGLE_KEYS = {
        "Player 1": {
            "rotation_right": Qt.Key_W,
            "drop": Qt.Key_Space,
        },
        "Player 2": {
            "rotation_right": Qt.Key_A,
            "drop": Qt.Key_Return,
        },
        "Player 3": {
            "rotation_right": Qt.Key_S,
            "drop": Qt.Key_Up,
        },
        "Player 4": {
            "rotation_right": Qt.Key_D,
            "drop": Qt.Key_Down,
        },
    }

    # Min and max number of players for multiplayer mode
    MIN_MULTIPLAYERS = 2
    MAX_MULTIPLAYERS = 4

    BLUETOOTH_VARIABLES = {
        "RFCOMM_channel": 4,
        "bytes": 1024,
        "data_format": "utf-8",
        "disconnect_command": "Disconnect",
        "max_clients_message": "Max clients reached",
    }
    
    HELP_URL = "https://github.com/kirtonBCIlab/Boccia-T2S-controller/wiki"
    
    def __init__(self):
        
        self.timer = None # Timer for the drop delay
        self.drop_delay = 15000 # [msec]
        self.drop_delay_active = None

        self.user_controls_widget = None
        self.key_press_handler = None
        self.operator_controls_widget = None

        self.toggle_command_active = False

        self.hold_key_map = dict(self.DEFAULT_HOLD_KEYS)
        self.toggle_key_map = dict(self.DEFAULT_TOGGLE_KEYS)

        self.multiplayer_key_map = {}
        for player, actions in self.MULTIPLAYER_TOGGLE_KEYS.items():
            for action, key in actions.items():
                self.multiplayer_key_map[key] = (player, action)

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
        for action, value in self.HOLD_ACTION_COMMANDS.items():
            if value == command:
                return self.hold_key_map.get(action)
            
    def get_key_from_toggle_command(self, command):
        for action, value in self.TOGGLE_ACTION_COMMANDS.items():
            if value == command:
                return self.toggle_key_map.get(action)

    def get_hold_command_for_key(self, key):
        for action, mapped_key in self.hold_key_map.items():
            if mapped_key == key:
                return self.HOLD_ACTION_COMMANDS.get(action)

    def get_toggle_command_for_key(self, key):
        for action, mapped_key in self.toggle_key_map.items():
            if mapped_key == key:
                return self.TOGGLE_ACTION_COMMANDS.get(action)
            
    def get_multiplayer_toggle_command_for_key(self, key):
        result = self.multiplayer_key_map.get(key)
        if not result:
            return None
        _, action = result
        command = self.TOGGLE_ACTION_COMMANDS.get(action)
        return command
                
    def get_player_for_toggle_key(self, key):
        result = self.multiplayer_key_map.get(key)
        if not result:
            return None
        player, _ = result
        return player

    def get_hold_command_for_action(self, action):
        return self.HOLD_ACTION_COMMANDS.get(action)

    def get_toggle_command_for_action(self, action):
        return self.TOGGLE_ACTION_COMMANDS.get(action)

    def get_hold_key_for_action(self, action):
        return self.hold_key_map.get(action)

    def get_toggle_key_for_action(self, action):
        return self.toggle_key_map.get(action)

    def get_key_text(self, key):
        if key is None:
            return "?"
        text = QKeySequence(key).toString()
        return text if text else "?"

    def set_hold_key(self, action, key):
        self._swap_key(self.hold_key_map, action, key)

    def set_toggle_key(self, action, key):
        self._swap_key(self.toggle_key_map, action, key)

    def _swap_key(self, key_map, action, new_key):
        if action not in key_map:
            return

        current_key = key_map[action]
        if current_key == new_key:
            return

        swap_action = None
        for action_name, mapped_key in key_map.items():
            if mapped_key == new_key:
                swap_action = action_name
                break

        key_map[action] = new_key
        if swap_action and swap_action != action:
            key_map[swap_action] = current_key

    def load_key_config(self, file_path):
        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return False

        hold_keys = data.get("hold_keys", {})
        toggle_keys = data.get("toggle_keys", {})

        for action, key_value in hold_keys.items():
            if isinstance(key_value, int):
                self.set_hold_key(action, key_value)

        for action, key_value in toggle_keys.items():
            if isinstance(key_value, int):
                self.set_toggle_key(action, key_value)

        return True

    def save_key_config(self, file_path):
        data = {
            "hold_keys": self.hold_key_map,
            "toggle_keys": self.toggle_key_map,
            }

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)