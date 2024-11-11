import RPi.GPIO as GPIO
from time import sleep
#------------------------- Define servo index for each pin
servopins = {1: 3, 2: 5, 3: 7}
#------------------------- Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #Pinmode set to board /pinout in terminal
servopwm = {}

for servo, pin in servopins.items(): #using for loop defining individual servo
    GPIO.setup(pin, GPIO.OUT) #Set pin on output
    p = GPIO.PWM(pin, 50) #pin + frequency
    p.start(0)
    servopwm[servo] = p

#------------------------ calculate dutycycle to angle
def angle(index, x):
    if x > 180 or x < 0:
        print("angle doesn't exist")
        return
    duty = x / 18 + 3
    servopwm[index].ChangeDutyCycle(duty)
#------------------------ code
angle(1, 180)
sleep(1)
angle(1, 0)
sleep(1)

#/general information
# Raspberry pi shutdown => connect pin 5 and 6 (GPIO and GND)
