"""
This code was made for BITL 2024-2025
Realised by VTIZ Zandhoven
"""

# Imported libraries
import ikpy.chain
import ikpy.utils.plot as plot_utils
import numpy as np
import time
import math
import ipywidgets as widgets
import serial
import matplotlib.pyplot as plt
import os
import RPi.GPIO as GPIO
from time import sleep

# Default servo code
servopins = {1: 3, 2: 35, 3: 37}
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #Pinmode set to board /pinout in terminal
servopwm = {}

for servo, pin in servopins.items(): #using for loop defining individual servo
    GPIO.setup(pin, GPIO.OUT) #Set pin on output
    p = GPIO.PWM(pin, 50) #pin + frequency
    p.start(0)
    servopwm[servo] = p

def angle(index, x):
    if x > 180 or x < 0:
        print("angle doesn't exist")
        return
    duty = x / 18 + 3
    servopwm[index].ChangeDutyCycle(duty)

# Default stepper code
in1=11
in2=12
in3=13
in4=15

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

# Getting absolute path
pwd_path= os.path.dirname(os.path.abspath(__file__))
myfile = os.path.join(pwd_path, 'BITL.urdf')

# aquiring the robot information and target position
my_chain = ikpy.chain.Chain.from_urdf_file(myfile,active_links_mask=[True, True, True, True, True, True])
target_position = [ 0.1, 0.2,0.2]
target_orientation = [-1, 0, 0]

# Calculating and saving angles of the servo's using inverse kinematics
ik = my_chain.inverse_kinematics(target_position, target_orientation, orientation_mode="Y")
angles = list(map(lambda r:math.degrees(r),ik.tolist()))
print("The angles of each joints are : ", angles)

# Controlling angles with forward kinematics
computed_position = my_chain.forward_kinematics(ik)
print("Computed position: %s, original position : %s" % (computed_position[:3, 3], target_position))
print("Computed position (readable) : %s" % [ '%.2f' % elem for elem in computed_position[:3, 3] ])

# Plotting the robotic arm
def showPlot(): 
    fig, ax = plot_utils.init_3d_figure()
    fig.set_figheight(9)
    fig.set_figwidth(13)  
    my_chain.plot(ik, ax, target=target_position)
    plt.xlim(-0.5, 0.5)
    plt.ylim(-0.5, 0.5)
    ax.set_zlim(0, 0.6)
    plt.ion()
    plt.show(block = True)

# Functions
def doIK():
    global ik
    old_position= ik.copy()
    ik = my_chain.inverse_kinematics(target_position, target_orientation, orientation_mode="Z", initial_position=old_position)

def updatePlot():
    ax.clear()
    my_chain.plot(ik, ax, target=target_position)
    plt.xlim(-0.5, 0.5)
    plt.ylim(-0.5, 0.5)
    ax.set_zlim(0, 0.6)
    fig.canvas.draw()
    fig.canvas.flush_events()

# # Moving function 
# def move(x,y,z):
#     global target_position
#     target_position = [x,y,z]
#     doIK()
#     updatePlot()
#     sendCommand(ik[1].item(),ik[2].item(),ik[3].item(),ik[4].item(),ik[5].item(),ik[6].item(),1)

# def servo():
#     move(0,0.2,0.3)

# ser = serial.Serial('COM3',9600, timeout=1)

# def sendCommand(a,b,c,d,e,f,move_time):
#     command = '0{:.2f} 1{:.2f} 2{:.2f} 3{:.2f} 4{:.2f} 5{:.2f} t{:.2f}\n'.format(math.degrees(a),math.degrees(b),math.degrees(c),math.degrees(d),math.degrees(e),math.degrees(f),move_time)
#     ser.write(command.encode('ASCII'))

# we'll call sendCommand once with a move time of 4s so the robot slowly moves to the initial point
sendCommand(ik[1].item(),ik[2].item(),ik[3].item(),ik[4].item(),ik[5].item(),ik[6].item(),4)

ser.close() 