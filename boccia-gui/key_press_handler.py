# Default libraries
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QTimer, Qt

# Custom libraries
from commands import Commands

class KeyPressHandler(QObject):
    def __init__(self, serial_handler = None):
        super().__init__()

        self.serial_handler = serial_handler

        self.key_pressed = None # Store the key pressed for hold commands

        self.key_toggled = None # Store the key pressed for toggle commands

        self.key_enabled = True # True if the key is enabled

        self.timer = None # Timer for key lock

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
                    # If the key is disabled, return
                    if not self.key_enabled:
                        print("Waiting for drop movement to finish")
                        return
                    
                    command = Commands.TOGGLE_COMMANDS[key]
                    self.serial_handler.send_command(command)
                    print(f"Sent {command} command")
                    self.key_enabled = False # Disable the key

                    # Stop timer if it exists
                    if self.timer:
                        self.timer.stop()

                    # Start the timer
                    self.timer = QTimer(self)
                    self.timer.setSingleShot(True)
                    self.timer.timeout.connect(lambda: self._reenable_key())
                    self.timer.start(15000) # Key disabled for 15 seconds
                    # print("Key disabled for 15 seconds")

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


    def _reenable_key(self):
        # Re-enable key
        self.key_enabled = True