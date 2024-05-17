// Include libraries
#include <Arduino.h>
#include <BocciaStepper.h>
#include <LinearActuator.h>
#include <Functions.h>
#include <AccelStepper.h>

// Build motor objects
// - Release Stepper Motor Configuration
int release_pin_step = 5;                           // Step pin for release stepper motor
int release_pin_dir = 6;                            // Direction pin for release stepper motor
int release_interrupt_pins[2] = {0, 2};             // Interrupt pins for release stepper motor limits
int release_nsteps = 800;                           // Number of steps per revolution for release stepper motor
int release_nsteps_return = 30;                     // Number of steps for release motor to return after operation
int release_default_speed = 600;                    // Default speed for release stepper motor (steps per second)
int release_default_accel = 20;                     // Default acceleration for release stepper motor
bool release_use_limits = false;                    // Whether to use limit switches for release stepper motor
BocciaStepper release(
    release_pin_step,
    release_pin_dir,
    release_interrupt_pins,
    release_nsteps,
    release_nsteps_return,
    release_default_speed,
    release_default_accel,
    release_use_limits
);

// - Rotation Stepper Motor Configuration
int rotation_pin_step = 12;                         // Step pin for rotation stepper motor
int rotation_pin_dir = 11;                          // Direction pin for rotation stepper motor
int rotation_interrupt_pins[2] = {3, 19};           // Interrupt pins for rotation stepper motor limits
int rotation_nsteps = 800;                          // Number of steps per revolution for rotation stepper motor
int rotation_nsteps_return = 180;                   // Number of steps for rotation motor to return after operation
int rotation_default_speed = 600;                   // Default speed for rotation stepper motor (steps per second)
int rotation_default_accel = 30;                    // Default acceleration for rotation stepper motor
bool rotation_use_limits = true;                    // Whether to use limit switches for rotation stepper motor
int rotation_gear_ratio = 3;                        // Gear ratio of rotation stepper motor
BocciaStepper rotation(
    rotation_pin_step,
    rotation_pin_dir,
    rotation_interrupt_pins,
    rotation_nsteps,
    rotation_nsteps_return,
    rotation_default_speed,
    rotation_default_accel,
    rotation_use_limits,
    rotation_gear_ratio
);

// - Incline Actuator Configuration
int incline_pin1 = 8;                               // Control pin 1 for incline linear actuator
int incline_pin2 = 7;                               // Control pin 2 for incline linear actuator
int incline_pin_pot = 4;                            // Analog pin for potentiometer feedback of incline actuator
int incline_speed_threshold = 15;                   // Speed threshold for incline actuator
int incline_speed_factor = 50;                      // Speed factor for incline actuator
int incline_pin_sensor = 7;                         // Pin sensor dependency for incline actuator calibration
int incline_pin_threshold = 600;                    // Threshold value for incline actuator calibration
LinearActuator incline(
    incline_pin1,
    incline_pin2,
    incline_pin_pot,
    incline_speed_threshold,
    incline_speed_factor,
    incline_pin_sensor,
    incline_pin_threshold
);

// - Elevator Actuator Configuration
int elevator_pin1 = 9;                              // Control pin 1 for elevator linear actuator
int elevator_pin2 = 10;                             // Control pin 2 for elevator linear actuator
int elevator_pin_pot = 3;                           // Analog pin for potentiometer feedback of elevator actuator
int elevator_speed_threshold = 15;                  // Speed threshold for elevator actuator
int elevator_speed_factor = 50;                     // Speed factor for elevator actuator
int elevator_manual_limits[2] = {20, 360};          // Manual limits (ADC values) for elevator actuator calibration
LinearActuator elevation(
    elevator_pin1,
    elevator_pin2,
    elevator_pin_pot,
    elevator_speed_threshold,
    elevator_speed_factor
);

// Prototype functions
void releaseLimit();
void leftLimit();
void rightLimit();
void waitMillis(unsigned long wait_msec);
void decodeCommand();

void setup() {
    // Serial communication setup for debugging
    Serial.begin(9600);
    Serial.println("Begin setup");

    // Initialize motor pins and clear sensors
    // release.initializePins();
    // rotation.initializePins();
    // incline.initializePins();
    // elevation.initializePins();

    // Clear sensors while motors are stopped
    release.clearSensorWhileStopped(release_interrupt_pins[1]);
    rotation.clearSensorWhileStopped(rotation_interrupt_pins[0]);
    rotation.clearSensorWhileStopped(rotation_interrupt_pins[1]);

    // Attach interrupts to limit switch pins
    attachInterrupt(digitalPinToInterrupt(release_interrupt_pins[1]), releaseLimit, RISING);
    attachInterrupt(digitalPinToInterrupt(rotation_interrupt_pins[0]), leftLimit, RISING);
    attachInterrupt(digitalPinToInterrupt(rotation_interrupt_pins[1]), rightLimit, RISING);

    Serial.println("\nSelect motor and movement...");
}


void loop() {
    if (Serial.available()) {
        decodeCommand(); // Process incoming commands from serial
    }
    waitMillis(250);  // Wait a bit while decoding command
}

// Function to handle release limit switch interrupt
void releaseLimit() {
    release.active_interrupt_pin = release_interrupt_pins[0];
    release.limitDetected();
}

// Function to handle left limit switch interrupt for rotation
void leftLimit() {
    rotation.limitDetected();
    rotation.active_interrupt_pin = rotation_interrupt_pins[0];
}

// Function to handle right limit switch interrupt for rotation
void rightLimit() {
    rotation.limitDetected();
    rotation.active_interrupt_pin = rotation_interrupt_pins[1];
}

// Decode incoming serial command to control motors and actuators
void decodeCommand() {
    long command = Serial.parseInt();

    // Extract motor and movement information from command
    String motor_names[4] = {"release", "rotation", "incline", "elevation"};
    int motor_select = 1000;
    int motor = abs(floor(command / motor_select));
    Serial.println("Case: " + String(motor));
    int movement = command % motor_select;

    String motor_name = motor_names[motor - 1];

    // Determine action based on command
    switch (motor) {
        case 1:
            release.releaseBall(movement);
            break;
        case 2:
            rotation.moveDegrees(movement);
            break;
        case 3:
            incline.moveByPercentage(movement);
            break;
        case 4:
            elevation.moveByPercentageRange(movement);
            break;
        case 8:
            // Handle motor recalibration
            int motor_calibration = abs(floor(movement / 100));
            motor_name = motor_names[motor_calibration - 1];
            Serial.println("Recalibrating: " + String(motor_name));

            switch (motor_calibration) {
                case 1:
                    release.moveDegrees(release_nsteps);
                    break;
                case 2:
                    rotation.findRange();
                    break;
                case 3:
                    incline.findRange();
                    break;
                case 4:
                    elevation.findRange();
                    break;
                case 5:
                    elevation.presetRange(elevator_manual_limits[1], elevator_manual_limits[2]);
                    break;
                case 7:
                    // Full system calibration
                    release.moveDegrees(release_nsteps);
                    rotation.findRange();
                    elevation.findRange();
                    elevation.moveToPercentageRange(50);
                    break;
                case 8:
                    // Reset to calibrated positions
                    release.moveDegrees(release_nsteps);
                    rotation.moveToMiddle();
                    elevation.moveToPercentageRange(50);
                    break;
                default:
                    Serial.println("Incorrect command to calibrate");
            }
            break;
        default:
            Serial.println("Incorrect command: " + String(command));
    }

    // Display command information via serial
    if (motor != 9) {
        Serial.println("\nCommand received: " + String(command));
        Serial.println("Movement request: ");
        Serial.println("- Motor: " + motor_name);
        Serial.println("- Movement: " + String(movement));

        Serial.println("\nSelect motor and movement...");
    }
}