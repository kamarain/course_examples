% Double integrator (continuous)
A = [0       1;
     0       0];

B = [  0;
       1];

C = [1 0];

D = [0];

sys = ss(A,B,C,D);

% Plot with reference (control) signal
t = 0:0.01:20;
u = zeros(size(t));
y = lsim(sys,u,t);
plot(t,u,'k',t,y,'k--');
u = sin(t);
y = lsim(sys,u,t);
hold on;
plot(t,u,'r',t,y,'r--');
hold off;
legend('u=0', 'y_0','u=sin(t)','y_{sin}');
title('Double integrator without control');
input('<RETURN>');

% Next plot with PID feedback controller
Kp = 20;
Ki = 10;
Kd = 5;
% PID feedback controller
C = pid(Kp,Ki,Kd); % Matlab function
s = tf('s');
C = Kp+Ki*1/s+Kd*s % Own construction
T = feedback(C*sys,1);
C*sys

u = sin(t);
y = lsim(T,u,t);
plot(t,u,'r',t,y,'r--');
legend('u=sin(t)','y_{sin}');
title('Double integrator with control');
