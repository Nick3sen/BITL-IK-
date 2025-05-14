# laptop_send.py
import serial
import time

# Replace 'COMx' with the actual COM port the CP2102 is using (e.g., 'COM4')
ser = serial.Serial('COM25', 9600, timeout=1)
time.sleep(2)  # Wait for connection to establish

try:
    while True:
        message = input("Enter message to send to Raspberry Pi: ")
        ser.write((message + '\n').encode())
        print("Message sent.")
except KeyboardInterrupt:
    print("Closing connection.")
    ser.close()
