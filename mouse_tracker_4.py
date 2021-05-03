# This scripts demonstrates LDS mouse tracker
#
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np
import time
import control
import control.matlab as cntmat

time.sleep(1)

# Environment initialization
f_t = 1/10 # tracker frame rate per second
x_m, y_m = +5,+5 # mouse start point
x_t, y_t = -5,-5 # tracker start point
theta_t = 0
v = 2.0*f_t # constant velocity per second
v_theta = 2*np.pi*1*f_t # constant rotation per second

# Motion model (Double Integrator)
A = [[0, 1],
     [0, 0]]
B = [[0],
     [1]]
C = [1, 0]
D = [0]
sys = cntmat.ss(A,B,C,D)

# PID controller
Kp = 1;
Ki = 0;
Kd = 0.1;
s = control.TransferFunction.s
C = Kp+Ki*1/s+Kd*s
T = control.feedback(C*sys,1);

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

    #theta_t = theta_t+theta_sign*v_theta
    # Sample angle model for f_t seconds (curr angle = 0)
    t = np.arange(0,2,0.01)
    u = np.ones(t.shape)*theta_diff
    theta_y = cntmat.lsim(T,u,t);
    theta_y = theta_y[0][-1]
    theta_t = theta_t+theta_y

    # Keep this in [-180,0,+180]
    if theta_t > np.pi: 
        theta_t = -np.pi+(theta_t-np.pi)
    if theta_t < -np.pi:
        theta_t = np.pi+(theta_t+np.pi)
    
    #theta_t = np.sign(theta_t)*(np.abs(theta_t) % np.pi)
    #print(theta_t*180/np.pi)

    # Sample angle model for f_t seconds (curr angle = 0)
    mouse_dist = np.linalg.norm([x_t-x_m,y_t-y_m])
    print(mouse_dist)
    if mouse_dist > 10:
        mouse_dist = 10
    
    t = np.arange(0,0.5,0.1)
    u = np.ones(t.shape)*mouse_dist
    mouse_y = cntmat.lsim(T,u,t);
    mouse_y = mouse_y[0][-1]
    x_t = x_t+np.cos(np.arctan2(y_m-y_t,x_m-x_t))*mouse_y
    y_t = y_t+np.sin(np.arctan2(y_m-y_t,x_m-x_t))*mouse_y
    
    #    x_k = np.array([x_t, y_t, np.cos(theta_t)*v, np.sin(theta_t)*v])
    #    G = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]])
    #    x_kk = G@x_k.T
    
    #    x_t, y_t = x_kk[0], x_kk[1]
    
    old_point, = plt.plot(x_t,y_t,'rx')
    plt.draw()
    plt.pause(f_t)
