from enum import Enum

from world_entity.blocks import *


def generate_terrain(noisemap: list, y_scale: int, terrain_levels: list, global_parent, shader):
    for z in range(len(noisemap)):
        for x in range(len(noisemap[0])):
            noise_val = noisemap[z][x]
            block_count = int(y_scale*noise_val)+1
            terrain_type: TerrainType = TerrainLevel.Water.value
            for t in terrain_levels:
                if t.threshold >= noise_val:
                    terrain_type = t
                    break

            position = (x,block_count,z)
            terrain_type.block_class(global_parent, position, shader)
            terrain_type.block_class(global_parent, (x,block_count-1,z), shader)


class TerrainType:
    def __init__(self, name: str, threshold: float, block_class):
        self.name = name
        self.threshold = threshold
        self.block_class: Cube = block_class


class TerrainLevel(Enum):
    Water = TerrainType("Water", 0.4, Water)
    Sand = TerrainType("Sand", 0.5, Sand)
    Ground = TerrainType("Ground", 0.7, Dirt)
    Hilly = TerrainType("Hilly", 0.9, Stone)
    Snowy = TerrainType("Snowy", 1.0, Snow)
