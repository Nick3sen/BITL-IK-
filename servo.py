import RPi.GPIO as GPIO
from time import sleep
#------------------------- Define variables
servo_1 = 3
#------------------------- Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #Pinmode set to board /pinout in terminal
# GPIO.setup(servo_1, GPIO.OUT) #Set pin on output
# p = GPIO.PWM(servo_1, 50) #pin + frequency
# p.start(0)

#------------------------ calculate dutycycle to angle
def angle(y,x):
    GPIO.setup(y, GPIO.OUT) #Set pin on output
    p = GPIO.PWM(y, 50) #pin + frequency
    p.start(0)
    if x > 180 or x < 0:
        print("angle doesn't exist")
        return
    duty = x / 18 + 3
    p.ChangeDutyCycle(duty)
#------------------------ code
angle(3 , 180)
sleep(1)
angle(3 ,0)
sleep(1)
