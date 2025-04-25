#-----------------------this code will consict of the main code for project BITL
import RPi.GPIO as GPIO
from time import sleep

#-----------------------Defining pinsµ
servopins = {1: 3, 2: 5, 3: 7}

for servo, pin in servopins.items(): #using for loop defining individual servo
    GPIO.setup(pin, GPIO.OUT) #Set pin on output
    p = GPIO.PWM(pin, 50) #pin + frequency
    p.start(0)
    servopwm[servo] = p