
import pySpatialSims as ss

area = ss.buildFrame(0,10,0,10)
area_z = ss.initFrameValues(area, type="kriging", options={'sample_size':0.2,'sill':0.95, 'range_per':0.15, 'nugget':0.01})
area_u = ss.initFrameValues(area, type="ked", options={'sample_size':0.2,'sill':0.95, 'range_per':0.15, 'nugget':0.01}, ked_secondary=area_z)
print(ss.estMorans(area_u))
ss.vizFrame(area_u, type="window")
ss.vizFrame(area_z, type="window")

#Parameters to think through
#Initial covariate spatial correlations

#LEFT OFF: NEed to figure out hwo to get the point drift frames into a format acceptable by Ukrig - see 
#https://stackoverflow.com/questions/42299587/python-transform-list-of-x-y-and-z-to-matrix-table
#https://pykrige.readthedocs.io/en/latest/generated/pykrige.uk.UniversalKriging.html