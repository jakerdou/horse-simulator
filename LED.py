import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

red = 16
green = 26


GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)

def yellow_light():   #calibration
    GPIO.output(red, 1)
    GPIO.output(green, 1)

def green_light():    #in camera view
    GPIO.output(green, 1)
    GPIO.output(red, 0)

def red_light():      #not in camera view
    GPIO.output(red, 1)
    GPIO.output(green, 0)

def off(pin):
    GPIO.output(pin, 0)