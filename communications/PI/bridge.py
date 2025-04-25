"""
Code made for BITL 24-25
Made by 5TWA VTIZandhoven
"""

import serial
import time

# Define serial ports for each device
gripper = serial.Serial('/dev/ttyUSB0', 9600)  # Replace with your Arduino port
crane = serial.Serial('/dev/ttyACM0', 9600)  # Replace with your Arduino port
# laptop = serial.Serial('/dev/ttyUSB2', 9600)    # Replace with your laptop port

# Wait for connections to establish
time.sleep(2)

def send_to_device(device, message):
    device.write((message + '\n').encode())
    time.sleep(0.1)

def read_from_device(device):
    if device.in_waiting > 0:  # Check if data is available
        data = device.readline().decode('utf-8').strip()  # Read and decode the data
        parse_data(data)
        print(f"Received: {data}")
        if parse_data[1] == move:
            send_to_device(crane, parse_data[3-6])

def parse_data(data):
    # Split the data into individual components
    data_parts = data.split()
    print(data_parts)
    for i in range(len(data_parts)):
        print(data_parts[i])


# Main loop
try:
    while True:
        # Example: Send commands
        send_to_device(gripper, "Command to Arduino 1")
        send_to_device(crane, "Command to Arduino 2")
        # Read responses
        read_from_device(gripper)
        read_from_device(crane)

except KeyboardInterrupt:
    print("Exiting...")
    gripper.close()
    crane.close()
    # laptop.close()
