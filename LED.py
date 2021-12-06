import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

red = 26
green = 16


GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)

def yellow_light():   #calibration
    GPIO.output(red, 0)
    GPIO.output(green, 0)

def green_light():    #in camera view
    GPIO.output(red, 1)
    GPIO.output(green, 0)

def red_light():      #not in camera view
    GPIO.output(red, 0)
    GPIO.output(green, 1)

def off():
    GPIO.output(red, 1)
    GPIO.output(green, 1)
    