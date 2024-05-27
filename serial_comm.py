import time

try:
    while True:
        # Check if 'A' key is pressed and the last command wasn't 'A'
        if keyboard.is_pressed('A') and last_command_sent != 'A':
            print("Sending command '2' to Arduino to turn on LED")
            ser.write(b'2')  # Send '2' as bytes to Arduino to turn on LED
            last_command_sent = 'A'  # Update the last command sent

            time.sleep(1)  # Wait for 1 second

            print("Sending command '3' to Arduino to turn off LED")
            ser.write(b'3')  # Send '3' as bytes to Arduino to turn off LED

except KeyboardInterrupt:
    print("Exiting program")
finally:
    ser.close()  # Close the serial connection when done