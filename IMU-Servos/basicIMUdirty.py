#! /usr/bin/python

# Code adapted from:
# for IMU: https://github.com/adafruit/Adafruit_Python_BNO055, see bottom of code
# for servo: https://www.raspberrypi-spy.co.uk/2018/02/basic-servo-use-with-the-raspberry-pi/

# wires for DSW
# IMU pins:
#   green = vin 3.3/5 volts
#   blue = gnd
#   purple = SCL = pin 5/GPIO3
#   gray = SDA = pin 3/GPIO2

# Servo pins:
#   black = gnd = pin 9
#   white = control = pin11/GPIO17
#   red - vin 3.3 volts = pin 1

# servo imports
from gpiozero import Servo

# IMU imports
import logging
import sys
import time
from Adafruit_BNO055 import BNO055

#misc variables
servoPIN = 17  # this must be the GPIO# not the physical pin #. e.g. to use pin 11 (GPIO17), this must be 17
moveDelay = .2 #a small amount of time to allow the servo to move
moveDelayMultiplier = 5 #sometimes you need the servo to move a great distance, so you can multiply the moveDelay to get a longer wait time
myCorrection = 0.2  # used to correct the motion of the servo. It is servo specific
maxPW = (2.0 + myCorrection) / 1000
minPW = (1.0 - myCorrection - .1) / 1000
servoMaxHeading = 0
servoMinHeading = 0
servoAngle_desired = 0 #initialize teh user input for what angle they want
servoAngle_actual = 0 #where the servo actually is

#variables for position_data()
heading = 0 #between 0 and 360
roll = 0 #unused
pitch = 0 #unused
servoAngle_actual = 0 #where the servo's pointing
servoAngle_desired = 0 #where we want it to point
servoAngle_diff = 0 #the difference between the two
moveDir = 1 #the direction to move the servo
moveBuffer = 5 #how much leeway between the servo angle and the IMU heading reading

#variables for nudge(direction)
servoPos = 0  # initial servo position
moveIncrement = .03  # how much the servo will move for each nudge(), .01 corrosponds to about 1 degree

def position_data():
    global heading #declare global vairables
    global roll
    global pitch
    global servoPos
    global servoAngle_actual
    global servoAngle_desired
    global servoAngle_diff
    global moveDir
    global moveBuffer
    heading, roll, pitch = bno.read_euler()  # we're only using heading
    servoAngle_actual = heading #load the heading of the servo, i.e. the angle it's at now
    servoAngle_diff = abs(servoAngle_actual-servoAngle_desired)#the difference between the servo angle and the desired angle. I.e. how far it need to go
    if servoAngle_diff > 180: #this normalizes the difference so it's always less than 180 degrees away
        servoAngle_diff = servoAngle_diff-180

    #print out relevant info
    print("servoAngle_actual: {} , servoAngle_desired: {}, servoAngle_diff: {}, moveDir: {}, "
          .format(servoAngle_actual, servoAngle_desired, servoAngle_diff, moveDir, ))
    return

def nudge(direction): #this will nudge the servo one direction or another
    global servoPos #declare global vairables
    global moveIncrement
    servoPos = servoPos + direction*moveIncrement #direction is either 1 or -1, so this changes the direction the servo will move
    if servoPos > 1 or servoPos < -1: #make sure the servo isn't outside it's range
        print("The servo is at it's maximum range. Try going the other direction")
        time.sleep(5) #gives you a time to stop the code
        position_data()
        return
    servo.value = servoPos  # move the servo
    time.sleep(moveDelay)
    position_data()
    return

# Create and configure the BNO sensor connection. For I2C
bno = BNO055.BNO055(address=0x29)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

servo = Servo(servoPIN, min_pulse_width=minPW, max_pulse_width=maxPW)  # initalize a servo

#initalize and get the servo's range of motion
servo.value = 1 #move servo all the way in one direction
time.sleep(moveDelay*moveDelayMultiplier) #let the servo move, but wait longer because it's a full sweep of the arm
heading, roll, pitch = bno.read_euler()  # we're only using heading
servoMaxHeading = heading #this is as far as the servo can go
servo.value = -1#move servo all teh way in the other direction
time.sleep(moveDelay*moveDelayMultiplier) #let the servo move, but wait longer because it's a full sweep of the arm
heading, roll, pitch = bno.read_euler()  # we're only using heading
servoMinHeading = heading #this is as far as the servo can go in the other direction
print("servoMaxHeading: {}, servoMinHeading: {}".format(servoMaxHeading, servoMinHeading))

servo.value = 0  # move the servo to 0 heading
time.sleep(moveDelay) #let it move

while True:
    time.sleep(moveDelay)
    position_data() #collect and print data before prompt
    servoAngle_input = input("Enter how many degrees you want to move? (can be positive or negative): ") #ask the user for input angle
    servoAngle_input = float(servoAngle_input)  # inputs are strings, this casts it into a float
    servoAngle_desired = servoAngle_actual+servoAngle_input #the angle we want to move to is where we are + the user's input

    #normalize the desired angle to be between 0 and 360
    if servoAngle_desired > 360:
        servoAngle_desired = servoAngle_desired-360
    if servoAngle_desired < 0:
        servoAngle_desired = servoAngle_desired + 360
    position_data()
    moveDir = 1 #reset moveDir to != 0 before loop runs
    while moveDir != 0:
        if servoAngle_input > 0: #if the input is positive, move the servo in the positive direction
            moveDir = 1
        else:
            moveDir = -1 #else (i.e. input is negative) move servo in the negative direction
        if servoAngle_diff < moveBuffer: #i.e. the arm is within range
           moveDir = 0
           print ("You're there!")
        nudge(moveDir) #move the servo incrimentally

servo.stop()
GPIO.cleanup()

##### end of code, start of legal stuff from borrowed code ####

# Simple Adafruit BNO055 sensor reading example.  Will print the orientation
# and calibration data every second.
#
# Copyright (c) 2015 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
