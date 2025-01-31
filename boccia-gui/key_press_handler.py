# Default libraries
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QTimer, Qt

# Custom libraries
from commands import Commands

class KeyPressHandler(QObject):
    def __init__(self, serial_handler = None, commands = None):
        super().__init__()

        self.serial_handler = serial_handler
        self.commands = commands

        self.key_pressed = None # Store the key pressed for hold commands
        self.key_toggled = None # Store the key pressed for toggle commands

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

                # If drop delay is active, do not send any commands
                if self.commands.get_drop_delay_active():
                    print("Waiting for drop movement to finish")
                    return
                
                # If a sweeping command is not currently active
                if not self.commands.get_toggle_command_active():
                    # If the Drop key was pressed, start the drop delay timer    
                    if key == Qt.Key_3:
                        self.commands.drop_delay_timer()

                    # Else if Elevation or Rotation was toggled
                    else:
                        self.key_toggled = key # Store the key
                        self.commands.set_toggle_command_active(True) # Set the flag

                    # Send the command
                    command = Commands.TOGGLE_COMMANDS[key]
                    self.serial_handler.send_command(command)
                    print(f"Start {command} command")

                elif self.commands.get_toggle_command_active():
                    if key == self.key_toggled:
                        # Send the command
                        command = Commands.TOGGLE_COMMANDS[key]
                        self.serial_handler.send_command(command)
                        print(f"Stop {command} command")

                        self.key_toggled = None # Reset the key
                        self.commands.set_toggle_command_active(False) # Reset the flag

                    else:
                        command = Commands.TOGGLE_COMMANDS[self.key_toggled]
                        print(f"Waiting for {command} command to be toggled off")
                
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
