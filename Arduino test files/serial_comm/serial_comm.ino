
/* SAMPLE CODE:
 the following code using a simple LED breadboard set up to test serial communication
 in the code, pressing A on the keyboard will trigger LED 22 to flah for 1 sec and similar with LED 24 for B */


#define COMMAND_LEN 1 // Define the length of your command

char command[COMMAND_LEN + 1]; // Define the command array with extra space for null-terminator

void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(22, OUTPUT); // Initialize pin 22 as an output
  pinMode(24, OUTPUT); // Initialize pin 24 as an output
}

void loop() {
  if (Serial.available() > 0) {
    decode_serial();
    LED_command(command[0]);
  }
}

void decode_serial() {
  delay(100); // Wait 100 msec for complete serial transmission
  
  for (int i = 0; i < COMMAND_LEN; i++) {
    while (Serial.available() == 0); // Wait until data is available
    command[i] = Serial.read();
  }
  command[COMMAND_LEN] = '\0'; // Null-terminate the command string for safety
}

void LED_command(char key) {
  if (key == '2') {
    Serial.println("Received command: 2 - Flash LED 22");
    digitalWrite(22, HIGH); // Turn LED 22 on
    delay(1000);            // Wait for 1 second
    digitalWrite(22, LOW);  // Turn LED 22 off
  } else if (key == '3') {
    Serial.println("Received command: 3 - Flash LED 24");
    digitalWrite(24, HIGH); // Turn LED 24 on
    delay(1000);            // Wait for 1 second
    digitalWrite(24, LOW);  // Turn LED 24 off
  } else {
    Serial.println("Invalid command");
  }
}
