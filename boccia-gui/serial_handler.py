import serial
import serial.tools.list_ports
from PyQt5.QtCore import QThread, pyqtSignal

class SerialHandler(QThread):
    """ Handles serial communication with the COM ports and connected devices """
    # Events
    connection_changed = pyqtSignal(str)    # Signal to indicate a change in the connection status
    new_data = pyqtSignal(str)              # Signal to indicate new data has been received from the Arduino

    def __init__(
            self,
            port:str = "",
            baudrate:int = 9600):
        """
            Initialize the SerialHandler object

            Attributes
            ----------
                - `port`: str\n
                    The COM port to connect to
                - `baudrate`: int\n
                    The baudrate to use for the serial connection
        """
        super().__init__()
        self._port = port
        self._baudrate = baudrate
        
        self._serial = None
        self._connection_status = ["Connected", "Disconnected", "Error"]
        self._current_connection_status = self._connection_status[1]
        self.command_sent = False   # Flag to indicate if a command has been sent succesfully


    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port


    @property
    def baudrate(self):
        return self._baudrate

    @baudrate.setter
    def baudrate(self, baudrate):
        self._baudrate = baudrate
        self._serial.baudrate = baudrate   


    def toggle_serial_connection(self):
        """ Toggle the serial connection """
        if (self._current_connection_status == "Disconnected") or (self._current_connection_status == "Error"):
            self.connect()
        else:
            self.disconnect()


    def connect(self):
        """ Open a serial connection """
        try:
            self._serial = serial.Serial(self._port, self._baudrate)
            self._current_connection_status = self._connection_status[0]
            self.connection_changed.emit(self._current_connection_status)
        except serial.SerialException:
            self._current_connection_status = self._connection_status[2]
            self.connection_changed.emit(self._current_connection_status)


    def disconnect(self):
        """ Close the serial connection """
        try:
            self._serial.close()
            self._serial = None
            self._current_connection_status = self._connection_status[1]
            self.connection_changed.emit(self._current_connection_status)
        except serial.SerialException:
            self._current_connection_status = self._connection_status[2]
            self.connection_changed.emit(self._current_connection_status)
        

    def send_command(self, command:str):
        """ Send `command` to the serial port """

        # Skip if command is empty or only whitespaces
        if not command.strip():
            return

        if self._current_connection_status == "Connected":
            try:
                code_str = command + "\n"
                self._serial.write(code_str.encode("UTF-8"))
                #print(f"Sent serial: {code_str}")
                self.command_sent = True
            except Exception as e:
                #print(f"Error sending data to serial: {str(e)}")
                self.command_sent = False

    
    def run(self):
        """ Start separate threat to read data from the serial port """
        
        # Skip if there is no serial connection
        if not self._serial:
            return
        
        self._serial.timeout = 0.1  # Non-blocking timeout
        self._running = True
        
        while self._running and self._serial.is_open:
            try:
                line = self._serial.readline()
                
                # Only process if there is data
                if line:
                    decoded_line = line.decode("UTF-8").strip()
                    if decoded_line:
                        self.new_data.emit(decoded_line)
                        
            except Exception as e:
                self.new_data.emit(f"Error reading serial data: {str(e)}")
                break


    def stop(self):
        """ Stop the thread to read from the serial port """
        #print("serial stopped")
        self._running = False


    def list_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        available_ports = [port.device for port in ports]

        return available_ports
    

    def get_current_connection_status(self):
        return self._current_connection_status
    
    