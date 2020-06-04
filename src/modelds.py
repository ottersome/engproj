from panda3d.core import NodePath
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBase import Loader as Loadies 
from os import listdir
from os.path import isfile, join
import re
import pandas as pd
import mymathnutils as mmu


class MyLoader(Loadies.Loader):
    def __init__(self,baseo,modelDir):
        print("Initializing me loadies")
        #self.loadedNodePaths = 40*[None]#This will store our models; This was for when we wanted to load only 40 of em
        self.loadedNodePaths = []#This will store individual instances per scene
        #self.mappings = pd.read_csv(mappingDir, sep='\t')
        self.nyuNames = [None]*41
        self.getModelEggNames(modelDir)
        return super().__init__(baseo)

    def scaleNP(self,nodePath):
        minLimit, maxLimit = nodePath.getTightBounds()
        dimensions = Point3(maxLimit - minLimit)
        print("Max for this boi ",maxLimit, " As for mins : ", minLimit);
        compList = [dimensions.getX(), dimensions.getY(), dimensions.getZ()]
        print("Max From list : ", max(compList));
        nodePath.setScale(1 / max(compList))

    def loadModel(self, modelPath, loaderOptions = None, noCache = None,
                  allowInstance = False, okMissing = None,
                  callback = None, extraArgs = [], priority = None,
                  blocking = None,index=None):
        print("Loading me loadiess");
        _nodePath = super().loadModel(modelPath,loaderOptions,noCache,
            allowInstance,okMissing, callback, extraArgs, priority,
            blocking)
        self.scaleNP(_nodePath)
        #Before rurning Node Path we will scale it
        return _nodePath
    def getCatIndex(self,fileName):
        result = re.findall(r'[0-9]+', fileName)
        return int(result[0])

    def getModelEggNames(self,modelDir):
        #Populate array with names
        eggfiles = [f for f in listdir(modelDir) if isfile(join(modelDir, f)) and f.endswith(".egg")]
        for f in eggfiles:
            indo = self.getCatIndex(f)
            self.nyuNames[indo] = f
        #Done

    def loadScene(self,sceneDir,modelsDir):
        df = pd.read_csv(sceneDir,delimiter=',',header=None)
        #for row in range(0,len(df.index)):
        for index, row in df.iterrows():
            #nyu40Index = int(self.mappings.iloc[int(row['categoryIndex'])]['nyu40id'])
            nyu40Index = int(row[0])
            if nyu40Index not in mmu.notgottie:
                nameOfFile = self.nyuNames[nyu40Index]
                absPathToFile  = join(modelsDir,nameOfFile)
                self.loadedNodePaths.append(self.loadModel(absPathToFile))
            else: 
                self.loadedNodePaths.append(None)

            #print("Nyu index for ",row['categoryIndex']," is : ",nyu40Index)
            #With that out of the way

        # For each row we will oad a modellinto loaded Node Paths
    def loadNYU40(self,dirPath):
        eggfiles = [f for f in listdir(dirPath) if isfile(join(dirPath, f)) and f.endswith(".egg")]
        #max length 
        for f in eggfiles:
            #TODO fix this horrid absolte path prepending
            catIndex = int(self.getCatIndex(f))
            nodePath = self.loadModel("/home/ottersome/Projects/EngProj/Models/Alden/CorrectedModels/"+f)
            self.loadedNodePaths[catIndex] = nodePath
            pass
    def returnAngles(a0,iHat,a1,jHat,a2,zHat):
        pass

