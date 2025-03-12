# Importing libraries
import ikpy.chain
import ikpy.utils.plot as plot_utils

import numpy as np
import time
import math

import ipywidgets as widgets
import serial

import matplotlib.pyplot as plt
import os

# Retrieving URDF file path
pwd_path= os.path.dirname(os.path.abspath(__file__))
myfile = os.path.join(pwd_path, 'BITL.urdf')
print(myfile)

motorpins = {1: 3, 2: 35, 3: 37}

# Creating IK chain
my_chain = ikpy.chain.Chain.from_urdf_file(myfile)
target_position = [ 0.1, 0.2,0.02]
target_orientation = [0, 0, 0]

# calculating the right angles
ik = my_chain.inverse_kinematics(target_position, target_orientation, orientation_mode="Y")
angles = list(map(lambda r:math.degrees(r),ik.tolist()))
print("The angles of each joints are : ", angles)

# Plotting the angles 
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

def showAngles(listHoeken, motorpins):
    for (servo, pin), angle in zip(motorpins.items(), listHoeken):  # Pair each servo with its corresponding angle
        print(f'Servo {servo} op pin {pin} staat {angle:.2f} graden gedraaid')

showAngles(angles, motorpins)

computed_position = my_chain.forward_kinematics(ik)
print("Computed position: %s, original position : %s" % (computed_position[:3, 3], target_position))
print("Computed position (readable) : %s" % [ '%.2f' % elem for elem in computed_position[:3, 3] ])

showPlot()
