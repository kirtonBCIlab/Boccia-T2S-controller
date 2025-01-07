# Default libraries
from PyQt5.QtCore import QObject

# Custom libraries
from commands import Commands

class KeyPressHandler(QObject):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.serial_handler = parent.serial_handler

        self.key_processed = False # Flag to prevent multiple key presses
        self.key_pressed = None # Store the key pressed for hold commands


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


    def focusInEvent(self, event):
        print("Key handler active")
        super().focusInEvent(event)


    def focusOutEvent(self, event):
        print("Key handler inactive")
        super().focusOutEvent(event)