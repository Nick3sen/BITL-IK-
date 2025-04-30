"""
Code made for BITL 24-25
Made by 5TWA VTI Zandhoven
"""

import serial
import time

# Define serial ports for each device
gripper = serial.Serial("/dev/ttyUSB0", 9600)  # Replace with your Arduino port
crane = serial.Serial("/dev/ttyACM0", 9600)  # Replace with your Arduino port
laptop = serial.Serial("/dev/ttyUSB2", 9600)  # Replace with your laptop port

# Wait for connections to establish
time.sleep(2)


def parse_data(data):
    # Split the data into individual components
    data_parts = data.split()
    print(data_parts)


# Sending a message through uft-8 encoding
def send_to_device(device, message):
    print(f"Sending: {message}")
    device.write((message + "\n").encode("utf-8"))
    time.sleep(0.1)


# Receiving a message and decoding it
def read_from_device(device):
    if device.in_waiting > 0:  # Check if data is available
        data = device.readline().decode("utf-8").strip()  # Read and decode the data
        parse_data(data)
        print(f"Received: {data}")


# Main loop
try:
    while True:
        read_from_device(gripper)
        read_from_device(crane)
        read_from_device(laptop)

except KeyboardInterrupt:
    print("Exiting...")
    gripper.close()
    crane.close()
    laptop.close()
