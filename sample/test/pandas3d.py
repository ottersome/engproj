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

loadPrcFileData("", "load-file-type p3assimp")


class MyApp(ShowBase):

    def LoadSofa(self):
        self.scene = self.loader.loadModel("/home/ottersome/Projects/EngineeringProject/Models/sofa1.obj")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        ## Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

    def getPoints(self):
        df = pd.read_csv(sys.argv[1])
        for index,row in df.iterrows():
            self.points.append([row['px'],row['py'],row['pz']])
            #print("Ford index : %d Coords : (%.3f,%.3f,%.3f)"%
            #    (row['objectIndex'],row['px'],row['py'],row['pz']))

    def __init__(self):
        ShowBase.__init__(self)
        self.amntObjs = 0
        self.points = []

        # Load the environment model.

        #arrs = self.GeomVertexArraFormat()
        #arrs.addColumn("vertex",3,Geom.NTFloat32,Geom.CPoint)
        #forms = GeomVertexFormat()
        #forms.addArray(arrs)
        #forms = GeomVertexFormat.registerFormat(forms)
        self.getPoints()

        self.drawPlane()
        self.drawSpherex(self.points)
        self.trackball.node().setPos(0,0,100)
        #base.disableMouse()

        #ambientLight = AmbientLight("Ambient Light")
        #ambientLight.setColor(Vec4(0.1,0.1,0.1,1))
        #self.ambientLightNP = self.render.attachNewNode(ambientLight)
        #self.render.setLight(self.ambientLightNP)
        #self.camera.setPos(0,0,100)
        #self.camera.lookAt(0,0,0)
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
            color.addData4f(random(),random(),random(),1)

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
app = MyApp()
app.run()
