# course_examples - repository for miscellaneous codes used in my courses

## Mouse tracker
The idea of this project is to study very basics of robot control. Our "robot" is a little virtual wagon that tries to catch the mouse pointer that user moves on the screen. We move from simple but unrealistic wagon toward more complicated but more realistic system - a system that could be actually build.

![Mouse tracker](files/mouse_tracker_1.png)


### Mouse tracker 1
The first tracker is without physial limitations. The only limit is the sampling rate 't_s' for which you may try various different values, e.g., 1, 1/2, 1/4 and so on. No physical limits means that the wagon "teleports" to the new location of target which it observes 1/t_s times per second (Hz).

### Mouse tracker 2
The second tracker is one step more realistic. It moves with the constant speed 'v' that can be changed. The speed remains the same even if you change the sampling rate 'v'. Now it should look much more realistic than the tracker number 1.

### Mouse tracker 3
The third tracker is even more realistic. The previous tracker (num. 2) was able to instantaneously change the steering angle toward the target in practice this is not possible. The tracker number 3 has constant velocity 'v' and constant rotation velocity 'v_theta'. For every observation it needs to decide only which direction to turn (clock-wise or counter clock-wise). This tracker looks very realistic, but actually it is *not*.

### Mouse tracker 4
This is the first tracker with a (almost) realistic model for kinematics: [Double Integrator](https://en.wikipedia.org/wiki/Double_integrator). Double integrator is realistic in the sense that it models how a particle with weight moves if it is pushed with some force (control signal), but still unrealistic in the sense that there is no friction or gravitation (particles do not slow down). For control models the code uses [Python Control Systems Library](https://python-control.readthedocs.io) which has similar functionality to the [Matlab Control Systems Toolbox](https://se.mathworks.com/products/control.html) which is popular within control engineers. To see basic study on double integrator have a look on the files *double_integrator.m* (Matlab) and *double_integrator.py* (Python version of the same code). For this simple demo we use continuous models that avoids some problems of the discrete control systems, but that's not bad at all.
