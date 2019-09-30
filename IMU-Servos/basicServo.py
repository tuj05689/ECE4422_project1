# This code was adapted from the URL:
#    https://www.raspberrypi-spy.co.uk/2018/02/basic-servo-use-with-the-raspberry-pi/

#! /usr/bin/python

from gpiozero import Servo
from time import sleep

#Servo pins:
#   black = gnd = pin 9
#   white = control = pin11/GPIO17
#   red - vin 3.3 volts = pin 1


servoPIN = 17  # this must be the GPIO# not the physical pin #. e.g. to use pin 11 (GPIO17), this must be 17
moveDelay = 0.75
myCorrection = 0.2  # used to correct the motion of the servo. It is servo specific
maxPW = (2.0 + myCorrection) / 1000
minPW = (1.0 - myCorrection - .1) / 1000

servo = Servo(servoPIN, min_pulse_width=minPW, max_pulse_width=maxPW)  # initalize a servo

# swings the arm back and forth, because it feels like there should be some sort of startup sequence
servo.value = -1
sleep(moveDelay)
servo.value = 1
sleep(moveDelay)
servo.value = 0
sleep(moveDelay)

while True:  # user inputs a position for the servo.
    servoPos = input("Enter positioin value between -1 and 1: ")
    servoPos = float(servoPos)
    if servoPos <= 1 and servoPos >= -1:
        servo.value = servoPos
    else:
        print("ERROR: Position value must be between -1 and 1.")

servo.stop()
GPIO.cleanup();
