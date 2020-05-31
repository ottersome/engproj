#notgottie = [1,2,22,38,40]
notgottie = [0,1,2,22,38,40]
import numpy as np

def getAngle(v0,v1):
    magniProduct = np.linalg.norm(v0)* np.linalg.norm(v1)
    return np.arccos(np.dot(v0,v1) / magniProduct)*180/3.1415

def getFullRot(a0,a1,a2):
    x = np.arctan2(a2[1],a2[2])*180/np.pi
    y = np.arctan2(-a2[0],np.sqrt(a2[1]**2 + a2[2]**2))*180/np.pi
    z = np.arctan2(a1[0],a0[0])*180/np.pi
    #x = getAngle(a0,[1,0,0])  
    #y = getAngle(a1,[0,1,0])  
    #z = getAngle(a2,[0,0,1])  
    #print('Angs : ',angs)
    return [x,y,z]
