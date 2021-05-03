# MOUSE_TRACKER_4.PY
#
#   * This tracker is almost realistic. It uses the double integrator
#     model of kinematics. The control signal 'u' creates (power) creates
#     acceleration.
#
#      x' = Ax+Bu
#      y  = Cx
#
#   *  The same model is used for the both spatial velocity v and
#      angular velocity v_theta
#
#     We also use a PID controller where the control signals are
#     distance to the target (velocity) and angular difference
#     (angular velocity).
#
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np
import time
import control
import control.matlab as cntmat

time.sleep(1)

# Environment initialization
t_s = 1/8 # sampling time in seconds
x_m, y_m = +5,+5 # mouse start point
x_t, y_t = -5,-5 # tracker start point
theta_t = 0 # tracker angle start point

# Motion model (Double Integrator)
A = [[0, 1],
     [0, 0]]
B = [[0],
     [1]]
C = [1, 0]
D = [0]
sys = cntmat.ss(A,B,C,D)

# PID controller parameters for velocity and angular velocity
Kp_v, Kp_theta = 10, 10;
Ki_v, Ki_theta = 0, 0;
Kd_v, Kd_theta = 1, 2;
s = control.TransferFunction.s
C_v = Kp_v+Ki_v*1/s+Kd_v*s
T_v = control.feedback(C_v*sys,1);
C_theta = Kp_theta+Ki_theta*1/s+Kd_theta*s
T_theta = control.feedback(C_theta*sys,1);

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

    # Move to [0,360] to make them comparable
    if theta < 0:
        theta_360 = 2*np.pi+theta
    else:
        theta_360 = theta
    if theta_t < 0:
        theta_t_360 = 2*np.pi+theta_t
    else:
        theta_t_360 = theta_t
    
    theta_diff_360 = theta_360-theta_t_360
    if np.abs(theta_diff_360) > np.pi:
        theta_sign = -np.sign(theta_diff_360)
        theta_diff = np.abs(2*np.pi-theta_diff_360)
    else:
        theta_sign = np.sign(theta_diff_360)
        theta_diff = np.abs(theta_diff_360)

    #theta_t = theta_t+theta_sign*v_theta
    
    # Sample dynamic model for this observation time
    t = np.arange(0,t_s,0.01)
    u = np.ones(t.shape)*(theta_sign*theta_diff)
    theta_y = cntmat.lsim(T_theta,u,t);
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
    
    t = np.arange(0,t_s,0.01)
    u = np.ones(t.shape)*mouse_dist
    mouse_y = cntmat.lsim(T_v,u,t);
    mouse_y = mouse_y[0][-1]
    #x_t = x_t+np.cos(np.arctan2(y_m-y_t,x_m-x_t))*mouse_y
    #y_t = y_t+np.sin(np.arctan2(y_m-y_t,x_m-x_t))*mouse_y
    v = mouse_y
    
    x_k = np.array([x_t, y_t, np.cos(theta_t)*v, np.sin(theta_t)*v])
    G = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]])
    x_kk = G@x_k.T
    
    x_t, y_t = x_kk[0], x_kk[1]
    
    old_point, = plt.plot(x_t,y_t,'rx')
    plt.draw()
    plt.pause(t_s)
