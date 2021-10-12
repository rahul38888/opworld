from ursina import color, mouse

from world_entity.cube import Cube


class Dirt(Cube):
    def __init__(self,parent, position, shader):
        super(Dirt, self).__init__(parent, position, shader)
        self.name = "dirt"
        self.color = color.white
        self.texture = "stone"
        self.hits = 5

    def another(self):
        position = self.world_position + mouse.world_normal.normalized()
        Dirt(self.parent, position, self.shader)

