from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QWidget
from commands import Commands

class KeyPressHandler(QObject):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.serial_handler = parent.serial_handler

        self.key_processed = False # Flag to prevent multiple key presses


    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            self.keyPressEvent(event)
            return True
        elif event.type() == event.KeyRelease:
            self.keyReleaseEvent(event)
            return True
        
        return super().eventFilter(obj, event)


    def keyPressEvent(self, event):
        print("Key pressed")
        if not event.isAutoRepeat():
            key = event.key()
            
            if (key in Commands.HOLD_COMMANDS) and (not self.key_processed):
                print(f"Operator key pressed: {key}")
                command = Commands.HOLD_COMMANDS[key]
                self.serial_handler.send_command(command)
                self.key_processed = True
                print(f"Sent press command: {command} to serial port\n")

            elif key in Commands.TOGGLE_COMMANDS:
                print(f"User key pressed: {key}")
                command = Commands.TOGGLE_COMMANDS[key]
                self.parent.serialHandler.send_command(command)
                print(f"Sent press command: {command} to serial port\n")
                
            event.accept()


    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            key = event.key()
            if (key in Commands.HOLD_COMMANDS) and (self.serial_handler.command_sent):
                print(f"Key released: {key}")
                command = Commands.HOLD_COMMANDS[key]
                self.serial_handler.send_command(command)
                self.serial_handler.command_sent = False
                print(f"Sent release command: {command} to serial port")


    def focusInEvent(self, event):
        print("Key handler active")
        super().focusInEvent(event)


    def focusOutEvent(self, event):
        print("Key handler inactive")
        super().focusOutEvent(event)