import random
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d
from scipy.interpolate import griddata
from pykrige.ok import OrdinaryKriging

def buildFrame(Xlim0, Xlim1, Ylim0, Ylim1, step):
    frame = []
    for x in range(Xlim0, Xlim1, step):
        for y in range(Ylim0, Ylim1, step):
            frame.append([x,y,random.random()])
    return(frame)


def initFrameValues(frame, type="random", options=None):
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
        sampleSize = int(options[0] * len(x))
        
        #Create our kriging matrix:
        kMat = random.sample(frame, k=sampleSize)
        sam_x, sam_y, sam_z = zip(*kMat)
        x =  [float(i) for i in x]
        y =  [float(i) for i in y]
        z =  [float(i) for i in z]



        #Krig:
        ok_krig = OrdinaryKriging(sam_x,sam_y,sam_z, variogram_model="spherical", variogram_parameters={'sill':0.5, 'range':5.0, 'nugget':0},verbose=False, enable_plotting=False)
        #Get results:
        z, ss = ok_krig.execute('points', x, y)
        return(zip(x,y,z))

    return False
            

def vizFrame(frame, type="window", fPath = None):
    x,y,z = zip(*frame)
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



area = buildFrame(0,10,0,10, step=1)
area_z = initFrameValues(area, type="kriging", options=[0.05])
vizFrame(area_z, type="window")