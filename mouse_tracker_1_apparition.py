# This scripts demonstrates "stupid" mouse tracker, i.e.:
#
#   * the trackers has no "physical" limitations beyond its
#     frame rate f_t - on that frame rate it can "teleport"
#     (apparition in Harry Potter) anywhere in the space
#
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np
import time


# Environment initialization
f_t = 1/2 # tracker frame rate
x_m, y_m = +5,+5 # mouse start point
x_t, y_t = -5,-5 # tracker start point

# Make "environment"
fig = plt.figure()
plt.xlim(-10,10)
plt.ylim(-10,10)
plt.ion()
plt.show()

# Plot inital tracker
old_point, = plt.plot(x_t,y_t,'rx')

# Handler to get mouse coordinates
def mouse_move(event):
    global x_m, y_m
    if event.xdata: # Check Null (outside axes)
        x_m, y_m = event.xdata, event.ydata
plt.connect('motion_notify_event', mouse_move)

k = 0 # Discrete time step
start_time = time.time()
while time.time()-start_time < 10: # for 10 seconds
    old_point.remove()

    # Calculate new tracker point: apparition
    x_t, y_t = x_m, y_m
    
    old_point, = plt.plot(x_t,y_t,'rx')
    plt.draw()
    plt.pause(f_t)
