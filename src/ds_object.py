import mymathnutils
from panda3d.core import *
from panda3d.core import LMatrix4f
from panda3d.core import LVecBase3f
from panda3d.core import LMatrix3f
from panda3d.core import LQuaternion
class SceneObj:
    def __init__(self,
        pos = [0,0,0],
        a0 = [0,0,0],
        a1 = [0,0,0],
        a2 = [0,0,0],
        radius = [0,0,0],
        quat = [0,0,0,0],
        mode = 'quat'
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

        #Quat Stuff
        self.quat = quat
        
        self.mode = mode

        #cur eurler angles(shouldnt interfere with nw podel)
        self.eAng = mymathnutils.getFullRot(self.a0,
            self.a1, self.a2)

        #Panda3D
        self.nodePath = None#Bounding Box
        self.ModelNodePath = None#Bounding Box
    

    def setPos(self,x,y,z):
        self.pos = [x,y,z]

    def setNodePath(self,nodePath):
        self.nodePath = nodePath

        # Different Rotation Procedures
        # According to whether we use quats 
        # or a0 and a1
        if self.mode != 'quat':
            self.rotateSO(self.eAng[0],
                self.eAng[1],self.eAng[2])
        else:
            self.rotQuat(self.quat)
        
    def rotateSO(self,x,y,z):
        if self.nodePath != None:
            self.eAng = [x,y,z]
            a0v = LVecBase3f(self.a0[0],self.a0[1],self.a0[2])
            a1v = LVecBase3f(self.a1[0],self.a1[1],self.a1[2])
            a2v = LVecBase3f(self.a2[0],self.a2[1],self.a2[2])
            mat3 = LMatrix3f(a0v,a1v,a2v)
            mato = LMatrix4f(mat3)
            self.nodePath.setMat(mato)
            self.nodePath.setPos(self.pos[0],self.pos[1],self.pos[2])
            #Why would the center of rotation be the first corner ?
            #self.nodePath.setHpr(0,0,90)
        else:
            print('Non-existing Node Path to rotate')

    def rotQuat(self,quat4):
        quato = LQuaternion(quat4[3],quat4[0],quat4[1],quat4[2])
        self.nodePath.setQuat(quat = quato)
        #That should be it


    def __str__(self):
        return self.modelPath
