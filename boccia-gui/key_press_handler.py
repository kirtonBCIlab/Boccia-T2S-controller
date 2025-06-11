# Default libraries
from PyQt5.QtCore import QObject, Qt, pyqtSignal

# Custom libraries
from commands import Commands

class KeyPressHandler(QObject):
    key_service_flag_changed = pyqtSignal(bool)

    def __init__(self, parent=None, serial_handler = None, commands = None):
        super().__init__()
        self.parent = parent
        self.serial_handler = serial_handler
        self.commands = commands

        self.key_pressed = None # Store the key pressed for hold commands
        self.key_toggled = None # Store the key pressed for toggle commands

        self.service_flag = False

        self.current_player = None

        self.key_action_map = {}
        self.mapKeys()

    def mapKeys(self):
        for index, key in enumerate(Commands.TOGGLE_COMMANDS.keys()):
            self.key_action_map[key] = index + 1

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            if event.key() == Qt.Key_F1:
                self.parent.serial_controls_widget.open_help_url()
                return True
            else:
                self.keyPressEvent(event)
            return True
        elif event.type() == event.KeyRelease:
            self.keyReleaseEvent(event)
            return True
        
        return super().eventFilter(obj, event)


    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            key = event.key()
            
            if (key in Commands.HOLD_COMMANDS):
                # Get the command
                command = Commands.HOLD_COMMANDS[key]
                self.hold_key_pressed(command, key)

            elif (key in Commands.TOGGLE_COMMANDS):
                # Get the command
                command = Commands.TOGGLE_COMMANDS[key]
                self.toggle_key_pressed("Player 1", command, key)
                
            event.accept()

    def hold_key_pressed(self, command, key=None):
        if key == None:
            key = self.commands.get_key_from_hold_command(command)

        # print(f"\nOperator key pressed: {key}")

        # If service is active, return
        if self.service_flag:
            return
        
        # Otherwise, send the command
        self.serial_handler.send_command(command)
        self.key_pressed = key
        # print(f"Start {command} command")

        self.toggle_service_flag(True)
        self.key_service_flag_changed.emit(True)

    def toggle_key_pressed(self, player, command, key=None):
        if key == None:
            key = self.commands.get_key_from_toggle_command(command)
            
        # print(f"\nUser key pressed: {key}")

        # If service is active
        if self.service_flag & (key == self.key_toggled):

            # If Drop delay is active, return
            if self.commands.get_drop_delay_active():
                return
            
            # Return if the player is not the current player
            if player != self.current_player:
                return
            
            # Otherwise, send the command
            self.serial_handler.send_command(command)
            # print(f"Stop {command} command")

            # Toggle the flag and set the current action
            self.toggle_service_flag(False)
            self.key_service_flag_changed.emit(False)
            self.key_toggled = None
            
        # If service is not active
        elif not self.service_flag:
            # Send the command
            self.serial_handler.send_command(command)
            # print(f"Start {command} command")

            # If Drop key was pressed, start the drop delay timer
            if command == "dd-70":
                self.commands.drop_delay_timer()

            # Toggle the flag and set the current action
            self.toggle_service_flag(True)
            self.key_service_flag_changed.emit(True)
            self.key_toggled = key

            # Set the current player
            self.current_player = player

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            key = event.key()
            if (key in Commands.HOLD_COMMANDS) and (key == self.key_pressed):
                #print(f"Operator key released: {key}")
                command = Commands.HOLD_COMMANDS[key]
                self.serial_handler.send_command(command)
                self.key_pressed = None
                #print(f"Stop {command} command")
                
                self.toggle_service_flag(False)
                self.key_service_flag_changed.emit(False)

            event.accept()

    def toggle_service_flag(self, flag):
        self.service_flag = flag
        # print(f"Key press service flag: {self.service_flag}")

    def reset_flags(self):
        self.service_flag = False
        self.key_toggled = None

class KeyPressHandlerMultiplayer(QObject):
    key_service_flag_changed = pyqtSignal(bool)

    def __init__(self, parent=None, bluetooth_client = None, commands = None):
        super().__init__()
        self.parent = parent
        self.bluetooth_client_thread = bluetooth_client
        self.commands = commands

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            self.keyPressEvent(event)

        return super().eventFilter(obj, event)
    
    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            key = event.key()
            if (key in Commands.TOGGLE_COMMANDS):

                # Get the command:
                command = Commands.TOGGLE_COMMANDS[key]
                self.bluetooth_client_thread.send_command(command)
                
            event.accept()

                