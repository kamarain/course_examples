import control
import control.matlab as cntmat
import numpy as np
import matplotlib.pyplot as plt

A = [[0, 1],
     [0, 0]]

B = [[0],
     [1]]

C = [1, 0]

D = [0]

Ts = 1/4

sys = cntmat.ss(A,B,C,D)

# Plot with reference (control) signal
t = np.arange(0,20,0.01)
u = np.zeros(t.shape)
y = cntmat.lsim(sys,u,t)
print(y[0])
plt.plot(t,u,'k', label='u=0')
plt.plot(t,y[0],'k--', label='y(u0)')
u = np.sin(t);
y = cntmat.lsim(sys,u,t)
plt.plot(t,u,'r',label='u=sin')
plt.plot(t,y[0],'r--',label='y(usin)')
plt.show()

# Next plot with PID controller
Kp = 10;
Ki = 10;
Kd = 10;
# PID feedback controller
s = control.TransferFunction.s
C = Kp+Ki*1/s+Kd*s
T = control.feedback(C*sys,1);
u = np.sin(t);
y = cntmat.lsim(T,u,t)
plt.plot(t,u,'r',label='u=sin')
plt.plot(t,y[0],'r--',label='y(usin)')
plt.show()

