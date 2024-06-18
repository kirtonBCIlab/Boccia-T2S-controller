const int motorPin1 = 22;  // LED pin for motor 1
const int motorPin2 = 23;  // LED pin for motor 2

volatile bool serialDataAvailable = false;
String commandBuffer;
bool toggleFlag = false;

void setup() {
  Serial.begin(9600);  // Initialize serial communication

  // Initialize motor control pins
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);

  // Setup Timer
  setupTimer();
}

void setupTimer() {
  // Set Timer1 to CTC mode
  TCCR1A = 0;  // Clear Timer/Counter Control Register A
  TCCR1B = 0;  // Clear Timer/Counter Control Register B
  TCNT1 = 0;   // Initialize counter value to 0

  // Set compare match register for desired interval (e.g., 10ms)
  OCR1A = 1562;  // (16*10^6) / (1000*1024) - 1 for 10ms intervals

  // Turn on CTC mode
  TCCR1B |= (1 << WGM12);

  // Set CS12 and CS10 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);

  // Enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);

  // Enable global interrupts
  sei();
}

ISR(TIMER1_COMPA_vect) {
  // Check for serial data
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();
    commandBuffer += incomingByte;

    if (incomingByte == '\n') {
      serialDataAvailable = true;  // Set flag to indicate new data is available
    }
  }
}

void loop() {
  if (serialDataAvailable) {
    serialDataAvailable = false;  // Reset flag
    handleCommand(commandBuffer);
    commandBuffer = "";  // Clear the command buffer
  }

  // Perform the Move action if toggleFlag is set
  if (toggleFlag) {
    moveMotors();
  }
}

void handleCommand(String command) {
  command.trim();

  // Command format: XYYY (X = motor number, YYY = degrees or percentage)
  if (command == "L") {
    // Toggle command
    toggleFlag = !toggleFlag;
  } else if (command == "Esc") {
    // Exit program
    toggleFlag = false;
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, LOW);
    // Add any other necessary cleanup code
  } else if (command.length() == 4) {
    int motor = command.charAt(0) - '0';
    int value = command.substring(1).toInt();

    // Determine the motor type and instruct the motor to move
    if (motor == 1) {
      // Control motor 1
      controlMotor(motorPin1, value);
    } else if (motor == 2) {
      // Control motor 2
      controlMotor(motorPin2, value);
    }
  }
}

void controlMotor(int motorPin, int value) {
  // Simulate motor control with LED
  if (value > 0) {
    digitalWrite(motorPin, HIGH);  // Turn on LED
  } else {
    digitalWrite(motorPin, LOW);   // Turn off LED
  }
}

void moveMotors() {
  // Simulate moving motors by toggling LEDs
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, HIGH);
  delay(500);  // Simulate movement duration
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
}
