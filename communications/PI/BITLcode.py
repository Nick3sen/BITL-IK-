import serial
import time
import RPi.GPIO as GPIO

# Define serial ports with timeout to avoid blocking on readline()
gripper = serial.Serial("/dev/ttyACM0", 9600, timeout=0.1)  
crane = serial.Serial("/dev/ttyACM1", 9600, timeout=0.1)  
laptop = serial.Serial("/dev/serial0", 9600, timeout=0.1)  

# GPIO setup
GPIO.setmode(GPIO.BCM)
BUTTON_PIN = 17
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

time.sleep(2)  # Allow serial connections to stabilize


def check_button_state(pin=BUTTON_PIN, current_state=0):
    if GPIO.input(pin) == GPIO.LOW:
        if current_state == 0:
            print("Button pressed! Value set to 1")
            time.sleep(0.3)  # debounce
            return 1
    else:
        if current_state == 1:
            print("Button released. Value reset to 0")
            return 0
    return current_state


def send_to_device(device, message):
    device.write((message + "\n").encode())
    print(f"Sent to {device.port}: {message}")
    time.sleep(0.05)  # small delay to let device process


def read_and_process(device):
    # Read all available lines from the device without blocking
    while device.in_waiting > 0:
        try:
            line = device.readline().decode("utf-8", errors="ignore").strip()
        except Exception as e:
            print(f"Error reading from {device.port}: {e}")
            break
        
        if not line:
            break
        
        print(f"Received from {device.port}: {line}")
        parts = parse_data(line)
        if len(parts) < 2:
            continue
        
        # Process according to keyword
        if parts[1] == "move":
            print("Forwarding move command to crane")
            # Defensive slicing if less than expected elements
            send_to_device(crane, " ".join(parts[3:7]))
        elif parts[1] == "ID":
            print("Forwarding ID to laptop")
            if len(parts) > 3:
                send_to_device(laptop, parts[3])


def parse_data(data):
    parts = data.split()
    # Uncomment if you want debug prints:
    # print(parts)
    return parts


# Main loop
try:
    default = ["-2", "0", "-2", "0"]
    button_state = 0

    while True:
        # Read and process data from all devices
        read_and_process(gripper)
        read_and_process(laptop)
        read_and_process(crane)

        # Check button state
        button_state = check_button_state(current_state=button_state)
        if button_state == 1:
            send_to_device(crane, " ".join(default))

        time.sleep(0.01)  # tiny sleep to prevent 100% CPU usage

except KeyboardInterrupt:
    print("\nExiting program.")
    gripper.close()
    crane.close()
    laptop.close()
    GPIO.cleanup()
