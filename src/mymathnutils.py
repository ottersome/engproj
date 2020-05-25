notgottie = [1,2,22,38,40]
#notgottie = [1,2,22,38,39,40]
import numpy as np

def getAngle(v0,v1):
    # dp = |v0||v1|cos(ang)
    # |v0||v1|
    magniProduct = np.linalg.norm(v0)* np.linalg.norm(v1)
    return np.arccos(np.dot(v0,v1) / magniProduct)*180/3.1415

def getFullRot(a0,a1,a2):
    print('Getting full rot')
    print('Thius dem : ',a0)
    x = getAngle(a0,[1,0,0])  
    y = getAngle(a1,[0,1,0])  
    z = getAngle(a2,[0,0,1])  

    return [x,y,z]