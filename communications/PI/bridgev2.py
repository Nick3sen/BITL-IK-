"""
Code made for BITL 24-25
Made by 5TWA VTIZandhoven
"""

import serial
import time
import RPi.GPIO as GPIO
import time

# Define serial ports for each device
gripper = serial.Serial("/dev/ttyUSB0", 9600)  # Replace with your Arduino port
crane = serial.Serial("/dev/ttyACM0", 9600)  # Replace with your Arduino port
laptop = serial.Serial("/dev/ttyUSB2", 9600)  # Replace with your laptop port

#GPIO setup
GPIO.setmode(GPIO.BCM)
BUTTON_PIN = 17
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
button_state = 0

# Wait for connections to establish
time.sleep(2)


def send_to_device(device, message):
    device.write((message + "\n").encode())
    time.sleep(0.1)


def read_from_device(device):
    if device.in_waiting > 0:  # Check if data is available
        data = (
            device.readline().decode("utf-8", errors="ignore").strip()
        )  # Read and decode the data
        dataParts = parse_data(data)
        if dataParts[1] == "move":
            print("crane")
            send_to_device(crane, dataParts[3 - 6])
        elif dataParts[1] == "ID":
            print("laptop")
            send_to_device(laptop, dataParts[3])
        data = ""
        dataParts = []
        return


def parse_data(data):
    # Split the data into individual components
    dataParts = data.split()
    print(dataParts)
    for i in range(len(dataParts)):
        print(dataParts[i])
    return dataParts


# Main loop

try:
    while True:

        read_from_device(gripper)


except KeyboardInterrupt:
    print("\nExiting program.")
    gripper.close()
    crane.close()
    laptop.close()
    GPIO.cleanup()