# This code is to test the toggle functionality of the Arduino code, it works using 2 LEDs and a space button
# The LEDs will toggle on and off when the space button is pressed (toggle mode)
# the left and right arrow keys will turn on the left and right LED respectively (direct mode)

from pynput.keyboard import Key, Listener
import serial
import time

# Set up serial connection (adjust 'COM3' to your Arduino's port)
ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)  # Wait for the serial connection to initialize

toggle_flag = False

def on_press(key):
    global ser
    print(f'Key {key} pressed')
    if key == Key.left:
        command = 'left_press\n'
    elif key == Key.right:
        command = 'right_press\n'
    elif key == Key.space:
        command = 'space_toggle\n'
    else:
        command = None

    if command:
        ser.write(command.encode())

def on_release(key):
    global ser
    print(f'Key {key} released')
    if key == Key.left:
        command = 'left_release\n'
    elif key == Key.right:
        command = 'right_release\n'
    else:
        command = None

    if command:
        ser.write(command.encode())

    if key == Key.esc:
        # Stop listener when the 'esc' key is pressed
        return False

# Start listening for events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Close serial connection when done
ser.close()
