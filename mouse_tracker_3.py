# MOUSE_TRACKER_2.PY
#
#   * This tracker has constant velocity and constant angular velocity and
#     observes target at the frame rate of 1/t_s
#
#     x^ = [v v_theta]
#
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np
import time

# Environment initialization
t_s = 1/8 # sampling time in seconds
x_m, y_m = +5,+5 # mouse start point
x_t, y_t = -5,-5 # tracker start point
theta_t = 0 # tracker angle start point
v = 2.0*t_s # constant velocity per second 
v_theta = 0.5*np.pi*t_s # constant rotation per second (1*pi is 180deg)

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

# Handler to get keyboard inputs
def key_pressed(event):
    if event.key == 'q': # quit
        exit()
plt.connect('key_press_event', key_pressed)

# Main loop for tracking
while True:
    old_point.remove()

    # Global angle from the current location to target
    theta = np.arctan2(y_m-y_t,x_m-x_t)
    # Move to [0,360]
    if theta < 0:
        theta_360 = 2*np.pi+theta
    else:
        theta_360 = theta
    if theta_t < 0:
        theta_t_360 = 2*np.pi+theta_t
    else:
        theta_t_360 = theta_t

    theta_diff = theta_360-theta_t_360
    if np.abs(theta_diff) > np.pi:
        theta_sign = -np.sign(theta_diff)
    else:
        theta_sign = np.sign(theta_360-theta_t_360)
    theta_t = theta_t+theta_sign*v_theta
    # Keep this in [-180,0,+180]
    if theta_t > np.pi: 
        theta_t = -np.pi+(theta_t-np.pi)
    if theta_t < -np.pi:
        theta_t = np.pi+(theta_t+np.pi)
    
    x_k = np.array([x_t, y_t, np.cos(theta_t)*v, np.sin(theta_t)*v])
    G = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]])
    x_kk = G@x_k.T
    
    #x_k = np.array([x_t ])
    x_t, y_t = x_kk[0], x_kk[1]
    
    old_point, = plt.plot(x_t,y_t,'rx')
    plt.draw()
    plt.pause(t_s)
