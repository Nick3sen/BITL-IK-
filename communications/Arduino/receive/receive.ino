#include "BITL.h"

BITL nano("nano", 9600);

int ledGreen = 5;
int ledRed = 2;
int button = 3;

int ledPin = 13; // Pin connected to the LED (use the built-in LED on pin 13)
String receivedData = ""; // Variable to store received data

void setup(){
    pinMode(ledGreen, OUTPUT);
    pinMode(ledRed, OUTPUT);
    pinMode(button, INPUT);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        String receivedData = Serial.readStringUntil('\n');
        Serial.println("Received: " + receivedData); // Verify received data
        if (receivedData) {
            digitalWrite(ledGreen, HIGH); // Turn on LED
            delay(1000);
            digitalWrite(ledGreen, LOW); // Turn off LED
        } else {
            digitalWrite(ledGreen, LOW); // Turn off LED
        }
    }
}

