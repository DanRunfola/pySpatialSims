
import pySpatialSims as pss

area = pss.buildFrame(0,10,0,10, step=1)
area_z = pss.initFrameValues(area, type="kriging", options={'sample_size':0.02,'sill':0.95, 'range_per':1.0, 'nugget':0.01})

print(pss.estMorans(area_z))
pss.vizFrame(area_z, type="window")


#Parameters to think through
#Initial covariate spatial correlations
#Initial intervention spatial correlations
#Spatial correlation in effectiveness of intervention
#Spatial spillover of intervention
#Error in measurements
#Error in spatial location of interventions