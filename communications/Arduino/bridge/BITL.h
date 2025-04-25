#ifndef BITL_H
#define BITL_H

#include <Arduino.h>

class BITL {
    public:
        BITL(const String &name, long baud);  // Constructor
        void sendPos(const String &name, int rowfrom, int heightfrom, int rowto, int heightto);  
        void sendID(const String &name, String id);  
        void goSend();
        void goReceive();
        void receive();
    private:
        String _deviceName;
        long baudRate;
};

#endif