# pi_send_input.py
import serial
import time

# Open serial port to laptop
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(2)  # Wait for the serial connection to stabilize

try:
    while True:
        message = input("Enter message to send to laptop: ")
        ser.write((message + '\n').encode())
        print(f"Sent: {message}")
except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
