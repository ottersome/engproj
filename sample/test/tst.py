import vtk
import argparse as ap
import sys
import pandas as pd
from panda3d.core import 


def reanderPointInSpace(pointDS):
    print("Now Rendering Object with Index: %d ..."%row['objectIndex'])
    pass

#For now lets just import our stuff
# This doesnt have to be the way but it just will for the moment.
print("Reading dataset from file: %s ..."%(sys.argv[1]))
df = pd.read_csv(sys.argv[1])
for index,row in df.iterrows():
    reanderPointInSpace(row)

#cone = vtk.vtkConeSource()
#
#mapper = vtk.vtkPolyDataMapper()
#mapper.SetInputConnection(cone.GetOutputPort())
#
#actor = vtk.vtkActor()
#actor.SetMapper(mapper)
#
#window = vtk.vtkRenderWindow()
## Sets the pixel width, length of the window.
#window.SetSize(500, 500)
#
#interactor = vtk.vtkRenderWindowInteractor()
#interactor.SetRenderWindow(window)
#
#renderer = vtk.vtkRenderer()
#window.AddRenderer(renderer)
#
#renderer.AddActor(actor)
## Setting the background to blue.
#renderer.SetBackground(0.1, 0.1, 0.4)
#
#window.Render()
#interactor.Start()

