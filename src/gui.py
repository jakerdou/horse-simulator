import PySimpleGUI as sg

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
    [sg.Text('Please enter your height. After entering your height, stand 10 feet from the basket.', font='Helvetica 10')],
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

col = sg.Column([[sg.Frame('Instructions', [[sg.Text(), sg.Column([[sg.Text('System is in calibration mode. Move to the location you want to shoot the ball...', size=(60, 4), font='Helvetica 14', key='sa_instruction')]])]], font='Helvetica 15')]], pad=(0,0))
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
col3 = sg.Column([[sg.Frame('Shot Instruction', [[sg.Text(), sg.Column([[sg.Text('System is in calibration mode. Move to the location you want to shoot the ball...', size=(70, 3), key='single_instruction', font='Helvetica 15')]])]], font='Helvetica 15')]], pad=(0,0))
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
col7 = sg.Column([[sg.Frame('Shot Instruction', [[sg.Text(), sg.Column([[sg.Text('System is in calibration mode. Move to the location you want to shoot the ball...', size=(84, 3), key='multi_instruction', font='Helvetica 15')]])]], font='Helvetica 15')]], pad=(0,0))
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
window = sg.Window('HORSE Simulator', layout, location=(0, 0), return_keyboard_events=True)
