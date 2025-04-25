import RPi.GPIO as GPIO
import time

# Set up the Raspberry Pi GPIO mode to BOARD (physical pin numbering)
GPIO.setmode(GPIO.BOARD)

# Define the PWM pin (use physical pin 12, which is GPIO 18)
PWM_PIN = 12
GPIO.setup(PWM_PIN, GPIO.OUT)

# Set up PWM at 100Hz frequency (can adjust for smoother output)
pwm = GPIO.PWM(PWM_PIN, 100)
pwm.start(0)  # Start PWM with 0% duty cycle

# Function to simulate reading potentiometer value
def read_potentiometer():
    try:
        while True:
            # Increase duty cycle from 0 to 100% to simulate potentiometer movement
            for dc in range(0, 101, 5):  # Increase every 5% for smoother output
                pwm.ChangeDutyCycle(dc)  # Set duty cycle
                print(f"Potentiometer value (simulated): {dc}%")
                time.sleep(0.1)  # Small delay to simulate gradual change
                
            # Decrease the duty cycle for potentiometer going back
            for dc in range(100, -1, -5):
                pwm.ChangeDutyCycle(dc)
                print(f"Potentiometer value (simulated): {dc}%")
                time.sleep(0.1)
                
    except KeyboardInterrupt:
        print("Program interrupted")

    finally:
        pwm.stop()
        GPIO.cleanup()

# Call function to read potentiometer
read_potentiometer()
