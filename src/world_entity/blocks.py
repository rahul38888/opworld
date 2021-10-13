from ursina import *

from world_entity.cube import Cube


class Water(Cube):
    def __init__(self,parent, position, shader):
        super(Water, self).__init__(parent, position, shader)
        self.name = "water"
        self.color = color.white
        self.texture = "water"
        self.hits = math.inf

    def another(self):
        position = self.world_position + mouse.world_normal.normalized()
        Water(self.parent, position, self.shader)


class Sand(Cube):
    def __init__(self,parent, position, shader):
        super(Sand, self).__init__(parent, position, shader)
        self.name = "sand"
        self.color = color.white
        self.texture = "sand"
        self.hits = math.inf

    def another(self):
        position = self.world_position + mouse.world_normal.normalized()
        Sand(self.parent, position, self.shader)


class Dirt(Cube):
    def __init__(self,parent, position, shader):
        super(Dirt, self).__init__(parent, position, shader)
        self.name = "dirt"
        self.color = color.white
        self.texture = "dirt"
        self.hits = 5

    def another(self):
        position = self.world_position + mouse.world_normal.normalized()
        Dirt(self.parent, position, self.shader)


class Stone(Cube):
    def __init__(self,parent, position, shader):
        super(Stone, self).__init__(parent, position, shader)
        self.name = "stone"
        self.color = color.white
        self.texture = "stone"
        self.hits = 7

    def another(self):
        position = self.world_position + mouse.world_normal.normalized()
        Stone(self.parent, position, self.shader)


class Snow(Cube):
    def __init__(self,parent, position, shader):
        super(Snow, self).__init__(parent, position, shader)
        self.name = "snow"
        self.color = color.white
        self.texture = "snow"
        self.hits = math.inf

    def another(self):
        position = self.world_position + mouse.world_normal.normalized()
        Snow(self.parent, position, self.shader)
