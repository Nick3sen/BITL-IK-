# laptop_echo_client.py
import serial
import time

# Replace COM25 with your actual port from Device Manager
ser = serial.Serial('COM25', 9600, timeout=1)
time.sleep(2)

try:
    while True:
        message = input("Enter message to send to Raspberry Pi: ")
        ser.write((message + '\n').encode())
        print("Message sent. Waiting for echo...")

        # Wait for echo
        time.sleep(0.5)  # Give Pi time to respond
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Echo from Pi: {response}")
except KeyboardInterrupt:
    print("Closing connection.")
    ser.close()
