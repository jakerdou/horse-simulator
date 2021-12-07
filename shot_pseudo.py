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














players = []
for i in range(2):
    player = {
        id = 0
        focal_length = None
        misses = 0
        height_inches = 0
        distance_inches = 0
        required_distance = 0
        person = None # an instance of object person that indicates where they will shoot from
        p_frames = []
        ready_for_shot = False
        taking_turn = False
    }
    players.append(player)

for idx, player in enumerate(players):

    player[id] = idx + 1
    print('Player ' + str(player[id]) + ' stand 5 feet away...')
    sleep(5)
    person = None

    while person is None:
        person = find_motionless_person(player['p_frames'], frame)

        if person:
            player['focal_length'] = get_focal_length(person[h_ind], dist_to_basket, player['height_inches'])
            player['p_frames'] = []

print('Player 1 get in position...')
players[0]['taking_turn'] = True
sleep(5)

iters = 0
# while len([players_w5_miss for player in players if player['misses'] == 5]) > 0:
while not game_over(players): # create game_helpers.py to house this function
    for (idx, player) in enumerate(players):
        while player['taking_turn']:
            if not player['ready_for_shot']:
                player['person'] = find_motionless_person(player['p_frames'], frame)

                if player['person'] is not None:
                    player['distance_inches'] = get_person_distance(player['focal_length'], player['height_inches'], player['person'][h_ind])

                    player_in_range = (player['required_distance'] > 0 and .95 * player['required_distance'] <= player['distance_inches'] <= 1.05 * player['required_distance']) or player['required_distance'] <= 0
                    if player_in_range:
                        player['ready_for_shot'] = True

            elif player['ready_for_shot']:
                ball_ready, held_ball = check_holding_ball(frame, player['person'])

                if ball_ready:
                    # shot_made = listen_for_shot()
                    shot_made = True if iters % 3 != 0 else False
                    print('Shot made!' if shot_made else 'Shot missed!')

                    next_player = players[(idx + 1) if idx != len(players) - 1 else 0]

                    if shot_made:
                        next_player['required_distance'] = player['distance_inches']
                    else:
                        if player['required_distance'] > 0:
                            player['misses'] += 1

                    player['distance_inches'] = 0
                    player['required_distance'] = 0
                    player['person'] = None
                    player['p_frames'] = []
                    player['ready_for_shot'] = False
                    player['taking_turn'] = False

                    next_player['taking_turn'] = True


            imgbytes = resize_frame(frame, 130)
            window['image'].update(data=imgbytes)

        iters += 1
