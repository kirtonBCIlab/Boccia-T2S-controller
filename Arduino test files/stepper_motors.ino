#define STEPPER_PIN_1 22
#define STEPPER_PIN_2 24
#define STEPPER_PIN_3 26
#define STEPPER_PIN_4 28

int step_number = 0;
bool motor_running = true; // Flag to control motor operation

void setup() {
  pinMode(STEPPER_PIN_1, OUTPUT);
  pinMode(STEPPER_PIN_2, OUTPUT);
  pinMode(STEPPER_PIN_3, OUTPUT);
  pinMode(STEPPER_PIN_4, OUTPUT);

  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  // Check if the motor should continue running
  if (motor_running) {
    // Move one step in the clockwise direction
    OneStep(true);
    delay(2); // Delay between steps
  }

  // Check for serial input
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming serial command

    // Process the command
    if (command == '2') {
      // Stop the stepper motor
      digitalWrite(STEPPER_PIN_1, LOW);
      digitalWrite(STEPPER_PIN_2, LOW);
      digitalWrite(STEPPER_PIN_3, LOW);
      digitalWrite(STEPPER_PIN_4, LOW);
      Serial.println("Stepper motor stopped");
      motor_running = false; // Set flag to stop motor
    }
  }
}

void OneStep(bool dir) {
  // Define the sequence of stepper motor steps
  if (dir) {
    // Clockwise direction
    switch (step_number) {
      case 0:
        digitalWrite(STEPPER_PIN_1, HIGH);
        digitalWrite(STEPPER_PIN_2, LOW);
        digitalWrite(STEPPER_PIN_3, LOW);
        digitalWrite(STEPPER_PIN_4, LOW);
        break;
      case 1:
        digitalWrite(STEPPER_PIN_1, LOW);
        digitalWrite(STEPPER_PIN_2, HIGH);
        digitalWrite(STEPPER_PIN_3, LOW);
        digitalWrite(STEPPER_PIN_4, LOW);
        break;
      case 2:
        digitalWrite(STEPPER_PIN_1, LOW);
        digitalWrite(STEPPER_PIN_2, LOW);
        digitalWrite(STEPPER_PIN_3, HIGH);
        digitalWrite(STEPPER_PIN_4, LOW);
        break;
      case 3:
        digitalWrite(STEPPER_PIN_1, LOW);
        digitalWrite(STEPPER_PIN_2, LOW);
        digitalWrite(STEPPER_PIN_3, LOW);
        digitalWrite(STEPPER_PIN_4, HIGH);
        break;
    }
  }

  // Increment step_number and wrap around (0-3)
  step_number++;
  if (step_number > 3) {
    step_number = 0;
  }
}