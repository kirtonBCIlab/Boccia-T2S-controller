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

        self.key_enabled = True # True if the key is enabled

        self.timer = None # Timer for key lock


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
                print(f"Operator key pressed: {key}")
                command = Commands.HOLD_COMMANDS[key]
                self.serial_handler.send_command(command)
                self.key_pressed = key

            elif key in Commands.TOGGLE_COMMANDS:
                # If the drop key is pressed, start a timer to lock it
                if key == Qt.Key_3:

                    print(f"User key pressed: {key}")

                    # If the key is already disabled, return
                    if self.key_enabled == False:
                        # print("Key is disabled")
                        return
                    
                    # If it is enabled, send the command then disable it
                    command = Commands.TOGGLE_COMMANDS[key]
                    self.serial_handler.send_command(command)
                    print("Sent command")

                    # Disable the key
                    self.key_enabled = False

                    # Stop timer if it exists
                    if self.timer:
                        self.timer.stop()

                    # Start the timer
                    self.timer = QTimer(self)
                    self.timer.setSingleShot(True)
                    self.timer.timeout.connect(lambda: self._reenable_key())
                    self.timer.start(15000) # Locked for 15 seconds
                    print("Key disabled for 15 seconds")

                else:
                    # Send the command normally if a different key is pressed
                    print(f"User key pressed: {key}")
                    command = Commands.TOGGLE_COMMANDS[key]
                    self.serial_handler.send_command(command)
                
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