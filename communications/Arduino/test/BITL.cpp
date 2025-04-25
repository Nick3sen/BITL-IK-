// test library, there is a newer version
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
    Serial.println(_deviceName + " move -2 1 0 0");
}

void BITL::goReceive() {
    Serial.println(_deviceName + " move -1 1 0 0");
}
