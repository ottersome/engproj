import mymathnutils
from panda3d.core import *
class SceneObj:
    def __init__(self,
        pos = [0,0,0],
        a0 = [0,0,0],
        a1 = [0,0,0],
        a2 = [0,0,0],
        radius = [0,0,0]
    ):

        #Model Stuff
        self.modelPath = 'N/A'
        self.relModel = None
        #Geometry
        #Note: a0,a1,a2 only reflect the axis
        # initially given by data set, these wont change if we manually
        # change orientation(atleast not for now)
        self.pos = pos
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.radius = radius

        #cur eurler angles
        self.eAng = mymathnutils.getFullRot(self.a0,
            self.a1, self.a2)

        #Panda3D
        self.nodePath = None

        pass
    

    def setPos(self,x,y,z):
        self.pos = [x,y,z]

    def setNodePath(self,nodePath):
        print('Setting Node Path for ')
        self.nodePath = nodePath
        print('Rotating for : ', self.eAng)
        self.rotateSO(self.eAng[0],
            self.eAng[1],self.eAng[2])
        
    def rotateSO(self,x,y,z):
        if self.nodePath != None:
            self.eAng = [x,y,z]
            #Why would the center of rotation be the first corner ?
            self.nodePath.setHpr(x,y,z)
            pass
        else:
            print('Non-existing Node Path to rotate')

    def __str__(self):
        return self.modelPath
