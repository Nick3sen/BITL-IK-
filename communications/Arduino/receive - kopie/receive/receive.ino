#include "BITL.h"

BITL grijper("grijper", 9600);

int ledGreen = 5;
int ledRed = 2;
int button = 3;

int ledPin = 13;           // Pin connected to the LED (use the built-in LED on pin 13)
String data = "";  // Variable to store received data
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
    Serial.println("HIGH");
    digitalWrite(9, HIGH);
    digitalWrite(ledGreen, HIGH);
    delay(100);
    digitalWrite(ledRed, LOW);
    delay(500);
    laststate = 1;
  }
  if(digitalRead(button)== HIGH && laststate == 1){
    Serial.println("LOW");
    digitalWrite(9, LOW);
    digitalWrite(ledRed, HIGH);
    delay(100);
    digitalWrite(ledGreen, LOW);
    delay(500);
    laststate = 0;
  }
  Serial.println(digitalRead(9));
  delay(500);
}