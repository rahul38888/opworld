import math

from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from direct.task import Task


class App(ShowBase):
    def __init__(self):
        super(App, self).__init__()

        # self.scene = self.loader.loadModel("ground.blend")
        # self.scene.reparentTo(self.render)
        # self.scene.setScale(10, 10, 10)
        # self.scene.setPos(-8, 42, 0)

        # self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        self.actor = Actor("monkey.blend")
        self.actor.setScale(5, 5, 5)
        # self.actor.setPos(0, 0, 1)
        self.actor.reparentTo(self.render)

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * math.pi/180
        self.camera.setPos(20*math.sin(angleRadians), -20*math.cos(angleRadians), 10)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


app = App()

if __name__ == '__main__':
    app.run()
