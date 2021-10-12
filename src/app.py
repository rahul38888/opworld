from ursina import *
from ursina.shaders import basic_lighting_shader as shdr

from world_entity.blocks import Dirt
from world_entity.player import Player


class Application(Ursina):
    def __init__(self, camera_world_rotation=(0, 0, 0)):
        super(Application, self).__init__()

        window.borderless = False
        window.fullscreen = True

        self.light = AmbientLight()
        self.sky = Sky(shader=shdr)
        self.global_parent = Entity(parent=scene)

        self.generate_land((10, 10))

        self.player = Player(position=(1, 10, 1), init_health=50)
        self.player.update()
        camera.world_rotation = camera_world_rotation

    def generate_land(self, dimension: tuple):
        for i in range(dimension[1]):
            for j in range(dimension[0]):
                Dirt(position=(i, 0, j), parent=self.global_parent, shader=shdr)

    def input(self, key):
        if key == input_handler.Keys.escape:
            application.quit()

    def update(self):
        if self.player.y < -50:
            self.player.position = (0, 4, 0)

