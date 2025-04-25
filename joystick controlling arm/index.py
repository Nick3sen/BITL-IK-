import RPi.GPIO as GPIO
from time import sleep

# defining pins and ports
servopins = {1: 3, 2: 35, 3: 37}
in1=11
in2=12
in3=13
in4=15
# ----------------------------------Servo-------------------------------- #

for servo, pin in servopins.items(): #using for loop defining individual servo
    GPIO.setup(pin, GPIO.OUT) #Set pin on output
    p = GPIO.PWM(pin, 50) #pin + frequency
    p.start(0)
    servopwm[servo] = p

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #Pinmode set to board /pinout in terminal
servopwm = {}

# dutycycle to angle 
def angle(index, x):
    if x > 180 or x < 0:
        print("angle doesn't exist")
        return
    duty = x / 18 + 3
    servopwm[index].ChangeDutyCycle(duty)

# ----------------------------------Stepper-------------------------------- #

step_sleep = 0.002
steps = 4096
direction = False #true is clockwise false is counter clockwise

step_sequence = [[1,0,0,1], # find in documentation 
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT) #for loop
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

GPIO.output(in1, GPIO.LOW) #for loop
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
motor_pins = [in1, in2, in3, in4]
motor_step_counter = 0

def cleanup():
    GPIO.output(in1, GPIO.LOW) #for loop
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    GPIO.cleanup()

def stepper(step_count):
    i = 0
    for i in range(step_count):
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        if direction==True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction==False:
            motor_step_counter = (motor_step_counter + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( step_sleep )

# ----------------------------------Actual code-------------------------------- #
