import serial
import time

# Set up serial connection
arduino = serial.Serial('/dev/serial0', 9600)  # Replace '/dev/ttyUSB0' with the actual port

# Allow time for the connection to establish
time.sleep(2)

print("Listening for data from Arduino...")

while True:
    if arduino.in_waiting > 0:  # Check if data is available
        data = arduino.readline().decode('utf-8').strip()  # Read and decode the data
        print(f"Received: {data}")

"""
data list: [to, fH, fR, tH, tR]
to: een index die aangeeft naar welk adres

"""