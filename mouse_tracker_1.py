# MOUSE_TRACKER_1.PY
#
#   * This trackers has no physical limitations beyond its
#     sampling rate 1/t_s
#   * It "teleports" to the mouse pointer every time it observes it
#
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np
import time

# Environment initialization
t_s = 1/4 # sampling time in seconds
x_m, y_m = +5,+5 # mouse start point
x_t, y_t = -5,-5 # tracker start point


# Make "environment"
fig = plt.figure()
plt.xlim(-10,10)
plt.ylim(-10,10)
plt.ion()
plt.title('Mouse tracker 1 (press q to quit)')
plt.show()

# Plot inital tracker
old_point, = plt.plot(x_t,y_t,'rx')

# Handler to get mouse coordinates
def mouse_move(event):
    global x_m, y_m
    if event.xdata: # Check Null (outside axes)
        x_m, y_m = event.xdata, event.ydata
plt.connect('motion_notify_event', mouse_move)

# Handler to get keyboard inputs
def key_pressed(event):
    if event.key == 'q': # quit
        exit()
plt.connect('key_press_event', key_pressed)

# Main loop for tracking
while True:
    old_point.remove()

    # Calculate new tracker point: apparition
    x_t, y_t = x_m, y_m
    
    old_point, = plt.plot(x_t,y_t,'rx')
    plt.draw()
    plt.pause(t_s)
