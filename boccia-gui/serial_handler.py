import serial
from PyQt5.QtCore import QThread

class SerialHandler(QThread):
    """ Handles serial communication with the COM ports and connected devices """

    def __init__(
            self,
            port:str = "COM1",
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
        self._port = port
        self._baudrate = baudrate
        
        self._connection_status = ["Connected", "Disconnected", "Error"]
        self._current_connection_status = self._connection_status[1]

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port
        self._serial.port = port

    @property
    def baudrate(self):
        return self._baudrate

    @baudrate.setter
    def baudrate(self, baudrate):
        self._baudrate = baudrate
        self._serial.baudrate = baudrate   

    def connect(self):
        """ Open a serial connection """
        try:
            self._serial = serial.Serial(self._port, self._baudrate)
            self._current_connection_status = self._connection_status[0]
        except serial.SerialException:
            self._current_connection_status = self._connection_status[2]

    def disconnect(self):
        """ Close the serial connection """
        try:
            self._serial.close()
            self._current_connection_status = self._connection_status[1]
        except serial.SerialException:
            self._current_connection_status = self._connection_status[2]
        

    def send(self, data):
        """ Send data to the serial port """
        self._serial.write(data)

    def read(self):
        """ Read data from the serial port """
        return self._serial.read()

    def list_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        available_ports = [port.device for port in ports]
        return available_ports
    
    def get_current_connection_status(self):
        return self._current_connection_status
    
    