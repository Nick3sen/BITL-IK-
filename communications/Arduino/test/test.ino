#include "BITL.h"

BITL nano("nano", 9600);

int ledGreen = 5;
int ledRed = 2;
int button = 3;

void setup(){
    pinMode(ledGreen, OUTPUT);
    pinMode(ledRed, OUTPUT);
    pinMode(button, INPUT);
    Serial.begin(9600);
}

void loop(){
    if (digitalRead(button) == HIGH)
    {
        digitalWrite(ledGreen, HIGH);
        digitalWrite(ledRed, LOW);
        nano.sendPos("software", 4, 2, 1, 1);
        delay(2000);
    }
    else{
        digitalWrite(ledGreen, LOW);
        digitalWrite(ledRed, HIGH);
    }
}