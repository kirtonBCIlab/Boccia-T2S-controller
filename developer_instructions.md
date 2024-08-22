# Developer Instruction Guide

## 1. **Environment Setup** 🔧

1. **Update Environment:** Ensure that the YML file is used to update the environment. This will configure all necessary dependencies and settings.
2. **Firmware Update:** Verify that the Arduino firmware is updated to the latest version. This is crucial for ensuring compatibility with the ramp system.

## 2. **Firmware Upload** 🖥️

1. **Running INO Files on VSCode**
   - Install the Arduino VS Code extension on VSCode
   - Open your project File > Open folder or Ctrl + K, Ctrl + O or create a new .ino file
   - Open the pallet command Ctrl + Shift + P
   - Start typing "Arduino", and set the board (board manager and change board), select the port, and select the sketch. This should create a new Arduino.json file
   - Verify the code (build) and upload to the board using the command pallet OR upload button on top right
     **Note:** *To detect which COM port is the Arduino connected to, you can open the device manager, and scroll down to ports. See the ports available, and the connect the Arduino, the list will refresh and the new port that shows up will be the one corresponding to the Arduino*

2. **Upload Firmware:**
   - Run the `main.cpp` file from the `bci-hardware` directory.
   - Upload it to the ramp following the user instructions provided.

## 3. **Program Compilation** 😊

1. **Compile GUI Program:** Compile the `Boccia_Ramp_Controls.exe` file from the source code.
2. **Program Execution:** Follow the program's instructions for further setup and operation, as outlined in the user instruction guide.
