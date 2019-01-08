from pykrige.ok import OrdinaryKriging
import math
import copy
import random

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