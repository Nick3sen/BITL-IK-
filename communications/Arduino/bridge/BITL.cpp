#include "BITL.h"

BITL::BITL(const String &name, long baud) {
    _deviceName = name;
    baudRate = baud;
    Serial.begin(baudRate);
    Serial.println("Library initialized with name: " + _deviceName);
}

void BITL::sendPos(const String &name, int rowfrom, int heightfrom, int rowto, int heightto) {
    Serial.println(_deviceName + " move " + name + " " + String(rowfrom) + " " + String(heightfrom) + " " + String(rowto) + " " + String(heightto));
}

void BITL::sendID(const String &name, String id) {        
    Serial.println(_deviceName + " ID " + name + " " + id);
}

void BITL::goSend() {
    Serial.println(_deviceName + " move 0 0 0 0");
}

void BITL::goReceive() {
    Serial.println(_deviceName + " move 1 0 0 0");
}

void BITL::receive() { // prints and saves the received data as receivedData
    if (Serial.available() > 0) {
        String receivedData = Serial.readStringUntil('\n');
        Serial.println("Received: " + receivedData); // Verify received data
    }
}