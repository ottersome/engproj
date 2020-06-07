import mymathnutils
from panda3d.core import *
from panda3d.core import LMatrix4f
from panda3d.core import LVecBase3f
from panda3d.core import LMatrix3f
from panda3d.core import LQuaternion
from scipy.spatial.transform import Rotation as R


class SceneObj:
    def __init__(self,
        pos = [0,0,0],
        a0 = [0,0,0],
        a1 = [0,0,0],
        a2 = [0,0,0],
        radius = [0,0,0],
        quat = [0,0,0,0],#Scalar last format
        mode = 'quat',
        catid = -1
    ):

        print("Got mode : ",mode)
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
        self.catid = catid

        #Quat Stuff
        self.quat = LQuaternion(r=quat[3],i=quat[0],j=quat[1],k=quat[2])
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
            print('We are using vectors for this')
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
        #quato = LQuaternion(r=quat4[3],i=quat4[0],j=quat4[1],k=quat4[2])
        #alden shoulve made the following unnecessary
        #print('En el file: ',quato)
        r = R.from_matrix([[self.a0[0],self.a0[1],self.a0[2]],
                           [self.a1[0],self.a1[1],self.a1[2]],
                           [self.a2[0],self.a2[1],self.a2[2]]])
        #print('Derivado de a# con scipy: ',r.as_quat())
        ##self.nodePath.setQuat(self.nodePath,quat = quato)
        ##That should be it
        ##Esto es todo lo que necesitas para quaternions
        #a0v = LVecBase3f(self.a0[0],self.a0[1],self.a0[2])
        #a1v = LVecBase3f(self.a1[0],self.a1[1],self.a1[2])
        #a2v = LVecBase3f(self.a2[0],self.a2[1],self.a2[2])
        #mat3 = LMatrix3f(a0v,a1v,a2v)
        #quaton.setFromMatrix(mat3)
        #Me Darias los resultados de "quaton"
        #quat = r.as_quat()
        #quaton = LQuaternion(quat[1],quat[2],quat[3],quat[0])
        self.nodePath.setQuat(self.nodePath,quat = quat4)
        self.nodePath.setPos(self.pos[0],self.pos[1],self.pos[2])
        #print('Derivado de a# con panda3d : ',quaton)
        #print('Done')


    def __str__(self):
        return self.modelPath
