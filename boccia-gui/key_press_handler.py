# Default libraries
from PyQt5.QtCore import QObject, pyqtSignal

# Custom libraries
from commands import Commands

class KeyPressHandler(QObject):
    key_service_flag_changed = pyqtSignal(bool)

    def __init__(self, serial_handler = None, commands = None):
        super().__init__()

        self.serial_handler = serial_handler
        self.commands = commands

        self.key_pressed = None # Store the key pressed for hold commands
        self.key_toggled = None # Store the key pressed for toggle commands

        self.service_flag = False

        self.key_action_map = {}
        self.mapKeys()

    def mapKeys(self):
        for index, key in enumerate(Commands.TOGGLE_COMMANDS.keys()):
            self.key_action_map[key] = index + 1

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
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
                print(f"\nOperator key pressed: {key}")
                command = Commands.HOLD_COMMANDS[key]
                self.serial_handler.send_command(command)
                self.key_pressed = key

            elif key in Commands.TOGGLE_COMMANDS:
                print(f"\nUser key pressed: {key}")

                # Get the command
                command = Commands.TOGGLE_COMMANDS[key]

                # If service is active
                if self.service_flag & (key == self.key_toggled):

                    # If Drop delay is active, return
                    if self.commands.get_drop_delay_active():
                        return
                    
                    # Otherwise, send the command
                    self.serial_handler.send_command(command)
                    print(f"Stop {command} command")

                    # Toggle the flag and set the current action
                    self.toggle_service_flag(False)
                    self.key_service_flag_changed.emit(False)
                    self.key_toggled = None
                    
                # If service is not active
                elif not self.service_flag:
                    # Send the command
                    self.serial_handler.send_command(command)
                    print(f"Start {command} command")

                    # If Drop key was pressed, start the drop delay timer
                    if command == "dd-70":
                        self.commands.drop_delay_timer()

                    # Toggle the flag and set the current action
                    self.toggle_service_flag(True)
                    self.key_service_flag_changed.emit(True)
                    self.key_toggled = key
                
            event.accept()


    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            key = event.key()
            if (key in Commands.HOLD_COMMANDS) and (key == self.key_pressed):
                print(f"Operator key released: {key}")
                command = Commands.HOLD_COMMANDS[key]
                self.serial_handler.send_command(command)
                self.key_pressed = None

            event.accept()

    def toggle_service_flag(self, flag):
        self.service_flag = flag
        # print(f"Key press service flag: {self.service_flag}")

    def reset_flags(self):
        self.service_flag = False
        self.key_toggled = None