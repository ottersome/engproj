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
from os import listdir
from os.path import isfile, join, dirname, abspath
import modelds
import re


loadPrcFileData("", "load-file-type p3assimp")
dirname = dirname(__file__)
dirToMappings = join(dirname, '../Dataset/Matterport/category_mapping.tsv')
dirToModels = join(dirname, '../Models/Alden/CorrectedModels/')
sceneDir = join(dirname, '../Dataset/Matterport/Alden/room#0_RealValues.csv')

class MyApp(ShowBase):

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
        self.radii = []

        self.meloader = modelds.MyLoader(self,dirToModels)

        self.loadPerSpec("/home/ottersome/Projects/EngProj/Dataset/1LXtFkjw3qLregion2.csv",
            '/home/ottersome/Projects/EngProj/Models/Alden/CorrectedModels')
        self.drawPlane()
        # self.LoadSofa()
        #self.testAxis("/home/ottersome/Projects/EngProj/Models/Alden/CorrectedModels")
        #self.drawSpherex(self.points)
        self.drawBoundingBoxes(None)
        self.drawLineSegments(self.points)
        base.disableMouse()
        base.camera.setPos(-2,-18,20)
        base.camera.lookAt(-2,-18,0)
        base.oobe()

        #plight = PointLight('plight')
        #plight.setColor((0.9, 0.9, 0.9, 1))
        #plnp = render.attachNewNode(plight)
        #plnp.setPos(0, 0, 1)
        #render.setLight(plnp)
        #  ambientLight = AmbientLight("Ambient Light")
        #  ambientLight.setColor(Vec4(0.1,0.1,0.1,1))
        #  self.ambientLightNP = self.render.attachNewNode(ambientLight)
        #  self.render.setLight(self.ambientLightNP)
        #self.taskMgr.add(self.spinCameraTask,"SpinCameraTask")

    def testAxis(self, path):
        # Get files from give directory
        eggfiles = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".egg")]
        #max length 
        xPos = -20
        yPos = -20
        for f in eggfiles:
            print("Testing ", f)
            #obj = self.loader.loadModel("/home/ottersome/Projects/EngProj/Models/Alden/CorrectedModels/"+f)
            obj = self.meloader.loadModel("/home/ottersome/Projects/EngProj/Models/Alden/CorrectedModels/"+f)
            # Reparent the model to render.
            obj.reparentTo(self.render)
            ## Apply scale and position transforms on the model.
            obj.setPos(xPos, yPos, 2)
            print("Setting at pos",xPos,",",yPos)
            xPos += 3
            plight = PointLight('estapos')
            plight.setColor((0.9, 0.9, 0.9, 1))
            plnp = self.render.attachNewNode(plight)
            plnp.setPos(xPos, yPos, 0.5)
            self.render.setLight(plnp)
            if xPos > 20:
                xPos = -20
                yPos += 5


    # Function in charge of loading a single room 
    def loadPerSpec(self,datasetPath,nyuLoadedModels):
        #Load this two 
        #self.meloader.loadNYU40(nyuLoadedModels)
        self.meloader.loadScene(abspath(sceneDir),abspath(dirToModels))
        #self.getPoints()

        models = self.meloader.loadedNodePaths
        print("Resulting Models : ",models)

        #TODO we have to handle multiple instance of the same
        #type of object
        df = pd.read_csv(sceneDir)
        objIndex =0
        for index,row in df.iterrows():
            modelo = models[objIndex]
            if modelo != None:
                #Actually Attach to scene to render
                print("Rendering : ",modelo, ' at : {:2.2} {:2.2} {:2.2}'.format(row[1],row[2],row[3]))
                print("\twith a0 : ",' at : {:2.2} {:2.2} {:2.2}'.format(row[4],row[5],row[6]))
                print("\twith a1 : ",' at : {:2.2} {:2.2} {:2.2}'.format(row[7],row[8],row[9]))
                modelo.reparentTo(self.render)
                #modelo.setPos(row[1],row[2],row[3])

                #Drawing Label
                text = TextNode('Nodess')
                text.setText('Esta')
                textNodePath = self.render.attachNewNode(text)
                textNodePath.setPos(row[1],row[2],row[3])
                textNodePath.setColor(0.7,0.1,0.1,1)
                textNodePath.setScale(0.2,0.2,0.2)
            objIndex += 1

        #Lets try loading 
    def drawBoundingBoxes(self,row):
        self.getPoints()
        # Let this be similar to the axis thingy
        vdata = GeomVertexData('',GeomVertexFormat.getV3c4(),Geom.UHStatic)
        vertex = GeomVertexWriter(vdata,'vertex')
        color = GeomVertexWriter(vdata,'color')
        counter = 0

        for point in self.points:
            self.amntObjs = self.amntObjs +1
            vertex.addData3f(point[0],point[1],point[2])
            self.colors.append([random(),random(),random()])
            color.addData4f(self.colors[-1][0],self.colors[-1][1],self.colors[-1][0],1)

            #Actual BBox
            self.drawBBox(point,self.a0n[counter],self.a0n[counter],self.radii[counter])
            counter +=1

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


    def getPoints(self):
        self.notgottie = [2,22,38,39,40]
        df = pd.read_csv(sceneDir)
        objIndex =0
        for index,row in df.iterrows():
            if row[0] not in self.notgottie:
                self.points.append([row[1],row[2],row[3]])
                self.a0.append([row[4],row[5],row[6]]);
                self.a1.append([row[7],row[8],row[9]]);
                
                self.a0n.append(self.a0[-1]/np.linalg.norm(self.a0[-1]))
                self.a1n.append(self.a1[-1]/np.linalg.norm(self.a1[-1]))
                self.a1n[-1]  = np.cross(self.a0n[-1],self.a1n[-1])
                self.a1n[-1]  = np.cross(self.a1n[-1],self.a0n[-1])
                self.a1n[-1] =  (self.a1n[-1]/np.linalg.norm(self.a1n[-1]))
                self.a2n.append(np.cross(self.a0n[-1],self.a1n[-1]));

                #Radii
                self.radii.append([row[10],row[11],row[12]]);

                #print("Ford index : %d Coords : (%.3f,%.3f,%.3f)"%
                #    (row['objectIndex'],row['px'],row['py'],row['pz']))


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

            #Draw th new threes
            ls.setColor(1,0,0,0.7)
            ls.moveTo(float(point[0]),float(point[1]),float(point[2]))
            ls.drawTo(float(point[0]+self.a0n[ind][0]),point[1]+float(self.a0n[ind][1]),point[2]+float(self.a0n[ind][2]))

            ls.moveTo(float(point[0]),float(point[1]),float(point[2]))
            ls.drawTo(float(point[0]+self.a1n[ind][0]),point[1]+float(self.a1n[ind][1]),point[2]+float(self.a1n[ind][2]))

            #ls.moveTo(float(point[0]),float(point[1]),float(point[2]))
            #ls.drawTo(float(point[0]+self.a2n[ind][0]),point[1]+float(self.a2n[ind][1]),point[2]+float(self.a2n[ind][2]))

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
        
    def drawBBox(self,pos,a0,a1,radius):
        ls = LineSegs()
        x,y,z = pos
        #xangle = self.getAngleBtwnVec([])
        rx,ry,rz = radius
        ls.setThickness(5)
        ls.setColor(0.2,1,0.2,1)

        ls.moveTo(x,y,z)
        ls.drawTo(x+rx,y+ry,z+rz)
        ls.drawTo(x+rx,y-ry,z+rz)
        ls.drawTo(x-rx,y-ry,z+rz)
        ls.drawTo(x-rx,y+ry,z+rz)
        ls.drawTo(x+rx,y+ry,z+rz)
 
        ls.moveTo(x,y,z)
        ls.drawTo(x+rx,y+ry,z-rz)
        ls.drawTo(x+rx,y-ry,z-rz)
        ls.drawTo(x-rx,y-ry,z-rz)
        ls.drawTo(x-rx,y+ry,z-rz)
        ls.drawTo(x+rx,y+ry,z-rz)

        linegeomn = ls.create(dynamic=False)
        self.render.attachNewNode(linegeomn)


        

app = MyApp()
app.run()
