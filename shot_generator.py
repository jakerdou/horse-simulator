import random

def distance_selector():
    array = [*range(2, 30, 1)]
    return random.choice(array)

def shot_select(distance):
    if distance > 20:
        return 'Shoot the ball {} feet away from the basket. (Behind 3 point line)'.format(distance)
    elif distance == 2:
        return 'Take a left-handed layup'
    elif distance == 3:
        return 'Take a right-handed layup'
    elif distance > 3:
        return 'Shoot the ball {} feet away from the basket. (Under 3 point line)'.format(distance)