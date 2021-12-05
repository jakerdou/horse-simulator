person_frames = last x amount of frames' persons arrays
person_detected = list of size x consisting of boolean values of whether or not a person was detected in those frames

ball_frames
ball_detected

if half of the person frames detect a person that is within x percent size and x percent distance of all the frames, consider that a person and lock it in place until a shot is taken

person = four corners of person that was detected

turn LED green

find the lowest and highest point of the ball in the ball frames, if that distance is x times the radius of the ball, consider a shot to have been taken

see if the us sensor senses something in the next 3 seconds, if so, shot made, if not, shot missed

repeat

if base height not found
look for it
if you find it

height_calibrated = False
person_ready_for_shot = False
person_holding_ball = False
focal_length = None
distance = None
p_frames = []
b_frames = []


if not person_ready_for_shot:
    persons = find_persons(frame)
    draw_persons(persons)
    p_frames = add_to_frames(persons)
    person = calibrate_height(p_frames)

    if person:
        if not height_calibrated:
            base_height = person[h_ind]
            focal_length = some calculation
            distance = some calculation
            height_calibrated = True
        else:
            distance = some calculation
            print('You are ____ distance away')
            person_ready_for_shot = True
else:
    ball = find_ball(frame)
    draw_ball(ball)
    draw_persons([person])
    b_frames = add_to_frames(ball)

    if not person_holding_ball:
        person_holding_ball = check_holding_ball(ball, person)
    else:
        if shot_taken(b_frames, person):
            person_ready_for_shot = False
            person_holding_ball = False
            focal_length = None
            distance = None
            p_frames = []
            b_frames = []
