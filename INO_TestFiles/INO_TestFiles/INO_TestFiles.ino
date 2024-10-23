// Define the pin numbers for the sensors
#define SENSOR1_PIN 26
#define SENSOR2_PIN 22

// Define the debounce time in milliseconds
#define DEBOUNCE_TIME 50

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);


  // Set the sensor pins as input
  pinMode(SENSOR1_PIN, INPUT);
  pinMode(SENSOR2_PIN, INPUT);
}

void loop() {
  // Check the state of the sensors
  if (digitalReadDebounce(SENSOR1_PIN, DEBOUNCE_TIME, true)) {
    Serial.println("Sensor 1 activated");
  }
  if (digitalReadDebounce(SENSOR2_PIN, DEBOUNCE_TIME, true)) {
    Serial.println("Sensor 2 activated");
  }

  // Wait for a short period before checking again
  delay(1000);
}

bool digitalReadDebounce(int pin, unsigned long msec_debounce, bool is_rising)
{
  int r0 = digitalRead(pin);
  int r1;
  unsigned long t0 = millis();
  unsigned long t1;

  do
  {
    r1 = digitalRead(pin);
    t1 = millis();

    if (is_rising && (r1 == 0)) { return false; }
    else if (!is_rising && (r1 == 1)) { return false; }

  } while ((t1-t0) < msec_debounce);
  
  return true;
}