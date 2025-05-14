#include "BITL.h"

BITL grijper("grijper", 9600);

int ledGreen = 5;
int ledRed = 2;
int button = 3;

int ledPin = 13;           // Pin connected to the LED (use the built-in LED on pin 13)
String data = "";  // Variable to store received data
String lastData = "";


void setup() {
  pinMode(ledGreen, OUTPUT);
  pinMode(ledRed, OUTPUT);
  pinMode(button, INPUT);
  Serial.begin(9600);
}

void loop() {
  String newData = grijper.receive();
  
  if (newData != "" && newData != lastData) {
    data = newData;
    editdata();
    lastData = newData;
  }
}

void editdata(){
  data.trim();  // Removes whitespace and newline

  int a, b, c, d;
  sscanf(data.c_str(), "%d %d %d %d", &a, &b, &c, &d);

  Serial.print("a = "); Serial.println(a);
  Serial.print("b = "); Serial.println(b);
  Serial.print("c = "); Serial.println(c);
  Serial.print("d = "); Serial.println(d);

  for(int i = 0; i < a; i++){
    digitalWrite(ledGreen, HIGH);
    delay(500);
    digitalWrite(ledGreen, LOW);
    delay(500);
  }
  for(int j = 0; j < c; j++){
    digitalWrite(ledRed, HIGH);
    delay(500);
    digitalWrite(ledRed, LOW);
    delay(500);
  }

}