import PySimpleGUI as sg
import numpy as np
import imutils
from collections import deque
from time import sleep
from matplotlib.ticker import NullFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.gui import *
from src.shotchart import *
from src.shot_generator import *
from src.LED import *
from src.sonar_helpers import *
from src.image_helpers import *
from src.game_helpers import *
from src.constants import *

if __name__ == '__main__':
    # Default GUI view is the menu
    mode = 'menu'

    # main loop where GUI is opened
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            break
        # print(event)

        if mode == 'menu':
            if event == 'Shootaround':
                window['menu'].update(visible=False)
                window['shootaround'].update(visible=True)
                mode = 'shootaround'
            elif event == 'Single Player':
                window['menu'].update(visible=False)
                window['single_player'].update(visible=True)
                mode = 'single_player'
            elif event == 'Multiplayer':
                window['menu'].update(visible=False)
                window['multi_player'].update(visible=True)
                mode = 'multi_player'

        elif mode == 'shootaround':
            #opening page, enter height and click ok, else cancel and return to main
            # feet = values[0]
            # inches = values[1]
            feet = '5'
            inches = '11'
            if event == 'OK' and feet != '' and inches != '':
                height_inches = int(feet) * 12 + int(inches)

                window['shootaround'].update(visible=False)
                window['camera'].update(visible=True)

                # sonic = 0
                # cam = 0
                makes = 0
                misses = 0
                three_makes = 0
                three_misses = 0
                # x = 0
                # y = 0

                cap = cv2.VideoCapture(0)
                # sleep(2)
                if not cap.isOpened():
                    print('capture failed to open')

                waited_for_person_to_move = False
                height_calibrated = False
                ready_for_shot = False
                ball_ready = False
                focal_length = None
                distance = None
                held_ball = None
                p_frames = []

                # TODO: put in GUI
                print('stand ~10 feet away from the camera for height calibration')
                for i in range(wait_secs):
                    print(str(wait_secs - i), end=', ')
                    sleep(1)
                print()

                while event != 'Finished':

                    # camera code
                    event, values = window.read(timeout=20)

                    # when calibration is done, instruction changes
                    if (event == 'a:38'):
                        window['sa_instruction'].update('Shoot the ball from any spot within the focus of the system. The LED will turn red if the system can not detect you.')

                    # frame is 480 x 640
                    _, frame = cap.read()

                    red_light()
                    # 1. Find motionless person in frames
                    if not ready_for_shot:
                        if height_calibrated and not waited_for_person_to_move:
                            print('Move to the location you want to shoot the ball...')
                            for i in range(wait_secs):
#                                 print("Before")
#                                 print("After")
                                print(str(wait_secs - i), end=', ')
                                sleep(1)
                            print()
                            waited_for_person_to_move = True

                        person = find_motionless_person(p_frames, frame)

                        if person is not None:
                            # 2. Upon finding motionless person first time, set focal length
                            if not height_calibrated:
                                focal_length = get_focal_length(person[h_ind], dist_5ft_to_basket, height_inches)

                                height_calibrated = True
                                p_frames = []
                            # 3. Second time, set distance and move on to seeing if ball is ready to be shot
                            elif height_calibrated:
                                distance_inches = get_person_distance(focal_length, height_inches, person[h_ind])

                                ready_for_shot = True

                    elif ready_for_shot:
                        # 4. See if person is holding ball up in a position to shoot
                        
                        ball_ready, held_ball = check_holding_ball(frame, person)

                        if ball_ready:
                            # 5. Check sonar to see if the shot was made
                            shot_made = listen_for_shot('shootaround')
                            if shot_made == True:
                                makes += 1
                            else:
                                misses += 1
                            # 6. Reset values and start to look for motionless person again
                            waited_for_person_to_move = False
                            ready_for_shot = False
                            person_holding_ball = False
                            distance = None
                            held_ball = None
                            p_frames = []
                            window['sa_instruction'].update('System is in calibration mode. Move to the location you want to shoot the ball...')
                    imgbytes = resize_frame(frame, 110)
                    window['image'].update(data=imgbytes)

                # made shots, shots attempted, three point makes , three point attempts
                analysis_update(makes, makes + misses, three_makes, three_makes + three_misses)

            #cancel and go back to menu page
            if event == 'Cancel':
                window['shootaround'].update(visible=False)
                window['camera'].update(visible=False)
                window['menu'].update(visible=True)
                mode = 'menu'
            # after youre done shooting, camera mode is off
            if event == 'Finished':
                window['camera'].update(visible=False)
                window['shotchart'].update(visible=True)
                court(axes)
                fig_canvas_agg = draw_figure(window['Canvas'].TKCanvas, fig)
            # click ok to close shot chart and return to menu
            if event == 'OK4':
                axes.clear()
                delete_figure_agg(fig_canvas_agg)
                window['shotchart'].update(visible=False)
                window['menu'].update(visible=True)
                mode = 'menu'

        elif mode == 'multi_player':
            if event == 'Cancel3':
                window['camera'].update(visible=False)
                window['multi_player'].update(visible=False)
                window['menu'].update(visible=True)
                mode = 'menu'
           # if event == 'Finished6':

            feet = values[4]
            inches = values[5]
            feet2 = values[6]
            inches2 = values[7]

            if event == 'OK2' and feet != '' and inches != '' and feet2 != '' and inches2 != '':
                window['multi_player'].update(visible=False)
                window['multiplayer_scoreboard'].update(visible=True)

                sonic = 0
                cam = 0
                mp1_makes = 0
                mp1_misses = 0
                mp2_makes = 0
                mp2_misses = 0

                num_players = 2
                players = []
                for i in range(num_players):
                    player = {
                        'id': i + 1,
                        # TODO: get this to change based on input
                        # 'height_inches': (12 * feet + inches) if i == 0 else (12 * feet2 + inches2),
                        'height_inches': 60,
                        'received_calibration_message': False,
                        'focal_length': None,
                        'waited_for_person_to_move': False,
                        'p_frames': [],
                        'person': None, # an instance of person object that indicates where they will shoot from
                        'distance_inches': 0,
                        'ready_for_shot': False,
                        'required_distance': 0,
                        'misses': 0,
                        # 'taking_turn': True
                    }
                    players.append(player)

                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    print('capture failed to open')

                player_idx = 0
                while event != 'Finished5' and not game_over(players):
                    # camera code
                    event, values = window.read(timeout=20)
                    # print(event)
                    # when calibration is done, instruction changes
                    if event == 'a:38':
                        distance = distance_selector()
                        window['multi_instruction'].update(shot_select(distance))

                    # while system is in calibration mode -> yellow light
                    # if player is not detected, LED -> red light
                    red_light()
                    
                    _, frame = cap.read()

                    player = players[player_idx % 2]
                    if not player['received_calibration_message']:
                        # TODO: put in GUI
                        
                        print('stand ~10 feet away from the camera for height calibration')
                        for i in range(wait_secs):
                            print(str(wait_secs - i), end=', ')
                            sleep(1)
                        print()

                        player['received_calibration_message'] = True

                    elif not player['ready_for_shot']:
                        player['person'] = find_motionless_person(player['p_frames'], frame)

                        if player['person'] is not None:
                            if not player['focal_length']:
                                player['focal_length'] = get_focal_length(player['person'][h_ind], dist_5ft_to_basket, player['height_inches'])
                                player['p_frames'] = []

                            if player['focal_length'] is not None and not player['waited_for_person_to_move']:
                                print('Move to the location you want to shoot the ball from...')

                                if player['required_distance'] > 0:
                                    print('You must make it from ' + str(player['required_distance']) + ' away...')

                                for i in range(wait_secs):
                                    print(str(wait_secs - i), end=', ')
                                    sleep(1)
                                print()
                                player['waited_for_person_to_move'] = True

                            elif player['waited_for_person_to_move']:
                                player['distance_inches'] = get_person_distance(player['focal_length'], player['height_inches'], player['person'][h_ind])

                                player_in_range = (player['required_distance'] > 0 and .95 * player['required_distance'] <= player['distance_inches'] <= 1.05 * player['required_distance']) or player['required_distance'] <= 0
                                if player_in_range:
                                    player['ready_for_shot'] = True
                                    print('Hold the ball at about eye level...')
                                else:
                                    print('please stand ' + str(player['required_distance']) + ' away...')
                                    sleep(1)

                    elif player['ready_for_shot']:
                        ball_ready, held_ball = check_holding_ball(frame, player['person'])
                        
                        if ball_ready:
                            shot_made = listen_for_shot('multi')
#                             shot_made = True if player_idx % 2 != 0 else False
                            print('Shot made!' if shot_made else 'Shot missed!')

                            player_idx += 1
                            next_player = players[player_idx % 2]

                            if shot_made:
                                next_player['required_distance'] = player['distance_inches'] if player['required_distance'] <= 0 else 0
                            else:
                                if player['required_distance'] > 0:
                                    player['misses'] += 1

                                    # update GUI with letters player has
                                    letter_id, letter = get_letter(player)
                                    window[letter_id].update(letter)

                                    print('Player ' + str(player['id']) + ' has ' + str(player['misses']) + ' misses')

                            player['distance_inches'] = 0
                            player['required_distance'] = 0
                            player['person'] = None
                            player['p_frames'] = []
                            player['ready_for_shot'] = False
                            player['waited_for_person_to_move'] = False
                            # player['taking_turn'] = False

                            # next_player['taking_turn'] = True
                    
#                     print('about to display frame')
                    imgbytes = resize_frame(frame, 130)
                    window['mp_image'].update(data=imgbytes)




                    # update shot chart with makes/misses when
                    # also need to account fo three point makes/misses

        elif mode == 'single_player':
            #opening page, enter height and click ok, else cancel and return to main
            if event == 'OK0':
                feet = values[2]
                inches = values[3]
                window['single_player'].update(visible=False)
                window['singleplayer_scoreboard'].update(visible=True)

                sonic = 0
                cam = 0
                makes = 0
                misses = 0
                three_makes = 0
                three_misses = 0
                x = 0
                y = 0

                cap = cv2.VideoCapture(0)
                if cap.isOpened():
                    person_cascade = cv2.CascadeClassifier('./haarcascade_fullbody.xml')
                    ball_cascade = cv2.CascadeClassifier('./ball_cascade.xml')
                while event != 'Finished5':
                    # camera code
                    event, values = window.read(timeout=20)
                    # print(event)
                    # when calibration is done, instruction changes
                    if event == 'a:38':
                        distance = distance_selector()
                        window['single_instruction'].update(shot_select(distance))
                    # update letter when there is a miss
                    if event == 'b:56':
                        misses += 1
                        if misses == 1:
                            window['h_s'].update('H')
                        if misses == 2:
                            window['o_s'].update('O')
                        if misses == 3:
                            window['r_s'].update('R')
                        if misses == 4:
                            window['s_s'].update('S')
                        if misses == 5:
                            window['e_s'].update('E')

                    ret, frame = cap.read()

                    # while system is in calibration mode -> yellow light
                    # if player is not detected, LED -> red light

                    persons = person_cascade.detectMultiScale(frame, 1.1, 1)
                    balls = ball_cascade.detectMultiScale(frame, 1.3, 3, 8)
                    # To draw a rectangle in each persons
                    # cv2.imshow('Ball detection', frame)
                    for (x,y,w,h) in balls:
                       cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                       font = cv2.FONT_HERSHEY_DUPLEX
                       cv2.putText(frame, 'Ball', (x + 6, y - 6), font, 0.5, (0, 0, 255), 1)
                    for (x,y,w,h) in persons:
                      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                      font = cv2.FONT_HERSHEY_DUPLEX
                      cv2.putText(frame, 'Person', (x + 6, y - 6), font, 0.5, (0, 255, 0), 1)
                    #Display frames in a window
                    # cv2.imshow('Ball detection', frame)
                    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
                    window['sp_image'].update(data=imgbytes)
                    # update shot chart with makes/misses when
                    # also need to account fo three point makes/misses
    #                 if (cam == 1 and sonic == 1):
    #                     chart_update(x, y, 1)
    #                     makes += 1
    #                 else:
    #                     chart_update(x, y, 1)
    #                     misses += 1

                    # while system is in calibration mode -> yellow light
                    # yellow_light()

                    # if player is not detected, LED -> red light

                    # sonic sensor code
        #             dist = distance()
        #             if confirm_shot(dist) == True:
        #                 sonic = 1

                # made shots, shots attempted, three point makes , three point attempts
                analysis_update(23, 45, 18, 30)

            #cancel and go back to menu page
            if event == 'Cancel1':
                window['camera'].update(visible=False)
                window['single_player'].update(visible=False)
                window['menu'].update(visible=True)
                mode = 'menu'
            # after game is over, camera mode is off
            if event == 'Finished5':
                window['singleplayer_scoreboard'].update(visible=False)
                window['shotchart'].update(visible=True)
                court(axes)
                fig_canvas_agg = draw_figure(window['Canvas'].TKCanvas, fig)
            # click ok to close shot chart and return to menu
            if event == 'OK4':
                axes.clear()
                delete_figure_agg(fig_canvas_agg)
                window['shotchart'].update(visible=False)
                window['menu'].update(visible=True)
                mode = 'menu'

    window.close()
