import PySimpleGUI as sg
import time

sg.theme('DarkAmber') # Add a touch of color
# All the stuff inside your window.
height_input_layout = [
    [sg.Text('Horse Simulator')],
    [sg.Text('Please input your height in inches')],
    [sg.InputText(), sg.Button('OK')]
]

detecting = True
height_detection = [
    [sg.Text('Horse Simulator')],
    [sg.Text('Please stand on the free throw line until the LED turns green')],
    [sg.Text('Detecting...')] if detecting else []
]

layout = [[
    sg.Column(height_input_layout, key='height_input'),
    sg.Column(height_detection, key='height_detection', visible=False)
]]

# Create the Window
window = sg.Window('Horse Simulator', layout)
# Event Loop to process "events" and get the "values" of the inputs
start_time = None
mode = 'height_input'
while True:
    # if mode == 'height_input':
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break

    if mode == 'height_input':
        if event == 'OK':
            height_inches = float(values[0])

            window['height_input'].update(visible=False)
            window['height_detection'].update(visible=True)
            mode = 'height_detection'
            time.sleep(1)

    elif mode == 'height_detection':
        if detecting and start_time:
            # print(str(time.perf_counter()))
            # print(str(start_time))
            if time.perf_counter() - start_time >= 3:
                break
        elif detecting:
            start_time = time.perf_counter()
        else:
            start_time = None

window.close()
