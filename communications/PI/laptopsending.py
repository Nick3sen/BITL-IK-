# laptop_sender.py
import serial
import time

# Change this to the correct port for your laptop
SERIAL_PORT = '/dev/ttyUSB0'  # or 'COMx' on Windows
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # wait for the serial connection to initialize

try:
    while True:
        message = "Hello from Laptop!\n"
        ser.write(message.encode('utf-8'))
        print(f"Sent: {message.strip()}")
        time.sleep(1)
except KeyboardInterrupt:
    ser.close()
    print("Connection closed.")
