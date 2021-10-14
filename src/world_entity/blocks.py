from ursina import *

from world_entity.cube import Cube


class Water(Cube):
    load_texture("water", path="water.png")

    def __init__(self, parent, position, shader):
        super(Water, self).__init__(parent, position, shader)
        self.name = "water"
        self.color = color.white
        self.texture = load_texture("water")
        self.hits = math.inf

    def another(self):
        position = self.world_position + mouse.world_normal.normalized()
        Water(self.parent, position, self.shader)


class Sand(Cube):
    texture = load_texture("sand", path="sand.png")

    def __init__(self, parent, position, shader):
        super(Sand, self).__init__(parent, position, shader)
        self.name = "sand"
        self.color = color.white
        self.texture = load_texture("sand")
        self.hits = math.inf

    def another(self):
        position = self.world_position + mouse.world_normal.normalized()
        Sand(self.parent, position, self.shader)


class Dirt(Cube):
    texture = load_texture("dirt", path="dirt.jpg")

    def __init__(self,parent, position, shader):
        super(Dirt, self).__init__(parent, position, shader)
        self.name = "dirt"
        self.color = color.white
        self.texture = load_texture("dirt")
        self.hits = 5

    def another(self):
        position = self.world_position + mouse.world_normal.normalized()
        Dirt(self.parent, position, self.shader)


class Stone(Cube):
    texture = load_texture("stone", path="stone.jpg")

    def __init__(self, parent, position, shader):
        super(Stone, self).__init__(parent, position, shader)
        self.name = "stone"
        self.color = color.white
        self.texture = load_texture("stone")
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
