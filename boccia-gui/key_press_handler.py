from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

class KeyPressHandler(QWidget):
    def __init__(self, serial_thread):
        super().__init__()
        self.serial_thread = serial_thread
        
        self.commands = {
            Qt.Key_A: "7100",
            Qt.Key_D: "7110",
            Qt.Key_S: "7200",
            Qt.Key_W: "7210",
        }

    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            key = event.key()
            if (key in self.commands) and (not self.serial_thread.is_command_sent):
                print(f"Key pressed: {key}")
                command = self.commands[key]
                self.serial_thread.send_command(command)
                self.serial_thread.is_command_sent = True
                print(f"Sent press command: {command} to serial port")
                event.accept()
            # else:
            #     super().keyPressEvent(event)

    # def keyPressEvent(self, event):
    #     key = event.key()
    #     if (key in self.commands) and :
    #         print(f"Key pressed: {key}")
    #         if self.serial_thread and self.serial_thread.serial:
    #             command = self.commands[key]
    #             if not self.serial_thread.is_command_sent:
    #                 self.serial_thread.send_command(command)
    #                 self.serial_thread.is_command_sent = True
    #                 print(f"Sent command: {command} to serial port")
        # else:
        #     # Propagate the event to other widgets
        #     super().keyPressEvent(event)
        # event.accept()

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            key = event.key()
            if (key in self.commands) and (self.serial_thread.is_command_sent):
                print(f"Key released: {key}")
                command = self.commands[key]
                self.serial_thread.send_command(command)
                self.serial_thread.is_command_sent = False
                print(f"Sent release command: {command} to serial port")
            # else:
            #     # Propagate the event to other widgets
            #     super().keyReleaseEvent(event)