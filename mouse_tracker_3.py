# This scripts demonstrates LDS mouse tracker
#
#   Linear Dynamic System (LDS) - constant speed
#
#     [theta^d v^d] = x^d = A
#
#   This tracker is semi-realistic - it moves on constant speed and
#   it rotates on constant speeed. Semi in the sense that switching
#   the rotation direction immediately is not completely realistic.
#
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np
import time

# Environment initialization
f_t = 1/10 # tracker frame rate per second
x_m, y_m = +5,+5 # mouse start point
x_t, y_t = -5,-5 # tracker start point
theta_t = 0
v = 2.0*f_t # constant velocity per second
v_theta = 2*np.pi*1*f_t # constant rotation per second

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
while time.time()-start_time < 20: # for 10 seconds
    old_point.remove()

    # Calculate new tracker point: constant velocity LDS
    k = k+1
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
    
    #theta_t = np.sign(theta_t)*(np.abs(theta_t) % np.pi)
    print(theta_t*180/np.pi)
    x_k = np.array([x_t, y_t, np.cos(theta_t)*v, np.sin(theta_t)*v])
    G = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]])
    x_kk = G@x_k.T
    
    #x_k = np.array([x_t ])
    x_t, y_t = x_kk[0], x_kk[1]
    
    old_point, = plt.plot(x_t,y_t,'rx')
    plt.draw()
    plt.pause(f_t)
