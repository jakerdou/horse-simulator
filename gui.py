import PySimpleGUI as sg
import cv2
from time import sleep
from matplotlib.ticker import NullFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shotchart import *
from shot_generator import *
#from sonar_test import *
#from LED import *

sg.theme('DarkAmber')

#Layouts for various pages
menu_layout = [
    [sg.Text('Horse Simulator', size=(45, 1), justification='center', font='Helvetica 20')],
    [sg.Text('Please select a mode', justification='center', font='Helvetica 12')],
    [sg.Button('Shootaround', size=(20, 4), font='Helvetica 14'), sg.Button('Single Player', size=(20, 4), font='Helvetica 14'), sg.Button('Multiplayer', size=(20, 4), font='Helvetica 14')]
]

shootaround_layout = [
    [sg.Text('Horse Simulator', size=(40, 1), justification='center', font='Helvetica 20')],
    [sg.Text('Shootaround Mode: Practice your shooting and get a statistical analysis of your shooting.', size=(60, 2), font='Helvetica 14')],
    [sg.Text('Please enter your height.', font='Helvetica 12')],
    [sg.Text('Feet: ', font='Helvetica 12'), sg.InputText()], [sg.Text('Inches: ', font='Helvetica 12'), sg.InputText()],
    [sg.Button('OK')],
    [sg.Button('Cancel')]
]

single_player_layout = [
    [sg.Text('HORSE: Single Player Mode', size=(40, 1), justification='center', font='Helvetica 20')],
    [sg.Text('Single Player Mode: Play a game of HORSE and try to beat your highest score.', size=(60, 2), font='Helvetica 14')],
    [sg.Text('Please enter your height.', font='Helvetica 12')],
    [sg.Text('Feet: ', font='Helvetica 12'), sg.InputText()], [sg.Text('Inches: ', font='Helvetica 12'), sg.InputText()],
    [sg.Button('OK')],
    [sg.Button('Cancel')]
]

multiplayer_layout = [
    [sg.Text('HORSE: Multiplayer Mode', size=(40, 1), justification='center', font='Helvetica 20')],
    [sg.Text('Multiplayer Mode: Play a game of HORSE with another player and try to beat the opposing player.', size=(60, 2), font='Helvetica 14')],
    [sg.Text('Player 1, please enter your height.', font='Helvetica 12')],
    [sg.Text('Feet: ', font='Helvetica 12'), sg.InputText()], [sg.Text('Inches: ', font='Helvetica 12'), sg.InputText()],
    [sg.Text('Player 2, please enter your height.', font='Helvetica 12')],
    [sg.Text('Feet: ', font='Helvetica 12'), sg.InputText()], [sg.Text('Inches: ', font='Helvetica 12'), sg.InputText()],
    [sg.Button('OK')],
    [sg.Button('Cancel')]
]

col = sg.Column([[sg.Frame('Instructions', [[sg.Text(), sg.Column([[sg.Text('Please stand at the free throw line for system calibration.'
                                                                                    'The LED will change from yellow to green when calibration is finished.'
                                                                                    ' When the LED is green, you can shoot the ball repeatedly. When you are'
                                                                                    ' finished, click on the finished button.', size=(60, 4), font='Helvetica 14', key='sa_instruction')]])]], font='Helvetica 15')]], pad=(0,0))
camera_layout = [
    [sg.Text('Court View', size=(40, 1), justification='center', font='Helvetica 20')],
    [sg.Image(filename='', key='image')], [sg.HorizontalSeparator()] , [col],
    [sg.Button('Finished', size=(10, 1))]
]

col1 = sg.Column([[sg.Frame('Court View', [[sg.Image(filename='', key='sp_image')]], font='Helvetica 15')]], pad=(0,0))
col2 = sg.Column([[sg.Frame('Player Score', [[sg.Text(), sg.Column([[sg.Text('Highest Score:', font='Helvetica 12', justification='center')], [sg.Text('18', justification='center', font='Helvetica 20')],
                                                                    [sg.Text('Current Score:', font='Helvetica 12', justification='center')], [sg.Text('0', font='Helvetica 20', justification='center')],
                                                                    [sg.Text('Letters:', font='Helvetica 12', justification='center')], [sg.Text('', justification='center', font='Helvetica 30', key='h_s')],
                                                                    [sg.Text('', justification='center', font='Helvetica 30', key='o_s')], [sg.Text('', justification='center', font='Helvetica 30', key='r_s')],
                                                                    [sg.Text('', justification='center', font='Helvetica 30', key='s_s')], [sg.Text('', justification='center', font='Helvetica 30', key='e_s')]], size=(120, 480))]], font='Helvetica 15')]], pad=(0,0))
col3 = sg.Column([[sg.Frame('Shot Instruction', [[sg.Text(), sg.Column([[sg.Text('Please stand at the free throw line for system calibration.'
                                                                                    'The LED will change from yellow to green when calibration is finished.'
                                                                                    ' When the LED is green, you can shoot the ball repeatedly. When you are'
                                                                                    ' finished, click on the finished button.', size=(70, 3), key='single_instruction', font='Helvetica 15')]])]], font='Helvetica 15')]], pad=(0,0))
singleplayer_scoreboard = [
    [sg.Text('Scoreboard', size=(25, 1), justification='center', font='Helvetica 40')],
    [col1, col2], [col3],
    [sg.Button('Finished', size=(10, 1))]
]

col4 = sg.Column([[sg.Frame('Court View', [[sg.Image(filename='', key='mp_image')]], font='Helvetica 15')]], pad=(0,0))
col5 = sg.Column([[sg.Frame('Player 1 Score', [[sg.Text(), sg.Column([[sg.Text('', justification='center', font='Helvetica 55', key='h1')],
                                                                    [sg.Text('', justification='center', font='Helvetica 55', key='o1')], [sg.Text('', justification='center', font='Helvetica 55', key='r1')],
                                                                    [sg.Text('', justification='center', font='Helvetica 55', key='s1')], [sg.Text('', justification='center', font='Helvetica 55', key='e1')]], size=(100, 480))]], font='Helvetica 15')]], pad=(0,0))
col6 = sg.Column([[sg.Frame('Player 2 Score', [[sg.Text(), sg.Column([[sg.Text('', justification='center', font='Helvetica 55', key='h2')],
                                                                    [sg.Text('', justification='center', font='Helvetica 55', key='o2')], [sg.Text('', justification='center', font='Helvetica 55', key='r2')],
                                                                    [sg.Text('', justification='center', font='Helvetica 55', key='s2')], [sg.Text('', justification='center', font='Helvetica 55', key='e2')]], size=(100, 480))]], font='Helvetica 15')]], pad=(0,0))
col7 = sg.Column([[sg.Frame('Shot Instruction', [[sg.Text(), sg.Column([[sg.Text('Please stand at the free throw line for system calibration.'
                                                                                    'The LED will change from yellow to green when calibration is finished.'
                                                                                    ' When the LED is green, you can shoot the ball repeatedly. When you are'
                                                                                    ' finished, click on the finished button.', size=(84, 3), key='multi_instruction', font='Helvetica 15')]])]], font='Helvetica 15')]], pad=(0,0))
multiplayer_scoreboard = [
    [sg.Text('Scoreboard', size=(30, 1), justification='center', font='Helvetica 40')],
    [col4, col5, col6], [col7],
    [sg.Button('Finished')]
]

shotchart_layout = [
    [sg.Text('Shooting Analysis', size=(30, 1), justification='center', font='Helvetica 40')],
    [sg.Canvas(key='Canvas'), sg.VerticalSeparator(), sg.Frame('Statistics', [[sg.Text(), sg.Column([[sg.Text('Shots Made', size=(45, 1), justification='center', font='Helvetica 12')],
                                                                                                     [sg.Text('0', size=(45, 1), justification='center', font='Helvetica 12', key='shotsm')],
                                                                                                     [sg.Text('Shots Attempted', size=(45, 1), justification='center', font='Helvetica 12')],
                                                                                                     [sg.Text('0', size=(45, 1), justification='center', font='Helvetica 12', key='shotsa')],
                                                                                                     [sg.Text('Three Point Shots Made', size=(45, 1), justification='center', font='Helvetica 12')],
                                                                                                     [sg.Text('0', size=(45, 1), justification='center', font='Helvetica 12', key='tps')],
                                                                                                     [sg.Text('Field Goal Percentage', size=(45, 1), justification='center', font='Helvetica 12')],
                                                                                                     [sg.Text('0 %', size=(45, 1), justification='center', font='Helvetica 12', key='fgp')],
                                                                                                     [sg.Text('Three Point Percentage', size=(45, 1), justification='center',font='Helvetica 12')],
                                                                                                     [sg.Text('0 %', size=(45, 1), justification='center', font='Helvetica 12', key='threepp')],
                                                                                                     [sg.Text('Two Point Percentage', size=(45, 1), justification='center',font='Helvetica 12')],
                                                                                                     [sg.Text('0 %', size=(45, 1), justification='center', font='Helvetica 12', key='twopp')]])]], font='Helvetica 15')],
    
    [sg.Button('OK')]
]

layout = [[
    sg.Column(menu_layout, key='menu'),
    sg.Column(shootaround_layout, key='shootaround', visible=False),
    sg.Column(single_player_layout, key='single_player', visible=False),
    sg.Column(multiplayer_layout, key='multi_player', visible=False),
    sg.Column(camera_layout, key='camera', visible=False),
    sg.Column(shotchart_layout, key='shotchart', visible=False),
    sg.Column(singleplayer_scoreboard, key='singleplayer_scoreboard', visible=False),
    sg.Column(multiplayer_scoreboard, key='multiplayer_scoreboard', visible=False)
]]

# Create the Window
window = sg.Window('HORSE Simulator', layout, location=(100, 100), return_keyboard_events=True)
# Event Loop to process "events" and get the "values" of the inputs
mode = 'menu'

# used in height function
feet = 0
inches = 0
feet2 = 0
inches2 = 0

# shooting analysis chart
fig = plt.figure(figsize=(5, 4.5))
axes = fig.add_axes([0, 0, 1, 1])
# draw/delete shooting chart
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg
def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
#update the chart with misses and makes
def chart_update(x, y, m):
    if m == 1:
        make(axes, x, y)
    else:
        miss(axes, x, y)
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
        if event == 'OK':
            feet = values[0]
            inches = values[1]
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
            if cap.isOpened():
                pedestrian_cascade = cv2.CascadeClassifier('./haarcascade_fullbody.xml')
                ball_cascade = cv2.CascadeClassifier('./ball_cascade.xml')
            while event != 'Finished':
                # camera code
                event, values = window.read(timeout=20)
                
                # when calibration is done, instruction changes 
                if (event == 'a:38'):
                    window['sa_instruction'].update('Shoot the ball from any spot within the focus of the system. The LED will turn red if the system can not detect you.')
                ret, frame = cap.read()
                
                # while system is in calibration mode -> yellow light
                # if player is not detected, LED -> red light
            
                pedestrians = pedestrian_cascade.detectMultiScale(frame, 1.1, 1)
                balls = ball_cascade.detectMultiScale(frame, 1.3, 3, 8)
                # To draw a rectangle in each pedestrians
                cv2.imshow('Ball detection', frame)
                for (x,y,w,h) in balls:
                   cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                   font = cv2.FONT_HERSHEY_DUPLEX
                   cv2.putText(frame, 'Ball', (x + 6, y - 6), font, 0.5, (0, 0, 255), 1)
                for (x,y,w,h) in pedestrians:
                  cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                  font = cv2.FONT_HERSHEY_DUPLEX
                  cv2.putText(frame, 'Person', (x + 6, y - 6), font, 0.5, (0, 255, 0), 1)
                #Display frames in a window
                cv2.imshow('Ball detection', frame)
                imgbytes = cv2.imencode('.png', frame)[1].tobytes() 
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
            analysis_update(23, 45, 18, 30)
            
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
                pedestrian_cascade = cv2.CascadeClassifier('./haarcascade_fullbody.xml')
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
                
                pedestrians = pedestrian_cascade.detectMultiScale(frame, 1.1, 1)
                balls = ball_cascade.detectMultiScale(frame, 1.3, 3, 8)
                # To draw a rectangle in each pedestrians
                cv2.imshow('Ball detection', frame)
                for (x,y,w,h) in balls:
                   cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                   font = cv2.FONT_HERSHEY_DUPLEX
                   cv2.putText(frame, 'Ball', (x + 6, y - 6), font, 0.5, (0, 0, 255), 1)
                for (x,y,w,h) in pedestrians:
                  cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                  font = cv2.FONT_HERSHEY_DUPLEX
                  cv2.putText(frame, 'Person', (x + 6, y - 6), font, 0.5, (0, 255, 0), 1)
                #Display frames in a window
                cv2.imshow('Ball detection', frame)
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
                pedestrian_cascade = cv2.CascadeClassifier('./haarcascade_fullbody.xml')
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
                
                pedestrians = pedestrian_cascade.detectMultiScale(frame, 1.1, 1)
                balls = ball_cascade.detectMultiScale(frame, 1.3, 3, 8)
                # To draw a rectangle in each pedestrians
                cv2.imshow('Ball detection', frame)
                for (x,y,w,h) in balls:
                   cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                   font = cv2.FONT_HERSHEY_DUPLEX
                   cv2.putText(frame, 'Ball', (x + 6, y - 6), font, 0.5, (0, 0, 255), 1)
                for (x,y,w,h) in pedestrians:
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
