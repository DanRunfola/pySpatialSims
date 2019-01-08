import random

def buildFrame(Xlim0, Xlim1, Ylim0, Ylim1, step):
    frame = []
    for x in range(Xlim0, Xlim1, step):
        for y in range(Ylim0, Ylim1, step):
            frame.append([x,y,random.random()])
    return(frame)