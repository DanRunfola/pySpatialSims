import copy
import pysal as ps

def estMorans(frame):
    workingFrame = copy.deepcopy(frame)
    x,y,z = zip(*workingFrame)
    w = ps.lat2W(int(max(x)+1.0), int(max(y)+1.0), rook=False)
    lm = ps.Moran(z,w)
    return(lm.I)