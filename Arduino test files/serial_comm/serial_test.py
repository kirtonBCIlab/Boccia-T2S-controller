import serial
import keyboard

# Set up the serial connection (Make sure to replace 'COM9' with your Arduino's port)
ser = serial.Serial('COM3', 9600, timeout=1)
ser.flush()

# Variable to track the last command sent2323
last_command_sent = None

try:
    while True:
        # Check if '2' key is pressed and the last command wasn't '2'
        if keyboard.is_pressed('2') and last_command_sent != '2':
            print("Sending command '2' to Arduino")
            ser.write(b'2')  # Send '2' as bytes to Arduino
            last_command_sent = '2'  # Update the last command sent

        # Check if '3' key is pressed and the last command wasn't '3'
        elif keyboard.is_pressed('3') and last_command_sent != '3':
            print("Sending command '3' to Arduino")
            ser.write(b'3')  # Send '3' as bytes to Arduino
            last_command_sent = '3'  # Update the last command sent

except KeyboardInterrupt:
    print("Exiting program")
finally:
    ser.close()  # Close the serial connection when done