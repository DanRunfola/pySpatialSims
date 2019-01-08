import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d
from scipy.interpolate import griddata
import copy

def vizFrame(frame, type="window"):
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