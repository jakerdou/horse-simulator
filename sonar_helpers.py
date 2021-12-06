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
    if d <= 5:
        return "Shot made"

def listen_for_shot():
    # TODO: put in GUI
    print('Shoot!\nYou have 5 seconds before the system will reset and you can shoot again')

    start = time.perf_counter()
    distance_frames = []

    seconds = 1
    while time.perf_counter() - start < 5:
        if seconds * .95 < time.perf_counter() - start < seconds * 1.05:
            print(str(seconds), ', ')
            seconds += 1
        distance_frames.append(get_sonar_distance())
    print('# of measurements <= 10 ' + str(len([d for d in distance_frames if d <= 10])))
    print('# of measurements <= 9 ' + str(len([d for d in distance_frames if d <= 9])))
    print('# of measurements <= 8 ' + str(len([d for d in distance_frames if d <= 8])))
    print('# of measurements <= 7 ' + str(len([d for d in distance_frames if d <= 7])))
    print('# of measurements <= 6 ' + str(len([d for d in distance_frames if d <= 6])))
    print('# of measurements <= 5 ' + str(len([d for d in distance_frames if d <= 5])))

    if len([d for d in distance_frames if d <= 5]) > 0:
        print('Shot made')
        return True
    else:
        print('Shot missed')
        return False

# count = 0
# made_count = 0
# shot_made_count = 0
# while True:
#     dist = get_sonar_distance()
#     a = confirm_shot(dist)
#     if a == 'Shot made':
#         shot_made_count += 1
#         if shot_made_count == 1:
#             count += 1
#     elif shot_made_count > 0 and a != 'Shot made':
#         shot_made_count += 1
#     if shot_made_count == 15:
#         shot_made_count = 0
#     #print('Shots made: ', count)
#     print(dist)