#!/bin/python
import numpy as np;
import matplotlib.pyplot as plt;
import matplotlib.animation as animation;

PI = 3.14159265359;
ANGLE = PI/2000.0;

POS_INIT = [(13.0, 15.0), (13.0, 15.0),(13.0, 15.0),(13.0, 15.0),(13.0, 15.0),(13.0, 15.0)];
VEL_INIT = [(np.cos(PI/4.0 + i*ANGLE), np.sin(PI/4.0 + i*ANGLE)) for i in range(-3, 3)];
COLORS = ['red', 'darkorange', 'gold', 'forestgreen', 'royalblue', 'rebeccapurple']

pos = POS_INIT;
vel = VEL_INIT;

HALFWIDTH = 20.0;
RADIUS = 10.0;
DT = 0.05;
STEPS = 20;
NUM_POINTS = 6;

def columntop(t):
    return np.sqrt(RADIUS*RADIUS - t*t);

def columnbot(t):
    return -np.sqrt(RADIUS*RADIUS - t*t);

def propagate(pos, vel):
    x = pos[0] + vel[0]*DT;
    y = pos[1] + vel[1]*DT;
    return [x, y];

def updateVelocity(pos, vel):
    if (pos[0]*pos[0] + pos[1]*pos[1] <= RADIUS*RADIUS):
        theta = np.arctan2(pos[1], pos[0]);
        degrees = theta*180.0/3.14159;
        #print "theta: %f" % degrees;
        vx_prime = np.cos(-theta)*vel[0] - np.sin(-theta)*vel[1];
        vx_prime = -vx_prime;
        vy_prime = np.sin(-theta)*vel[0] + np.cos(-theta)*vel[1];
        vx = np.cos(theta)*vx_prime - np.sin(theta)*vy_prime;
        vy = np.sin(theta)*vx_prime + np.cos(theta)*vy_prime;
        #print 'theta {} old ({}, {}), transformed ({}, {}), new ({}, {})'.format(degrees, vel[0], vel[1], vx_prime, vy_prime, vx, vy);
        return [vx, vy];
    elif (np.abs(pos[0]) >= HALFWIDTH):
        return [-vel[0], vel[1]];
    elif (np.abs(pos[1]) >= HALFWIDTH):
        return [vel[0], -vel[1]];
    return vel;

plt.ion();

x = np.arange(-RADIUS, RADIUS+0.02, 0.01);


fig = plt.figure();
ax = fig.add_subplot(121);
plt.axis("square");
plt.xticks([]);
plt.yticks([]);
plt.plot((0.0, 0.0), (RADIUS, HALFWIDTH), 'k--');
#plt.plot((0.0, 0.0), (-HALFWIDTH, -RADIUS), 'k--');
ax.set_xlim([-HALFWIDTH, HALFWIDTH]);
ax.set_ylim([-HALFWIDTH, HALFWIDTH]);
coltop, = ax.plot(x, columntop(x), 'k');
colbot, = ax.plot(x, columnbot(x), 'k');
point = [];
for i in range(0, NUM_POINTS):
    obj = ax.plot(pos[i][0], pos[i][1], color=COLORS[i], marker = 'o')[0];
    point.append(obj);

#code for second phase space plot
ax2 = fig.add_subplot(122);
plt.axis("square");
plt.xticks([]);
plt.yticks([]);
ax2.set_xlim([0.0, HALFWIDTH]);
ax2.set_ylim([-1.0, 1.0]);
ax2.set_aspect(20.0/2.0, adjustable='box');
phase = [];
phaseobj = [];
for i in range(0, NUM_POINTS):
    phase.append([[100], [100]]);
    obj = ax2.plot(phase[i][0], phase[i][1], color=COLORS[i], marker = '.', markersize = 4.0, linestyle='None')[0];
    phaseobj.append(obj);

def animate(t):
    global pos;
    global vel;
    global phase;
    if (t==0):
        return tuple(point);
    numsteps = int(1+ int(t/10)*0.05)*STEPS;
    for ptNum, pt in enumerate(point):
        for i in range(0, numsteps):
            newpos = propagate(pos[ptNum], vel[ptNum]);
            if(newpos[0]*pos[ptNum][0] < 0):
                phase[ptNum][0].append(newpos[1]);
                phase[ptNum][1].append(vel[ptNum][1]);
                #if (ptNum == 0):
                    #print phase[ptNum][0]
                    #print phase[ptNum][1]
                phaseobj[ptNum].set_xdata(phase[ptNum][0]);
                phaseobj[ptNum].set_ydata(phase[ptNum][1]);
            pos[ptNum] = newpos;
            vel[ptNum] = updateVelocity(pos[ptNum], vel[ptNum]);
            pt.set_xdata(pos[ptNum][0]);
            pt.set_ydata(pos[ptNum][1]);
    return tuple(point) + tuple(phaseobj)


ani = animation.FuncAnimation(fig, animate, frames=5000, blit=True);

ani.save('test_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264']);

plt.show();    


