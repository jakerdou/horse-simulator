# import the necessary packages
import numpy as np
import cv2
import imutils
from functools import cmp_to_key
from math import floor
from time import sleep

frame_buffer_size = 10 # number of frames to keep in buffer
frames_threshold = .5 # percent of frames that need to meet criteria
min_frames = floor(frame_buffer_size * frames_threshold)

min_radii_away = 10
ball_hold_threshold = .125

x_ind = 0
y_ind = 1
w_ind = 2
h_ind = 3

# Malisiewicz et al.
def non_max_suppression_fast(boxes, overlapThresh):
	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return []
	# if the bounding boxes integers, convert them to floats --
	# this is important since we'll be doing a bunch of divisions
	if boxes.dtype.kind == "i":
		boxes = boxes.astype("float")
	# initialize the list of picked indexes
	pick = []
	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]
	# compute the area of the bounding boxes and sort the bounding
	# boxes by the bottom-right y-coordinate of the bounding box
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(y2)
	# keep looping while some indexes still remain in the indexes
	# list
	while len(idxs) > 0:
		# grab the last index in the indexes list and add the
		# index value to the list of picked indexes
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)
		# find the largest (x, y) coordinates for the start of
		# the bounding box and the smallest (x, y) coordinates
		# for the end of the bounding box
		xx1 = np.maximum(x1[i], x1[idxs[:last]])
		yy1 = np.maximum(y1[i], y1[idxs[:last]])
		xx2 = np.minimum(x2[i], x2[idxs[:last]])
		yy2 = np.minimum(y2[i], y2[idxs[:last]])
		# compute the width and height of the bounding box
		w = np.maximum(0, xx2 - xx1 + 1)
		h = np.maximum(0, yy2 - yy1 + 1)
		# compute the ratio of overlap
		overlap = (w * h) / area[idxs[:last]]
		# delete all indexes from the index list that have
		idxs = np.delete(idxs, np.concatenate(([last],
			np.where(overlap > overlapThresh)[0])))
	# return only the bounding boxes that were picked using the
	# integer data type
	return boxes[pick].astype("int")

def find_persons(frame):
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    # persons, weights =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
    persons, weights =  HOGCV.detectMultiScale(frame, winStride = (6, 6), padding = (8, 8), scale = 1.1)
    # print(pedestrians)
    # print(weights)

    persons = non_max_suppression_fast(persons, .3)

    return persons

def draw_persons(frame, persons):
    for idx, (x,y,w,h) in enumerate(persons):
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        font = cv2.FONT_HERSHEY_DUPLEX
        # cv2.putText(frame, 'Person\n' + str(weights[idx]), (x + 6, y - 6), font, 0.5, (0, 255, 0), 1)
        cv2.putText(frame, 'Person', (x + 6, y - 6), font, 0.5, (0, 255, 0), 1)

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

def find_ball(frame):
	# big ball
    # orangeLower = (7, 141, 80)
    # orangeUpper = (15, 206, 206)

	# small ball
#     orangeLower = (0, 81, 80)
#     orangeUpper = (10, 170, 152)
    orangeLower = (0, 74, 51)
    orangeUpper = (14, 173, 110)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "orange", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, orangeLower, orangeUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

    return Ball(x, y, radius) if len(cnts) > 0 else None

def draw_ball(frame, ball):
    # only proceed if the radius meets a minimum size
    if ball and ball.radius > 10:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(frame, (int(ball.x), int(ball.y)), int(ball.radius),
            (0, 255, 255), 2)

def find_motionless_person(p_frames, frame):

	# find and draw people on frame
	persons = find_persons(frame)
	draw_persons(frame, persons)

	# add frame to buffer
	if len(p_frames) < frame_buffer_size:
		p_frames.append(persons)
	else:
		del p_frames[0]
		p_frames.append(persons)

	# look through frames for motionless person
	def compare_persons(a, b):
		return b[w_ind] * b[h_ind] - a[w_ind] * a[h_ind]

	area_percent_threshold = .8
	distance_threshold = 100

	if len(p_frames) > min_frames:
	    flat_list = [item for sublist in p_frames for item in sublist]
	    if len(flat_list) > min_frames:
	        flat_list.sort(key=cmp_to_key(compare_persons))
	        # print(flat_list)
	        first_person = flat_list[0]
	        base_area = first_person[w_ind] * first_person[h_ind]
	        base_x = first_person[x_ind]
	        base_y = first_person[y_ind]

	        for i in range(1, min_frames):
	            person = flat_list[i]
	            percent_of_base_area = person[w_ind] * person[h_ind] / base_area
	            distance_from_base = ((person[x_ind] - base_x)**2 + (person[y_ind] - base_y)**2)**.5
	            if percent_of_base_area < area_percent_threshold or distance_from_base > distance_threshold:
	                return None

	        # print('Found a person ready to shoot')
	        med_ind = floor(frame_buffer_size / 4)
	        # return flat_list[med_ind]
	        # return flat_list[0][3], flat_list[0][0], flat_list[0][2]
	        return flat_list[med_ind]

	return None

def get_focal_length(base_height_pixels, dist_to_basket, height_inches):
	# TODO: put in GUI
	print('Height calibrated, get in position')
	for i in range(3):
		print(str(3 - i), end=', ')
		sleep(1)
	print()

	return (base_height_pixels * dist_to_basket) / height_inches

def get_person_distance(focal_length, height_inches, height_pixels):
	distance_inches = (focal_length * height_inches) / height_pixels

	# TODO: put in GUI
	print('You are ' + str(distance_inches)[0:6] + ' inches away, hold the ball at about eye level...')

	return distance_inches

def check_holding_ball(frame, person):
	ball = find_ball(frame)
	draw_ball(frame, ball)
	draw_persons(frame, [person])

	if ball is None:
	    return False, None
	else:
	    x_in_range = person[x_ind] <= ball.x <= person[x_ind] + person[w_ind]
	    y_in_range = person[y_ind] <= ball.y <= person[y_ind] + person[h_ind] * ball_hold_threshold
	    if x_in_range and y_in_range:
	        return True, ball
	    else:
	        return False, None

def shot_taken(b_frames, held_ball, person):
    # print('in shot taken')
    # remove values that are None
    b_frames = [frame for frame in b_frames if frame is not None]

    if len(b_frames) < min_frames:
        return False
    else:
        # print('in else in shot taken')
        # is there a frame in which the ball is over the persons head
        ball_overhead = False
        # is there a frame in which the ball is the minimum distance away from where it started (in the y direction)
        ball_min_distance_away = False

        for ball in b_frames:
            if person[x_ind] <= ball.x <= person[x_ind] + person[w_ind] and ball.y < person[y_ind]:
                # print('ball overhead')
                ball_overhead = True
            if held_ball.y - ball.y > held_ball.radius * min_radii_away:
                # print('ball min distance')
                ball_min_distance_away = True
            if ball_overhead and ball_min_distance_away:
                return True
        return False

def resize_frame(frame, percent):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)

    # resize image
    resized_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    imgbytes = cv2.imencode('.png', resized_frame)[1].tobytes()

    return imgbytes
