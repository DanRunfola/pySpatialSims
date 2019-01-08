from pykrige.ok import OrdinaryKriging
from pykrige.uk import UniversalKriging
import math
import copy
import random
import numpy as np
import pandas as pd

def initFrameValues(frame, type="random",  options={'sample_size':0.02,'sill':0.05, 'range_per':5.0, 'nugget':0}, ked_secondary = None):
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

    if(type == "ked"):
        if(ked_secondary == None):
            print("You must specify a secondary frame to base the drift off of for Kriging with External Drift.")
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

        #Create the drift matrix:
        dri_x, dri_y, dri_z = zip(*ked_secondary)
        ked_x =  [float(i) for i in dri_x]
        ked_y =  [float(i) for i in dri_y]
        ked_z =  [float(i) for i in dri_z]
        ked_dta = np.array([ked_x, ked_y, ked_z])

        ked_pd = pd.DataFrame(ked_dta, columns=['x','y','z'])
        print(ked_pd)
        ked_pivot = ked_pd.pivot_table(values='z', index='x', columns='y')
        print(ked_pivot)
        #Calculate the range as a percentage of the maximum distance in the matrix based on the input dimensions
        max_dist = math.sqrt((max(x)-min(x))**2 + (max(y)-min(y))**2)
        options['range'] = max_dist * options['range_per']

        ked_krig = UniversalKriging(sam_x,sam_y,sam_z, drift_terms='external_Z', variogram_model="spherical", point_drift = ked_mat, variogram_parameters={'sill':options['sill'], 'range':options['range'], 'nugget':options['nugget']},verbose=False, enable_plotting=False)
        #Get results:
        z, ss = ked_krig.execute('points', x, y)
        return(zip(x,y,z))

    return False