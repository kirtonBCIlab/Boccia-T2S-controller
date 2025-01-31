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
        self.key_enabled = True # True if the key is enabled
        self.toggle_command_active = False # Store if a toggle command is active

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

                # If the Drop key is pressed, start a timer to disable it
                if key == Qt.Key_3:
                    # If drop delay is active, return
                    if self.commands.get_drop_delay_active():
                        print("Waiting for drop movement to finish")
                        return

                    # Send the command
                    command = Commands.TOGGLE_COMMANDS[key]
                    self.serial_handler.send_command(command)
                    print(f"Sent {command} command")
                    self.commands.drop_delay_timer() # Start the timer
                    
                # Else if the Elevation or Rotation key is pressed
                else:
                    if self.toggle_command_active:
                        if key == self.key_toggled:
                            # Deactivate the command
                            command = Commands.TOGGLE_COMMANDS[key]
                            self.serial_handler.send_command(command)
                            print(f"Stop sweeping {command} command")

                            self.toggle_command_active = False # Set the flag
                            self.key_toggled = None # Reset the key

                        else:
                            print(f"Waiting for key {self.key_toggled} to be toggled off")
                        
                    else:
                        # Activate the command
                        command = Commands.TOGGLE_COMMANDS[key]
                        self.serial_handler.send_command(command)
                        print(f"Start sweeping {command} command")
            
                        self.toggle_command_active = True # Set the flag
                        self.key_toggled = key # Store the key
                
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
