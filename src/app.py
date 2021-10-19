from ursina import *
from ursina.shaders import basic_lighting_shader as shdr

from world_entity.blocks import *
from world_entity.player import Player
from worldgen.noise import Noise
from worldgen.terrain_gen import generate_terrain, TerrainLevel


class Application(Ursina):
    def __init__(self, camera_world_rotation=(0, 0, 0)):
        super(Application, self).__init__()

        window.borderless = False
        window.fullscreen = True

        self.sky = Sky(shader=shdr)
        self.global_parent = Entity(parent=scene)

        self.terrain_levels = [TerrainLevel.Water.value, TerrainLevel.Sand.value, TerrainLevel.Ground.value,
                               TerrainLevel.Hilly.value, TerrainLevel.Snowy.value]
        self.generate_land((50, 50))

        self.player = Player(position=(1, 100, 1), init_health=50)
        self.light = PointLight(position=(0, 5, 0), parent=self.player)
        self.player.update()
        camera.world_rotation = camera_world_rotation

    def generate_land(self, dimension: tuple):
        noise_map = Noise.noise_map(size=dimension, seed=1, octaves=3, scale=((dimension[0]+dimension[1])//2))
        generate_terrain(noise_map, 10, self.terrain_levels, self.global_parent, shdr)
