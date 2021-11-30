import PySimpleGUI as sg
days = ['Monday', 'Tuesday', 'Wednesday']
row = [sg.Column([[sg.Text(days[0])], [sg.Checkbox('Time 1')], [sg.Checkbox('Time 2')]])]
for day in days[1:]:
    row += [sg.VerticalSeparator(pad=(0, 0)),
            sg.Column([[sg.Text(day)], [sg.Checkbox('Time 1')], [sg.Checkbox('Time 2')]])]
layout = [[sg.Text('Testing two Frames next to each other')],
          [sg.Frame(layout=[row],
                    title='Week 1')],
          [sg.Submit(), sg.Cancel()]]

window = sg.Window('Testing Window', layout, finalize=True)
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    print(event, values)

window.close()