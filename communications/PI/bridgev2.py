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

# GPIO setup
GPIO.setmode(GPIO.BCM)
BUTTON_PIN = 17
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Wait for connections to establish
time.sleep(2)


def check_button_state(pin=BUTTON_PIN, current_state=0):
    """
    Checks the button once. Returns updated state (0 or 1).
    """
    if GPIO.input(pin) == GPIO.LOW:
        if current_state == 0:
            print("Button pressed! Value set to 1")
            time.sleep(0.3)  # Debounce
            return 1
    else:
        if current_state == 1:
            print("Button released. Value reset to 0")
            return 0
    return current_state


def send_to_device(device, message):
    device.write((message + "\n").encode())
    print(message, device)
    time.sleep(0.1)


def read_from_device(device):
    if device.in_waiting > 0:  # Check if data is available
        data = (
            device.readline().decode("utf-8", errors="ignore").strip()
        )  # Read and decode the data
        dataParts = parse_data(data)
        if len(dataParts) == 1:
            return 
        else: 
            if dataParts[1] == "move":
                print("crane")
                send_to_device(crane, ' '.join(dataParts[3:7]))
                print(dataParts[3:7])
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
    default = ['-2', '0', '-2', '0']
    button_state = 0

    while True:
        # Project start, sending str start to crane
        button_state = check_button_state(current_state=button_state)
        if button_state == 1:
            send_to_device(crane, ' '.join(default))

        read_from_device(gripper)
        read_from_device(laptop)


except KeyboardInterrupt:
    print("\nExiting program.")
    gripper.close()
    crane.close()
    laptop.close()
    GPIO.cleanup()