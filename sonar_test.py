import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 23
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
maxTime = 0.04
   
def get_sonar_distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER,False)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.01)
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.0001)
    GPIO.output(GPIO_TRIGGER,False)
    
    # save StartTime
    StartTime = time.time()
    timeout = StartTime + maxTime
    while GPIO.input(GPIO_ECHO) == 0 and StartTime < timeout:
        StartTime = time.time()
 
    # save time of arrival
    StopTime = time.time()
    timeout = StopTime + maxTime
    while GPIO.input(GPIO_ECHO) == 1 and StopTime < timeout:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    return distance

def confirm_shot(d):
    if d <= 10:
        return "Shot made"

count = 0
made_count = 0
shot_made_count = 0
while True:
    dist = get_sonar_distance()
    a = confirm_shot(dist)
    if a == 'Shot made':
        shot_made_count += 1
        if shot_made_count == 1:
            count += 1
    elif shot_made_count > 0 and a != 'Shot made':
        shot_made_count += 1
    if shot_made_count == 15:
        shot_made_count = 0
    #print('Shots made: ', count)
    print(dist)
        