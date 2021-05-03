# This scripts demonstrates LDS mouse tracker
#
#   Linear Dynamic System (LDS) - constant speed
#
#     x^d = A
#
#   The tracker is still not realistic as it can turn to any angle
#   without delay
#
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np
import time

# Environment initialization
f_t = 1/10 # tracker frame rate per second
x_m, y_m = +5,+5 # mouse start point
x_t, y_t = -5,-5 # tracker start point
v = 5.0*f_t # constant velocity per second

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

    # Calculate new tracker point: constant velocity LDS
    k = k+1
    theta = np.arctan2(y_m-y_t,x_m-x_t)
    x_k = np.array([x_t, y_t, np.cos(theta)*v, np.sin(theta)*v])
    G = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]])
    x_kk = G@x_k.T
    
    #x_k = np.array([x_t ])
    x_t, y_t = x_kk[0], x_kk[1]
    
    old_point, = plt.plot(x_t,y_t,'rx')
    plt.draw()
    plt.pause(f_t)
