from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        #Load enviro model
        self.scene = self.loader.loadModel("/home/ottersome/Projects/EngProj/Models/sofa1.obj")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25,0.25,0.25)
        self.scene.setPos(-8,42,0)

app = MyApp()
app.run()
