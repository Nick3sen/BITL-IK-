import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17

def setup_button(pin=BUTTON_PIN):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

try:
    setup_button()
    button_state = 0

    while True:
        button_state = check_button_state(current_state=button_state)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting program.")
    GPIO.cleanup()
