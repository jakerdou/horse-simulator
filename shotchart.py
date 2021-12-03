'''Reference used to create court: https://towardsdatascience.com/make-a-simple-nba-shot-chart-with-python-e5d70db45d0d
Dimensions are changed to fit our design needs'''

import matplotlib as mpl
import matplotlib.pyplot as plt

def court(axes):
    axes.plot([-220, -220], [330, 470], linewidth=2, color='black')
    axes.plot([220, 220], [330, 470], linewidth=2, color='black')
    axes.add_artist(mpl.patches.Arc((0, 330), 440, 315, theta1=0, theta2=180, angle=180, facecolor='none', edgecolor='black', lw=2))
    axes.plot([-80, -80], [280, 470], linewidth=2, color='black')
    axes.plot([80, 80], [280, 470], linewidth=2, color='black')
    axes.plot([-60, -60], [280, 470], linewidth=2, color='black')
    axes.plot([60, 60], [280, 470], linewidth=2, color='black')
    axes.plot([-80, 80], [280, 280], linewidth=2, color='black')
    axes.add_artist(mpl.patches.Circle((0, 280), 60, facecolor='none', edgecolor='black', lw=2))   #key
    axes.add_artist(mpl.patches.Circle((0, 430), 15, facecolor='none', edgecolor='black', lw=2))   #rim
    axes.plot([-30, 30], [450, 450], linewidth=2, color='black')  #backboard
    axes.set_xlim(-250, 250)
    axes.set_ylim(0, 470)

def make(axes, x, y):
    axes.add_artist(mpl.patches.Circle((x,y), 12, facecolor='none', fill='true',edgecolor='green', lw=1))

def miss(axes, x, y):
    axes.plot(x, y, marker="x", color="red", markersize=15)

# fig = plt.figure(figsize=(5, 4.5))
# axes = fig.add_axes([0, 0, 1, 1])
# court(axes)
# plt.show()