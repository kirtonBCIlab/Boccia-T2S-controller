import serial

def start_echo_server(port):
    try:
        # Open serial port
        with serial.Serial(port, 9600, timeout=1) as ser:
            print(f"Listening on {port}...")
            while True:
                if ser.in_waiting > 0:
                    # Read data from serial port
                    data = ser.read(ser.in_waiting).decode('utf-8')
                    print(f"Received: {data}")
                    
                    # Echo data back
                    ser.write(data.encode('utf-8'))
                    
    except serial.SerialException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    port = 'COM6'  # Change this to the COM port you're using
    start_echo_server(port)
