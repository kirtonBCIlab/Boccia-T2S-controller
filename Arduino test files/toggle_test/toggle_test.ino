
// This code is to mimic both modes of the ramp (rotation and direct) using LEDs
// The LEDs will represent the movement of the ramp in the respective direction (Left and Right)
// the 'space_toggle' command initiates the rotation mode of the ramp and toggles it on and off

 
const int leftLED = 22;  // LED to represent 'left' movement
const int rightLED = 24;  // LED to represent 'right' movement

bool toggleFlag = false;

void setup() {
  pinMode(leftLED, OUTPUT);
  pinMode(rightLED, OUTPUT);
  Serial.begin(9600);  // Initialize serial communication
  digitalWrite(leftLED, LOW);
  digitalWrite(rightLED, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Releft any trailing whitespace or newline characters

    if (command == "left_press") {
      digitalWrite(leftLED, HIGH);  // Turn on 'left' LED
    } else if (command == "left_release") {
      digitalWrite(leftLED, LOW);   // Turn off 'left' LED
    } else if (command == "right_press") {
      digitalWrite(rightLED, HIGH);  // Turn on 'right' LED
    } else if (command == "right_release") {
      digitalWrite(rightLED, LOW);   // Turn off 'right' LED
    } else if (command == "space_toggle") {
      toggleFlag = !toggleFlag;
      if (toggleFlag) {
        // Toggle on - will intiate movement of ramp (rotation mode)
        digitalWrite(leftLED, HIGH);
        digitalWrite(rightLED, HIGH);
      } else {
        // Toggle off - will stop movement of ramp (rotation mode)
        digitalWrite(leftLED, LOW);
        digitalWrite(rightLED, LOW);
      }
      Serial.print("Toggle flag is now: ");
      Serial.println(toggleFlag);
    }
  }
}
