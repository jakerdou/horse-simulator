import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
menu_layout = [
    [sg.Text('Horse Simulator')],
    [sg.Text('Please select a mode')],
    [sg.Button('Shootaround'), sg.Button('Single Player'), sg.Button('Multiplayer')]
]

shootaround_layout = [
    [sg.Text('Horse Simulator')],
    [sg.Text('This is the Shootaround mode')],
    [sg.Button('Cancel')]
]

single_player_layout = [
    [sg.Text('Horse Simulator')],
    [sg.Text('This is the Single Player mode')],
    [sg.Button('Cancel')]
]

multiplayer_layout = [
    [sg.Text('Horse Simulator')],
    [sg.Text('This is the Multiplayer mode')],
    [sg.Button('Cancel')]
]

layout = [[
    sg.Column(menu_layout, key='menu'),
    sg.Column(shootaround_layout, key='shootaround', visible=False),
    sg.Column(single_player_layout, key='single_player', visible=False),
    sg.Column(multiplayer_layout, key='multiplayer', visible=False)
]]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
mode = 'menu'
while True:
    event, values = window.read()
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
            window['multiplayer'].update(visible=True)
            mode = 'multiplayer'

    elif mode == 'shootaround':
        if event == 'Cancel':
            window['shootaround'].update(visible=False)
            window['menu'].update(visible=True)
            mode = 'menu'
    elif mode == 'single_player':
        if event == 'Cancel0':
            window['single_player'].update(visible=False)
            window['menu'].update(visible=True)
            mode = 'menu'
    elif mode == 'multiplayer':
        if event == 'Cancel1':
            window['multiplayer'].update(visible=False)
            window['menu'].update(visible=True)
            mode = 'menu'

window.close()
