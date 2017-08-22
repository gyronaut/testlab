#!/usr/bin/python
import numpy;
import math;
import matplotlib.pyplot as plt;
import random;
from matplotlib.colors import LinearSegmentedColormap;

#function to initialize the stage (set boundaries to 100)
def initialize(nrows, ncols, points):
    rows = nrows;
    cols = ncols;
    stage = numpy.zeros((rows,cols));

    for i in range(0, rows):
        stage[i][0] = 10000.0;
        stage[i][cols-1] = 10000.0;

    for j in range(0, cols):
        stage[0][j] = 10000.0;
        stage[rows-1][j] = 10000.0;
    for pt in points:
        if (pt[0] < nrows and pt[0]>0 and pt[1] < ncols and pt[1]>0):
            stage[pt[0]][pt[1]] = 10000.0;
    return stage

#function to recursively "relax" the stage based on the current stage (each cell becomes an average of it's nearest neighbors, except source cells)
def relax(stage, nrows, ncols, nsteps, points, weight):
    nsteps = nsteps - 1;
    if nsteps==0:
        return stage;
    nextstage = initialize(nrows, ncols, ());
    for i in range(0,nrows):
        for j in range(0,ncols):
            ispoint = False;
            for k in range(len(points)):
                if(i==points[k][0] and j==points[k][1]):
                    ispoint = True;
            if ispoint:
                nextstage[i][j] = 10000.0;
            #adding a plus to the center of the stage
            #elif ((i>48 and i<51) and (j < 69 and j >30)) or ((j>48 and j<51) and (i < 69 and i > 30)):
            #    nextstage[i][j] = 10000.0
            #adding a circle to the center of the stage:
            elif ((math.sqrt((i-49.5)*(i-49.5) + (j-49.5)*(j-49.5)) < 20) and (math.sqrt((i-49.5)*(i-49.5)+(j-49.5)*(j-49.5)) >17) and not ((math.atan2(i-49.5,j-49.5) < 1.31 and (math.atan2(i-49.5,j-49.5) > 0.26)) or ((math.atan2(i-49.5,j-49.5)) > -2.88 and (math.atan2(i-49.5,j-49.5) < -1.83)))):
                nextstage[i][j] = 10000.0
            #relaxing the interior
            elif (i!=0 and i!=nrows-1 and j!=0 and j!=ncols-1):
                nextstage[i][j] = weight*stage[i][j] + (1-weight)*(0.125*(stage[i-1][j] + stage[i+1][j] + stage[i][j-1] + stage[i][j+1]) + 0.125*0.707*(stage[i-1][j-1] + stage[i-1][j+1] + stage[i+1][j-1] + stage[i+1][j+1]));
            #setting catch for the border cells
            else:
                nextstage[i][j] = 10000.0
    stage = nextstage;
    return relax(stage, nrows, ncols, nsteps, points, weight);

#function that takes all points that are set to 100, and moves them in the direction of lowest value
def move(stage, nrows, ncols, points):
    newpoints = points;
    for i in range(len(points)):
        pt = points[i];
        if (pt[0]>0 and pt[0]<nrows-1 and pt[1]>0 and pt[1]<ncols-1):
            nextpt = pt;
            value = stage[pt[0]][pt[1]];
            for r in (-1,0,1):
                for c in (-1,0,1):
                    newvalue = ((1+(math.sqrt(2)-1)*math.fabs(r*c))*stage[pt[0]+r][pt[1]+c]);
                    if value > random.gauss(0,100)+newvalue:
                        nextpt = [pt[0]+r, pt[1]+c];
                        value = newvalue;
        newpoints[i] = nextpt;
        stage[nextpt[0]][nextpt[1]] = 10000.0;
    for i in range(len(points)):
        points[i] = newpoints[i];
    return stage;


rows = 100;
cols = 100;
points = [[56,45], [20,36], [80,12], [83,90], [15,30], [92,47], [27, 51], [40, 69], [4, 20], [12,11], [19, 88]]
stage = initialize(rows,cols, points);
stage = relax(stage,rows,cols, 50, points, 0.0);
print points;

colors = {'red': ((0.0, 36.0/255.0, 36.0/255.0),
                  (0.25, 181.0/255.0, 181.0/255.0),
                  (0.5, 16.0/255.0, 16.0/255.0),
                  (0.75, 36.0/255.0, 36.0/255.0),
                  (1.0, 109.0/255.0, 109.0/255.0)),
          'green': ((0.0, 77./255., 77./255.),
                    (0.25, 201./255., 201./255.),
                    (0.5, 201./255., 201./255.),
                    (0.75, 54./255., 54./255.),
                    (1.0, 154./255., 154./255.)),
          'blue': ((0.0, 54./255., 54./255.),
                   (0.25, 16./255., 16./255.),
                   (0.5, 147./255., 147./255.),
                   (0.75, 39./255., 39./255.),
                   (1.0, 1.0, 1.0))
          }
colormap = LinearSegmentedColormap('worm', colors)

fig = plt.figure(figsize=(3, 3))
plt.box('off')
plt.axis('off')
plt.imshow(stage, cmap=colormap)
plt.margins(0,0)
#plt.show()
plt.savefig("test.png")
plt.close(fig)

#let the points start moving around
for i in range(0,1000):
    stage = move(stage, rows, cols, points);
    stage = relax(stage, rows, cols, 2, points, 0.995);
    #print points;
    if i%10==0:
        fig = plt.figure(figsize=(3, 3))
        plt.box('off')
        plt.axis('off')
        plt.imshow(stage, cmap=colormap)
        plt.margins(0,0)
        framenum = (i/10)
        filename = "vid_roller/roller9_frame" + str(framenum) + ".png"
        plt.savefig(filename)
        plt.close(fig)

#delete the points, fade out
for j in range(0,120):
    stage = relax(stage, rows, cols, 2, [], 0.7);
    if j%2==0:
        fig = plt.figure(figsize=(3, 3))
        plt.box('off')
        plt.axis('off')
        plt.imshow(stage, cmap=colormap)
        plt.margins(0,0)
        framenum = 100 + (j/2)
        filename = "vid_roller/roller9_frame" + str(framenum) + ".png"
        plt.savefig(filename)
        plt.close(fig)

