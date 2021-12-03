import random

def distance_selector():
    array = [*range(3, 30, 1)]
    return random.choice(array)

def shot_select(distance):
    if distance > 20:
        return 'Shoot the ball {} feet away from the basket. (Behind 3 point line)'.format(distance)
    elif distance == 3:
        return 'Shoot the ball from the free throw line.'
    elif distance > 3:
        return 'Shoot the ball {} feet away from the basket. (Under 3 point line)'.format(distance)