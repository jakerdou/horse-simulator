import PySimpleGUI as sg
import cv2
from matplotlib.ticker import NullFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shotchart import *
from shot_generator import *

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
menu_layout = [
    [sg.Text('Horse Simulator', size=(45, 1), justification='center', font='Helvetica 20')],
    [sg.Text('Please select a mode', justification='center', font='Helvetica 12')],
    [sg.Button('Shootaround', size=(20, 4), font='Helvetica 14'), sg.Button('Single Player', size=(20, 4), font='Helvetica 14'), sg.Button('Multiplayer', size=(20, 4), font='Helvetica 14')]
]

shootaround_layout = [
    [sg.Text('Horse Simulator', size=(40, 1), justification='center', font='Helvetica 20')],
    [sg.Text('This is the Shootaround mode')],
    [sg.Text('Please enter your height.')],
    [sg.Text('Feet: '), sg.InputText()], [sg.Text('Inches: '), sg.InputText()],
    [sg.Button('OK')],
    [sg.Button('Cancel')]
]

single_player_layout = [
    [sg.Text('HORSE: Single Player Mode', size=(40, 1), justification='center', font='Helvetica 20')],
    [sg.Text('This is the Single Player mode.')],
    [sg.Text('Please enter your height.')],
    [sg.Text('Feet: '), sg.InputText()], [sg.Text('Inches: '), sg.InputText()],
    [sg.Button('OK')],
    [sg.Button('Cancel')]
]

multiplayer_layout = [
    [sg.Text('HORSE: Multiplayer Mode', size=(40, 1), justification='center', font='Helvetica 20')],
    [sg.Text('This is the Multiplayer mode.')],
    [sg.Text('Player 1, please enter your height.')],
    [sg.Text('Feet: '), sg.InputText()], [sg.Text('Inches: '), sg.InputText()],
    [sg.Text('Player 2, please enter your height.')],
    [sg.Text('Feet: '), sg.InputText()], [sg.Text('Inches: '), sg.InputText()],
    [sg.Button('OK')],
    [sg.Button('Cancel')]
]

camera_layout = [
    [sg.Text('Court View', size=(40, 1), justification='center', font='Helvetica 20')],
    [sg.Text('Shoot the ball')],
    [sg.Image(filename='', key='image')],
    [sg.Button('Finished', size=(10, 1))]
]

distance = distance_selector()
col1 = sg.Column([[sg.Frame('Court View', [[sg.Image(filename='', key='sp_image')]], font='Helvetica 10')]], pad=(0,0))
col2 = sg.Column([[sg.Frame('Player Score', [[sg.Text(), sg.Column([[sg.Text('Highest Score', size=(40, 1), font='Helvetica 10')]])]], font='Helvetica 10')]], pad=(0,0))
col3 = sg.Column([[sg.Frame('Shot Instruction', [[sg.Text(), sg.Column([[sg.Text(shot_select(distance), size=(40, 1), font='Helvetica 10')]])]], font='Helvetica 10')]], pad=(0,0))
singleplayer_scoreboard = [
    [sg.Text('Scoreboard', size=(30, 1), justification='center', font='Helvetica 40')],
    [col1, col2], [col3],
    [sg.Button('Finished', size=(10, 1))]
]

col4 = sg.Column([[sg.Frame('Court View', [[sg.Image(filename='', key='mp_image')]], font='Helvetica 15')]], pad=(0,0))
col5 = sg.Column([[sg.Frame('Player 1 Score', [[sg.Text(), sg.Column([[sg.Text('Score', size=(40, 1), font='Helvetica 10')]])]], font='Helvetica 15')]], pad=(0,0))
col6 = sg.Column([[sg.Frame('Player 2 Score', [[sg.Text(), sg.Column([[sg.Text('Score', size=(40, 1), font='Helvetica 10')]])]], font='Helvetica 15')]], pad=(0,0))
multiplayer_scoreboard = [
    [sg.Text('Scoreboard', size=(30, 1), justification='center', font='Helvetica 40')],
    [col4], [col5, col6],
    [sg.Button('Finished')], [sg.Stretch()]
]

shotchart_layout = [
    [sg.Text('Shooting Analysis', size=(30, 1), justification='center', font='Helvetica 40')],
    [sg.Canvas(key='Canvas')],
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
window = sg.Window('HORSE Simulator', layout, location=(100, 100))
# Event Loop to process "events" and get the "values" of the inputs
mode = 'menu'

feet = 0
inches = 0
feet2 = 0
inches2 = 0

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    #figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

while True:
    event, values = window.read()
    print(event)
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break

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
            
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                pedestrian_cascade = cv2.CascadeClassifier('./haarcascade_fullbody.xml')
                ball_cascade = cv2.CascadeClassifier('./ball_cascade.xml')
            while event != 'Finished':
                event, values = window.read(timeout=20)
                ret, frame = cap.read()
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
        
        if event == 'Cancel':
            window['shootaround'].update(visible=False)
            window['camera'].update(visible=False)
            window['menu'].update(visible=True)
            mode = 'menu'
        # after youre done shooting, camera mode is off 
        if event == 'Finished':
            cv2.destroyAllWindows()
            window['camera'].update(visible=False)
            window['shotchart'].update(visible=True)
            fig = plt.figure(figsize=(5, 4.5))
            axes = fig.add_axes([0, 0, 1, 1])
            court(axes)
            fig_canvas_agg = draw_figure(window['Canvas'].TKCanvas, fig)
        #click ok to close shot chart
        if event == 'OK4':
            window['shotchart'].update(visible=False)
            window['menu'].update(visible=True)
            mode = 'menu'
    elif mode == 'single_player':
        if event == 'Cancel1':
            window['camera'].update(visible=False)
            window['single_player'].update(visible=False)
            window['menu'].update(visible=True)
            mode = 'menu'
        if event == 'OK0':
            feet = values[2]
            inches = values[3]
            window['single_player'].update(visible=False)
            window['singleplayer_scoreboard'].update(visible=True)
            
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                pedestrian_cascade = cv2.CascadeClassifier('./haarcascade_fullbody.xml')
                ball_cascade = cv2.CascadeClassifier('./ball_cascade.xml')
            while event != 'Finished5':
                event, values = window.read(timeout=20)
                ret, frame = cap.read()
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
        
        if event == 'Finished5':
            cv2.destroyAllWindows()
            window['singleplayer_scoreboard'].update(visible=False)
            window['shotchart'].update(visible=True)
            fig = plt.figure(figsize=(5, 4.5))
            axes = fig.add_axes([0, 0, 1, 1])
            court(axes)
            fig_canvas_agg = draw_figure(window['Canvas'].TKCanvas, fig)
        if event == 'OK4':
            window['shotchart'].update(visible=False)
            window['menu'].update(visible=True)
            mode = 'menu'
            
    elif mode == 'multi_player':
        if event == 'Cancel3':
            window['camera'].update(visible=False)
            window['multi_player'].update(visible=False)
            window['menu'].update(visible=True)
            mode = 'menu'
        if event == 'OK2':
            feet = values[4]
            inches = values[5]
            feet2 = values[6]
            inches2 = values[7]
            window['multi_player'].update(visible=False)
            window['multiplayer_scoreboard'].update(visible=True)
            
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                pedestrian_cascade = cv2.CascadeClassifier('./haarcascade_fullbody.xml')
                ball_cascade = cv2.CascadeClassifier('./ball_cascade.xml')
            while event != 'Finished':
                event, values = window.read(timeout=20)
                ret, frame = cap.read()
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

window.close()
