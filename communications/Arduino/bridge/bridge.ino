#include "BITL.h"

BITL grijper("grijper", 9600);

// kraan en grijper

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
    Serial.println('READY');
}

void loop() {
  if (digitalRead(button)== HIGH){
    grijper.sendPos("gripper", 3, 0, 3, 0);
    digitalWrite(ledGreen, HIGH);
    delay(200);
    digitalWrite(ledGreen, LOW);
  }
}