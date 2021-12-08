from math import floor
dist_5ft_to_basket = 120

wait_secs = 5

# image helper constants
frame_buffer_size = 10 # number of frames to keep in buffer
frames_threshold = .5 # percent of frames that need to meet criteria
min_frames = floor(frame_buffer_size * frames_threshold)

min_radii_away = 10
ball_hold_threshold = .125

x_ind = 0
y_ind = 1
w_ind = 2
h_ind = 3

'''
Make it so that message to move pops up every so often (actually maybe not bc the gui can take care of it)

Let the person know when they are good to shoot

have custom messaging for calibrating height

Take input from text boxes
'''
