import serial
import time
import RPi.GPIO as GPIO
import time

laptop = serial.Serial("/dev/serial0", 9600)  # Replace with your laptop port

GPIO.setmode(GPIO.BCM)
BUTTON_PIN = 17
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_from_device(device):
    if device.in_waiting > 0:  # Check if data is available
        data = (
            device.readline().decode("utf-8", errors="ignore").strip()
        )  # Read and decode the data
        dataParts = parse_data(data)
        if len(dataParts) == 1:
            return
        # checks the data for keyword
        else:
            if dataParts[1] == "move":
                print("crane")
                # send_to_device(crane, " ".join(dataParts[3:7]))
                print(dataParts[3:7])
            elif dataParts[1] == "ID":
                print("laptop")
                print(dataParts[3])
                # send_to_device(laptop, dataParts[3])
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
    default = ["-2", "0", "-2", "0"]
    button_state = 0

    while True:
        # read_from_device(gripper)
        read_from_device(laptop)
        # print("crane:" + crane.readline().decode().strip())
        # print("gripper" + gripper.readline().decode().strip())
        # Project start, sending str start to crane
        # button_state = check_button_state(current_state=button_state)
        # if button_state == 1:
            # send_to_device(crane, " ".join(default))


except KeyboardInterrupt:
    print("\nExiting program.")
    gripper.close()
    crane.close()
    laptop.close()
    GPIO.cleanup()

