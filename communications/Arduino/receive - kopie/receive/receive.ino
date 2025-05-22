#include "BITL.h"

BITL grijper("grijper", 9600);

int ledGreen = 5;
int ledRed = 2;
int button = 3;

int ledPin = 13;           // Pin connected to the LED (use the built-in LED on pin 13)
String data = "ABDC";  // Variable to store received data
String lastData = "";
int laststate = 1;


void setup() {
  pinMode(ledGreen, OUTPUT);
  pinMode(ledRed, OUTPUT);
  pinMode(button, INPUT);
  Serial.begin(9600);
}

void loop() {
  if(digitalRead(button)== HIGH && laststate == 0){
    grijper.sendID(grijper, data)
  }
  if(digitalRead(button)== HIGH && laststate == 1){
    grijper.sendID(grijper, lastData)
  }
  delay(500);
}