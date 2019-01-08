import random
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d
from scipy.interpolate import griddata
from pykrige.ok import OrdinaryKriging
import pysal as ps
import math
import copy

def buildFrame(Xlim0, Xlim1, Ylim0, Ylim1, step):
    frame = []
    for x in range(Xlim0, Xlim1, step):
        for y in range(Ylim0, Ylim1, step):
            frame.append([x,y,random.random()])
    return(frame)


def initFrameValues(frame, type="random",  options={'sample_size':0.02,'sill':0.05, 'range_per':5.0, 'nugget':0}):
    valFrame = []
    if(type == "random"):
        for obs in frame:
            valFrame.append([obs[0], obs[1], random.random()])
        return valFrame

    if(type=="kriging"):
        x,y,z = zip(*frame)
        #Randomly sample from the input frame a set number of seeds to use
        #For kriging.
        # Set as a percentage 
        sampleSize = int(options['sample_size']*len(x))#int(options[0] * len(x))
        
        #Create our kriging matrix:
        kMat = random.sample(frame, k=sampleSize)
        sam_x, sam_y, sam_z = zip(*kMat)
        x =  [float(i) for i in x]
        y =  [float(i) for i in y]
        z =  [float(i) for i in z]

        #Calculate the range as a percentage of the maximum distance in the matrix based on the input dimensions
        max_dist = math.sqrt((max(x)-min(x))**2 + (max(y)-min(y))**2)
        options['range'] = max_dist * options['range_per']
        #Krig:
        ok_krig = OrdinaryKriging(sam_x,sam_y,sam_z, variogram_model="spherical", variogram_parameters={'sill':options['sill'], 'range':options['range'], 'nugget':options['nugget']},verbose=False, enable_plotting=False)
        #Get results:
        z, ss = ok_krig.execute('points', x, y)
        return(zip(x,y,z))

    return False
            

def vizFrame(frame, type="window", fPath = None):
    workingFrame = copy.deepcopy(frame)
    x,y,z = zip(*workingFrame)
    z = list(map(float, z))
    grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]
    grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')

    if(type == "window"):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_surface(grid_x, grid_y, grid_z, cmap=plt.cm.Spectral)
        plt.show()


def sampleFrame(n, frame, pStrat="random"):
    if(pStrat=="random"):      
        print("Return")


def estMorans(frame):
    workingFrame = copy.deepcopy(frame)
    x,y,z = zip(*workingFrame)
    w = ps.lat2W(int(max(x)+1.0), int(max(y)+1.0), rook=False)
    lm = ps.Moran(z,w)
    return(lm.I)

area = buildFrame(0,10,0,10, step=1)
area_z = initFrameValues(area, type="kriging", options={'sample_size':0.02,'sill':0.95, 'range_per':1.0, 'nugget':0.01})

print(estMorans(area_z))
vizFrame(area_z, type="window")


#Parameters to think through
#Initial covariate spatial correlations
#Initial intervention spatial correlations
#Spatial correlation in effectiveness of intervention
#Spatial spillover of intervention
#Error in measurements
#Error in spatial location of interventions