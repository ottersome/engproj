from math import pi, sin, cos
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

#from panda3d.core import AmbientLight
#from panda3d.core import Vec4
#from panda3d.core import GeomVertexData
from panda3d.core import *

from direct.task import Task
from numpy.random import rand

import sys
import pandas as pd
import numpy as np
from panda3d.core import LineSegs
from os import listdir
from os.path import isfile, join, dirname, abspath
import modelds
import re
import mymathnutils
import argparse
from ds_object import SceneObj


loadPrcFileData("", "load-file-type p3assimp")
dirname = dirname(__file__)
dirToMappings = join(dirname, '../Dataset/Matterport/category_mapping.tsv')
dirToModels = join(dirname, '../Models/Alden/CorrectedModels/')
#  sceneDir = join(dirname, '../Dataset/Matterport/Alden/room#0_RealValues.csv')
#sceneDir = join(dirname, '../Dataset/Matterport/Alden/room#1200_RealValues.csvI')
#New format
#sceneDir = join(dirname, '../Dataset/Matterport/predictions_may26/room#1_RealValues.csv')
#Defautl rotation mode

defRotMode = 'quat'
#sceneDir = join(dirname, '../Dataset/Matterport/predictions_may26/room#1_RealValues.csv')
#sceneDir = join(dirname, '../Dataset/Matterport/3rdFormat/room#47_RealValues.csv')
sceneDir = join(dirname, '../Dataset/Newest')

parser = argparse.ArgumentParser(description='Render Results')
parser.add_argument('-f', metavar='f', type=str, nargs=1,action='store')             
parser.add_argument('-t', metavar='t', type=str, nargs=1,action='store')
parser.add_argument('-m', action='store_true')

args = parser.parse_args()
defrotMode = args.t
sceneDir = join(sceneDir, args.f[0])

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.amntObjs = 0

        #Replace this bois...
        self.colors = []# Maybe except this
        for i in range(40):
            self.colors.append([rand(),rand(),rand(),1])

        self.scnObjs = []

        self.meloader = modelds.MyLoader(self,dirToModels)
        self.linesegs = []

        self.drawAxis()
        self.loadPerSpec("/home/ottersome/Projects/EngProj/Dataset/1LXtFkjw3qLregion2.csv",
            '/home/ottersome/Projects/EngProj/Models/Alden/CorrectedModels')
        self.drawPlane()
        # self.LoadSofa()
        #self.testAxis("/home/ottersome/Projects/EngProj/Models/Alden/CorrectedModels")
        #self.drawSpherex(self.points)
        self.drawBoundingBoxes(None)
        #Need a0,a1 for this
        self.accept('h', self.hideAxis)
        self.drawLineSegments(self.scnObjs)

        #Append room name to scene dir
        base.disableMouse()
        base.camera.setPos(-2,-18,20)
        base.camera.lookAt(-2,-18,0)
        base.oobe()

        self.hidden = True


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

        models = self.meloader.loadedNodePaths
        print("Resulting Models : ",models)
        #TODO we have to handle multiple instance of the same
        #type of object
        df = pd.read_csv(sceneDir)
        objIndex =0
        for index,row in df.iterrows():
            if int(row[0]) not in mymathnutils.notgottie:
                modelo = models[objIndex]
                if modelo != None:
                    #Actually Attach to scene to render
                    #IF YOU WANT TO RENDER MODELS UNCOMMENT BELOW
                    if(args.m):
                        modelo.reparentTo(self.render)
                        modelo.setPos(row[1],row[2],row[3])

                    #Drawing Label
                    text = TextNode('Nodess')
                    textNodePath = self.render.attachNewNode(text)
                    textNodePath.setPos(row[1],row[2],row[3])
                    textNodePath.setColor(0.7,0.1,0.1,1)
                    textNodePath.setScale(0.2,0.2,0.2)
            objIndex += 1

        #Lets try loading 
    def drawBoundingBoxes(self,row):
        #self.getPoints()
        self.getPointsNQuat()

        #for point in self.points:
        counter = 0
        for scnobj in self.scnObjs:
            self.drawOBBox(scnobj)
            if counter == 15:
                break
            counter +=1 

        return 0

    def drawAxis(self):
        ls = LineSegs()
        ls.setThickness(10)

        #X axis 
        ls.setColor(1,0,0,1)
        ls.moveTo(-10,0,0)
        ls.drawTo(10,0,0)

        #Y axis 
        ls.setColor(0,1,0,1)
        ls.moveTo(0,-10,0)
        ls.drawTo(0,10,0)

        #Z axis 
        ls.setColor(0,0,1,1)
        ls.moveTo(0,0,-10)
        ls.drawTo(0,0,10)
        linegeomn = ls.create(dynamic=False)# Creates a geomnode
        nodePath = self.render.attachNewNode(linegeomn)

    def getPointsNQuat(self):
        #New format is : category, px, py, pz ,qx, qy, qz, q0, r0, r1, r2
        df = pd.read_csv(sceneDir)
        objIndex =0
        for index,row in df.iterrows():
            if int(row[0]) not in mymathnutils.notgottie:
                point=[40*row[1],40*row[2],10*row[3]]

                #Quat info 
                quat = [float(row[7]),float(row[4]),float(row[5]),float(row[6])]

                #A thingers
                #a0n = [row[8],row[9],row[10]]
                #a1n = [row[11],row[12],row[13]]
                a0n = [1,0,0]
                a1n = [0,1,0]

                print('For {:} A0 : {:}'.format(row[0],a0n))
                print('For {:} A1 : {:}'.format(row[0],a1n))

                #Radii
                radii=[row[8],row[9],row[10]]

                #  print('Sorting axis...')
                # Sort Axes:
                if(radii[1] > radii[0]):
                    swap_axis = a0n
                    swap_radii = radii[0]

                    a0n = a1n
                    radii[0] = radii[1]

                    a1n = swap_axis
                    radii[1] = swap_radii

                if(radii[2] > radii[0]):
                    swap_axis = a0n
                    swap_radii = radii[0]

                    a0n = a2n
                    radii[0] = radii[2]

                    a2n = swap_axis
                    radii[2] = swap_radii

                if(radii[2] > radii[1]):
                    swap_axis = a1n
                    swap_radii = radii[1]

                    a1n = a2n
                    radii[1] = radii[2]

                    a2n = swap_axis
                    radii[2] = swap_radii

                # No Idea why thi is idone
                a2n = np.cross(a0n,a1n)
                a2n = (a2n/np.linalg.norm(a2n))

                print("Rotation mode is : ", defRotMode)
                #Now appedn it into the scenObjs array 
                self.scnObjs.append(
                    SceneObj(pos = point,
                    quat = quat,
                    mode = defRotMode,
                    a0 = a0n,
                    a1 = a1n,
                    a2 = a2n,
                    catid = int(row[0]),
                    radius=radii))#I know radii is not the correct term, its a recycled name

                #print("Ford index : %d Coords : (%.3f,%.3f,%.3f)"%
                #    (row['objectIndex'],row['px'],row['py'],row['pz']))



    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees*(pi/180)
        self.camera.setPos(20*sin(angleRadians),-20*cos(angleRadians),10)
        self.camera.setHpr(angleDegrees,0,0)
        return Task.cont

    def drawRectangle(self, sqr,clr):
        #Square will be a list of 4 elemets. Each element being a 3 element vector
        #Square will be a list of 4 elemets. RGBA. This single 4-element value will be
            #applied to every vertex
        vdata = GeomVertexData('',GeomVertexFormat.getV3n3c4(),Geom.UHStatic)
        vertex = GeomVertexWriter(vdata,'vertex')
        color = GeomVertexWriter(vdata,'color')
        normal = GeomVertexWriter(vdata,'normal')

        for i in range(4):
            vertex.addData3f(sqr[i][0],sqr[i][1],sqr[i][2])
        for i in range(4):
            color.addData4f(clr[0],clr[1],clr[2],clr[3])

        prim = GeomTristrips(Geom.UHStatic)
        for i in range(4):
            prim.addVertex(i)
        prim.close_primitive()

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        name = 'square'+str(int(rand()))
        node = GeomNode('planeNode')
        node.addGeom(geom)

        nodePath = self.render.attachNewNode(node)
        return nodePath

    def drawBox(self, scnobj):
        #6 Of these
        rx,ry,rz = scnobj.radius
        clr = self.colors[scnobj.catid]
        r1 = self.drawRectangle(
            [[rx,ry,rz],
            [-rx,ry,rz],
            [rx,-ry,rz],
            [-rx,-ry,rz]],
            clr
            )
        r1.set_two_sided(True)
        r2 = self.drawRectangle(
            [[rx,ry,-rz],
            [-rx,ry,-rz],
            [rx,-ry,-rz],
            [-rx,-ry,-rz]],
            clr
            )
        r2.set_two_sided(True)
        r3 = self.drawRectangle(
            [[rx,ry,-rz],
            [rx,ry,rz],
            [rx,-ry,-rz],
            [rx,-ry,rz]],
            clr
            )
        r3.set_two_sided(True)
        r4 = self.drawRectangle(
            [[-rx,ry,-rz],
            [-rx,ry,rz],
            [-rx,-ry,-rz],
            [-rx,-ry,rz]],
            clr
            )
        r4.set_two_sided(True)
        r5 = self.drawRectangle(
            [[rx,ry,-rz],
            [rx,ry,rz],
            [-rx,ry,-rz],
            [-rx,ry,rz]],
            clr
            )
        r5.set_two_sided(True)
        r6 = self.drawRectangle(
            [[rx,-ry,-rz],
            [rx,-ry,rz],
            [-rx,-ry,-rz],
            [-rx,-ry,rz]],
            clr
            )
        r6.set_two_sided(True)
        popNP = NodePath('Nodepath')
        #self.render.attachNewNode(popNP)
        r1.reparentTo(popNP)
        r2.reparentTo(popNP)
        r3.reparentTo(popNP)
        r4.reparentTo(popNP)
        r5.reparentTo(popNP)
        r6.reparentTo(popNP)
        popNP.setTransparency(TransparencyAttrib.MAlpha)
        popNP.setAlphaScale(0.5)
        popNP.reparentTo(self.render)
        return popNP


    def drawPlane(self):
        vdata = GeomVertexData('',GeomVertexFormat.getV3n3c4(),Geom.UHStatic)
        vertex = GeomVertexWriter(vdata,'vertex')
        color = GeomVertexWriter(vdata,'color')
        normal = GeomVertexWriter(vdata,'normal')
        center = [0,0,0]
        halfW = 20

        #Add four points that make up a plane
        vertex.addData3f(-halfW,halfW,-5)
        color.addData4f(1,1,1,1)
        normal.addData3f(0,0,1)
        vertex.addData3f(-halfW,-halfW,-5)
        color.addData4f(1,1,1,1)
        normal.addData3f(0,0,1)
        vertex.addData3f(halfW,halfW,-5)
        color.addData4f(1,1,1,1)
        normal.addData3f(0,0,1)
        vertex.addData3f(halfW,-halfW,-5)
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

    def drawLineSegments(self,scnObjs):#Point will be origin of line segments
        ls = LineSegs()

        ls.setThickness(5)
        ind = 0
        for scnobj in scnObjs:
            point = scnobj.pos
            a0 = scnobj.a0
            a1 = scnobj.a1
            a2 = scnobj.a2

            #Draw th new threes
            ls.setColor(1,0,0,0.7)
            ls.moveTo(float(point[0]),float(point[1]),float(point[2]))
            ls.drawTo(float(point[0]+a0[0]),point[1]+float(a0[1]),point[2]+float(a0[2]))

            ls.setColor(0,1,0,0.7)
            ls.moveTo(float(point[0]),float(point[1]),float(point[2]))
            ls.drawTo(float(point[0]+a1[0]),point[1]+float(a1[1]),point[2]+float(a1[2]))

            ls.setColor(0,0,1,0.7)
            ls.moveTo(float(point[0]),float(point[1]),float(point[2]))
            ls.drawTo(float(point[0]+a2[0]),point[1]+float(a2[1]),point[2]+float(a2[2]))

            #ls.setColor(1,0,0,0.7)
            ind +=1

        linegeomn = ls.create(dynamic=False)# Creates a geomnode
        nodePath = self.render.attachNewNode(linegeomn)
        self.linesegs.append(nodePath)

    def hideAxis(self):
        if not self.hidden:
            for axis in self.linesegs:
                axis.hide()
        else:
            for axis in self.linesegs:
                axis.show()
        self.hidden = not self.hidden

    def getAngleBtwnVec(self, v0,v1):# Assuming 3D Vectors
        v0 = np.unit_vector(v0)
        v1 = np.unit_vector(v1)
        return np.arccos()
        #  dotProduct = sum((a*b)) for a,b in zip(v0,v1)

    def unit_vector(self,vector):
        return vector / np.linalg.norm(vector)
        

    def drawOBBox(self,scnObj):
        ls = LineSegs()
        x,y,z = scnObj.pos
        rx,ry,rz = scnObj.radius
        ls.setThickness(4)
        #ls.setColor(1,0.4,0.0,0.3)
        rc,gc,bc = [rand(),rand(),rand()]
        #ls.setColor(rc+0.1,gc+0.1,bc+0.1,0.3)
        nps = self.drawBox(scnObj)
        nps.setQuat(scnObj.quat)
        nps.setPos(x,y,z)

        ls.setColor(0,0,0,0.3)

        ls.moveTo(0,0,0)
        ls.drawTo(rx,ry,rz)
        ls.drawTo(rx,-ry,rz)
        ls.drawTo(-rx,-ry,rz)
        ls.drawTo(-rx,ry,rz)
        ls.drawTo(rx,ry,rz)
 
        ls.moveTo(0,0,0)
        ls.drawTo(rx,ry,-rz)
        ls.drawTo(rx,-ry,-rz)
        ls.drawTo(-rx,-ry,-rz)
        ls.drawTo(-rx,ry,-rz)
        ls.drawTo(rx,ry,-rz)

        #Done with top sides
        # Now with other sides
        ls.moveTo(rx,ry,rz)
        ls.drawTo(rx,ry,-rz)

        ls.moveTo(rx,-ry,rz)
        ls.drawTo(rx,-ry,-rz)

        ls.moveTo(-rx,-ry,rz)
        ls.drawTo(-rx,-ry,-rz)

        ls.moveTo(-rx,ry,rz)
        ls.drawTo(-rx,ry,-rz)

        linegeomn = ls.create(dynamic=False)
        np  = self.render.attachNewNode(linegeomn)
        #np.setPos(x,y,z)
        scnObj.setNodePath(np)# Rotation should occure ere, TODO but maybe it shouldnt 

#Trash
    def drawBBox(self,scnObj):
        ls = LineSegs()
        x,y,z = scnObj.pos
        rx,rz,ry = scnObj.radius
        ls.setThickness(5)
        ls.setColor(1,0.4,0.0,0.3)

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
        np  = self.render.attachNewNode(linegeomn)
        scnObj.setNodePath(np)# Rotation should occure ere, TODO but maybe it shouldnt 


    def getPoints(self):
        df = pd.read_csv(sceneDir)
        objIndex =0
        for index,row in df.iterrows():
            if int(row[0]) not in mymathnutils.notgottie:
                #print('This is it : ',int(row[0]))
                point=[row[1],row[2],row[3]]
                a0=[row[4],row[5],row[6]]
                a1=[row[7],row[8],row[9]]
                
                a0n=a0/np.linalg.norm(a0)
                a1n=a1/np.linalg.norm(a1)
                a1n = np.cross(a0n,a1n)
                a1n = np.cross(a1n,a0n)
                a1n =  (a1n/np.linalg.norm(a1n))
                a2n = np.cross(a0n,a1n)

                #Radii
                radii=[row[10],row[11],row[12]]

                #print('Sorting axis...')
                # Sort Axes:
                if(radii[1] > radii[0]):
                    swap_axis = a0n
                    swap_radii = radii[0]

                    a0n = a1n
                    radii[0] = radii[1]

                    a1n = swap_axis
                    radii[1] = swap_radii

                if(radii[2] > radii[0]):
                    swap_axis = a0n
                    swap_radii = radii[0]

                    a0n = a2n
                    radii[0] = radii[2]

                    a2n = swap_axis
                    radii[2] = swap_radii

                if(radii[2] > radii[1]):
                    swap_axis = a1n
                    swap_radii = radii[1]

                    a1n = a2n
                    radii[1] = radii[2]

                    a2n = swap_axis
                    radii[2] = swap_radii

                # No Idea why thi is idone
                a2n = np.cross(a0n,a1n)
                a2n = (a2n/np.linalg.norm(a2n))

                #Now appedn it into the scenObjs array 
                self.scnObjs.append(SceneObj(pos = point,
                    a0=a0n,a1=a1n,a2=a2n,
                    radius=radii))#I know radii is not the correct term, its a recycled name


app = MyApp()
app.run()
