import RPi.GPIO as GPIO
import time

# Use BCM numbering (GPIO numbers, not pin numbers)
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin
BUTTON_PIN = 17

# Set up the button pin as input with an internal pull-up resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variable to change
button_state = 0

try:
    print("Waiting for button press. Press CTRL+C to exit.")
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            if button_state == 0:
                button_state = 1
                print("Button pressed! Value set to 1")
                time.sleep(0.3)  # Debounce delay
        else:
            if button_state == 1:
                button_state = 0
                print("Button released. Value reset to 0")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting program.")
    GPIO.cleanup()
