from math import pi, sin, cos
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

#from panda3d.core import AmbientLight
#from panda3d.core import Vec4
#from panda3d.core import GeomVertexData
from panda3d.core import *

from direct.task import Task
from random import random

import sys
import pandas as pd
import numpy as np
from panda3d.core import LineSegs


loadPrcFileData("", "load-file-type p3assimp")


class MyApp(ShowBase):

    def LoadSofa(self):
        self.scene = self.loader.loadModel("/home/ottersome/Projects/EngineeringProject/Models/Alden/working/cat34_sink.egg",)
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        ## Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(0, 0, 10)

        self.notgottie = [2,22,38,39,40]

    def getPoints(self):
        df = pd.read_csv(sys.argv[1])
        for index,row in df.iterrows():
            self.points.append([row['px'],row['py'],row['pz']])
            self.a0.append([row['a0x'],row['a0y'],row['a0z']]);
            self.a1.append([row['a1x'],row['a1y'],row['a1z']]);

            #THe normalization and orthogonalizaiton thingy
            self.a0n.append(self.a0[-1]/np.linalg.norm(self.a0[-1]))
            self.a1n.append(self.a1[-1]/np.linalg.norm(self.a1[-1]))
            self.a1n[-1]  = np.cross(self.a0n[-1],self.a1n[-1])
            self.a1n[-1]  = np.cross(self.a1n[-1],self.a0n[-1])
            self.a1n[-1] =  (self.a1n[-1]/np.linalg.norm(self.a1n[-1]))
            self.a2n.append(np.cross(self.a0n[-1],self.a1n[-1]));

            #print("Ford index : %d Coords : (%.3f,%.3f,%.3f)"%
            #    (row['objectIndex'],row['px'],row['py'],row['pz']))

    def __init__(self):
        ShowBase.__init__(self)
        self.amntObjs = 0
        self.points = []
        self.colors = []
        self.a0 = []
        self.a1 = []
        self.a0n = []
        self.a1n = []
        self.a2n = []


        # Load the environment model.

        #arrs = self.GeomVertexArraFormat()
        #arrs.addColumn("vertex",3,Geom.NTFloat32,Geom.CPoint)
        #forms = GeomVertexFormat()
        #forms.addArray(arrs)
        #forms = GeomVertexFormat.registerFormat(forms)
        self.getPoints()

        self.drawPlane()
        self.LoadSofa()
        self.drawSpherex(self.points)
        self.drawLineSegments(self.points)
        base.disableMouse()
        base.camera.setPos(-2,-18,20)
        base.camera.lookAt(-2,-18,0)
        base.oobe()

        plight = PointLight('plight')
        plight.setColor((0.9, 0.9, 0.9, 1))
        plnp = render.attachNewNode(plight)
        plnp.setPos(0, 0, 1)
        render.setLight(plnp)
        #  ambientLight = AmbientLight("Ambient Light")
        #  ambientLight.setColor(Vec4(0.1,0.1,0.1,1))
        #  self.ambientLightNP = self.render.attachNewNode(ambientLight)
        #  self.render.setLight(self.ambientLightNP)
        #self.taskMgr.add(self.spinCameraTask,"SpinCameraTask")

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees*(pi/180)
        self.camera.setPos(20*sin(angleRadians),-20*cos(angleRadians),10)
        self.camera.setHpr(angleDegrees,0,0)
        return Task.cont

    def drawPlane(self):
        vdata = GeomVertexData('',GeomVertexFormat.getV3n3c4(),Geom.UHStatic)
        vertex = GeomVertexWriter(vdata,'vertex')
        color = GeomVertexWriter(vdata,'color')
        normal = GeomVertexWriter(vdata,'normal')
        center = [0,0,0]
        halfW = 20

        #Add four points that make up a plane
        vertex.addData3f(-halfW,halfW,0)
        color.addData4f(1,1,1,1)
        normal.addData3f(0,0,1)
        vertex.addData3f(-halfW,-halfW,0)
        color.addData4f(1,1,1,1)
        normal.addData3f(0,0,1)
        vertex.addData3f(halfW,halfW,0)
        color.addData4f(1,1,1,1)
        normal.addData3f(0,0,1)
        vertex.addData3f(halfW,-halfW,0)
        color.addData4f(1,1,1,1)
        normal.addData3f(0,0,1)

        prim = GeomTristrips(Geom.UHStatic)
        for i in range(4):
            prim.addVertex(i)
        prim.close_primitive()

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        node = GeomNode('planeNode')
        node.addGeom(geom)

        nodePath = self.render.attachNewNode(node)



    def drawSpherex(self,points):

        vdata = GeomVertexData('',GeomVertexFormat.getV3c4(),Geom.UHStatic)
        vertex = GeomVertexWriter(vdata,'vertex')
        color = GeomVertexWriter(vdata,'color')

        for point in points:
            self.amntObjs = self.amntObjs +1
            vertex.addData3f(point[0],point[1],point[2])
            self.colors.append([random(),random(),random()])
            color.addData4f(self.colors[-1][0],self.colors[-1][1],self.colors[-1][0],1)

            #Draw a line Segment pointing down

        prim = GeomPoints(Geom.UHStatic)
        prim.add_consecutive_vertices(0,self.amntObjs)
        prim.close_primitive()

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        node = GeomNode('gnode')
        node.addGeom(geom)

        nodePath = self.render.attachNewNode(node)
        nodePath.setRenderModeThickness(5)
        return 0

    def drawLineSegments(self,points):#Point will be origin of line segments
        ls = LineSegs()

        ls.setThickness(5)
        ind = 0
        for point in points:
            #ls.setColor(self.colors[ind][0],self.colors[ind][1],self.colors[ind][1],0.7)
            #ls.moveTo(float(point[0]),float(point[1]),float(point[2]))
            #ls.drawTo(float(point[0]+self.a0[ind][0]),point[1]+float(self.a0[ind][1]),point[2]+float(self.a0[ind][2]))

            #ls.moveTo(float(point[0]),float(point[1]),float(point[2]))
            #ls.drawTo(float(point[0]+self.a1[ind][0]),point[1]+float(self.a1[ind][1]),point[2]+float(self.a1[ind][2]))

            #a2 = np.cross(self.a0[ind],self.a1[ind])
            #print("A2 is : ",a2)
            ##ls.setColor(1,0,0,0.7)
            #ls.moveTo(float(point[0]),float(point[1]),float(point[2]))
            #ls.drawTo(float(point[0]+a2[0]),point[1]+float(a2[1]),point[2]+float(a2[2]))

            #Draw th new threes
            ls.setColor(1,0,0,0.7)
            ls.moveTo(float(point[0]),float(point[1]),float(point[2]))
            ls.drawTo(float(point[0]+self.a0n[ind][0]),point[1]+float(self.a0n[ind][1]),point[2]+float(self.a0n[ind][2]))

            ls.moveTo(float(point[0]),float(point[1]),float(point[2]))
            ls.drawTo(float(point[0]+self.a1n[ind][0]),point[1]+float(self.a1n[ind][1]),point[2]+float(self.a1n[ind][2]))

            ls.moveTo(float(point[0]),float(point[1]),float(point[2]))
            ls.drawTo(float(point[0]+self.a2n[ind][0]),point[1]+float(self.a2n[ind][1]),point[2]+float(self.a2n[ind][2]))

            #ls.setColor(1,0,0,0.7)
            ind +=1

        linegeomn = ls.create(dynamic=False)# Creates a geomnode
        nodePath = self.render.attachNewNode(linegeomn)

    def getAngleBtwnVec(self, v0,v1):# Assuming 3D Vectors
        v0 = np.unit_vector(v0)
        v1 = np.unit_vector(v1)
        return np.arccos()
        #  dotProduct = sum((a*b)) for a,b in zip(v0,v1)

    def unit_vector(self,vector):
        return vector / np.linalg.norm(vector)





app = MyApp()
app.run()
