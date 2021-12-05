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
