import PySimpleGUI as sg
import numpy as np
import imutils
from collections import deque
from time import sleep
from matplotlib.ticker import NullFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from shotchart import *
from shot_generator import *
from image_helpers import *
from layout import *
# from sonar_test import *
# from LED import *

frames_size = 10

# Create the Window
window = sg.Window('HORSE Simulator', layout, location=(100, 100), return_keyboard_events=True)
# Event Loop to process "events" and get the "values" of the inputs
mode = 'menu'

# used in height function
feet = 0
inches = 0
feet2 = 0
inches2 = 0

# update shooting statistics
def analysis_update(shotsm, shotsa, tps, tpa):
    string_shotsm = str(shotsm)
    string_shotsa = str(shotsa)
    string_tps = str(tps)
    string_fgp = str(round((shotsm / shotsa) * 100, 1)) + ' %'
    string_threepp = str(round((tps / tpa) * 100, 1)) + ' %'
    string_twopp = str(round(((shotsm - tps) / (shotsa - tpa)) * 100, 1)) + ' %'
    window['shotsm'].update(string_shotsm)
    window['shotsa'].update(string_shotsa)
    window['tps'].update(string_tps)
    window['fgp'].update(string_fgp)
    window['threepp'].update(string_threepp)
    window['twopp'].update(string_twopp)

# main loop where GUI is opened
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    print(event)

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

            sonic = 0
            cam = 0
            makes = 0
            misses = 0
            three_makes = 0
            three_misses = 0
            x = 0
            y = 0

            cap = cv2.VideoCapture(0)
            # sleep(2)
            if cap.isOpened():
                # person_cascade = cv2.CascadeClassifier('./haarcascade_fullbody.xml')
                # ball_cascade = cv2.CascadeClassifier('./ball_cascade.xml')
                print('start')

            persons_frames = []
            height_calibrated = False

            # num_frames = 0
            while event != 'Finished':
                # num_frames += 1
                # print(num_frames)

                # camera code
                event, values = window.read(timeout=20)

                # when calibration is done, instruction changes
                if (event == 'a:38'):
                    window['sa_instruction'].update('Shoot the ball from any spot within the focus of the system. The LED will turn red if the system can not detect you.')

                ret, frame = cap.read()

                # while system is in calibration mode -> yellow light
                # if player is not detected, LED -> red light

                persons = find_persons(frame)
                draw_persons(frame, persons)

                if len(persons_frames) < frames_size:
                    persons_frames.append(persons)
                else:
                    del persons_frames[0]
                    persons_frames.append(persons)

                # height_calibrated, height_pixels = calibrate_height(persons_frames)

                ball = find_ball(frame)
                draw_ball(frame, ball)

                imgbytes = resize_frame(frame, 130)
                window['image'].update(data=imgbytes)

                # update shot chart with makes/misses
                # also need to account fo three point makes/misses
#                 if (cam == 1 and sonic == 1):
#                     chart_update(x, y, 1)
#                     makes += 1
#                 else:
#                     chart_update(x, y, 1)
#                     misses += 1
#
    #        sonic sensor code
    #             dist = distance()
    #             if confirm_shot(dist) == True:
    #                 sonic = 1

            # made shots, shots attempted, three point makes , three point attempts
            # analysis_update(23, 45, 18, 30)

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
            window['sa_instruction'].update('Please stand at the free throw line for system calibration.'
                                                                                    'The LED will change from yellow to green when calibration is finished.'
                                                                                    ' When the LED is green, you can shoot the ball repeatedly. When you are'
                                                                                    ' finished, click on the finished button.')
            court(axes)
            fig_canvas_agg = draw_figure(window['Canvas'].TKCanvas, fig)
        # click ok to close shot chart and return to menu
        if event == 'OK4':
            axes.clear()
            delete_figure_agg(fig_canvas_agg)
            window['shotchart'].update(visible=False)
            window['menu'].update(visible=True)
            mode = 'menu'

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
                print(event)
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

    elif mode == 'multi_player':
        if event == 'Cancel3':
            window['camera'].update(visible=False)
            window['multi_player'].update(visible=False)
            window['menu'].update(visible=True)
            mode = 'menu'
       # if event == 'Finished6':

        if event == 'OK2':
            feet = values[4]
            inches = values[5]
            feet2 = values[6]
            inches2 = values[7]
            window['multi_player'].update(visible=False)
            window['multiplayer_scoreboard'].update(visible=True)

            sonic = 0
            cam = 0
            mp1_makes = 0
            mp1_misses = 0
            mp2_makes = 0
            mp2_misses = 0

            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                person_cascade = cv2.CascadeClassifier('./haarcascade_fullbody.xml')
                ball_cascade = cv2.CascadeClassifier('./ball_cascade.xml')
            while event != 'Finished5':
                # camera code
                event, values = window.read(timeout=20)
                print(event)
                # when calibration is done, instruction changes
                if event == 'a:38':
                    distance = distance_selector()
                    window['multi_instruction'].update(shot_select(distance))
                # update letter when there is a miss
                if event == 'b:56':
                    mp1_misses += 1
                    mp2_misses += 1
                    if mp1_misses == 1:
                        window['h1'].update('H')
                    if mp1_misses == 2:
                        window['o1'].update('O')
                    if mp1_misses == 3:
                        window['r1'].update('R')
                    if mp1_misses == 4:
                        window['s1'].update('S')
                    if mp1_misses == 5:
                        window['e1'].update('E')
                    if mp2_misses == 1:
                        window['h2'].update('H')
                    if mp2_misses == 2:
                        window['o2'].update('O')
                    if mp2_misses == 3:
                        window['r2'].update('R')
                    if mp2_misses == 4:
                        window['s2'].update('S')
                    if mp2_misses == 5:
                        window['e2'].update('E')

                ret, frame = cap.read()

                # while system is in calibration mode -> yellow light
                # if player is not detected, LED -> red light

                persons = person_cascade.detectMultiScale(frame, 1.1, 1)
                balls = ball_cascade.detectMultiScale(frame, 1.3, 3, 8)
                # To draw a rectangle in each persons
                cv2.imshow('Ball detection', frame)
                for (x,y,w,h) in balls:
                   cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                   font = cv2.FONT_HERSHEY_DUPLEX
                   cv2.putText(frame, 'Ball', (x + 6, y - 6), font, 0.5, (0, 0, 255), 1)
                for (x,y,w,h) in persons:
                  cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                  font = cv2.FONT_HERSHEY_DUPLEX
                  cv2.putText(frame, 'Person', (x + 6, y - 6), font, 0.5, (0, 255, 0), 1)
                #Display frames in a window
                cv2.imshow('Ball detection', frame)
                imgbytes = cv2.imencode('.png', frame)[1].tobytes()
                window['mp_image'].update(data=imgbytes)
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


window.close()
