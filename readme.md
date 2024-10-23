# Boccia Mental Command Firmware

This repo hosts the firmware to controller for the Boccia ramp to be used with mental commands for the BCI4Kids clinical program.

It contains the following folders:

1. Main Firmware: houses all the primary code to be run on the ramp
2. Arduino Test Files: the code that is used to test individual electronic components

# Instructions to Run
Running the code requires the Arduino Extension in VSCode and the PlatformIO extension.
When developing the main project it is best to open each folder (Arduino Test files and Main Firmware) individually.

# Steps to run INO files on VSCode
1. Install the Arduino VS Code extension on VSCode 
3. Open your project File > Open folder or Ctrl + K, Ctrl + O or create a new .ino file
4. Open the pallet command Ctrl + Shift + P
5. Start typing "Arduino", and set the board (board manager and change board), select the port, and select the sketch. This should create a new Arduino.json file
6. Verify the code (build) and upload to the board using the command pallet OR upload button on top right

Note: To detect which COM port is the Arduino connected to, you can open the device manager, and scroll down to ports. See the ports available, and the connect the Arduino, the list will refresh and the new port that shows up will be the one corresponding to the Arduino
