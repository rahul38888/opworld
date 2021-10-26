from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from worldgen.noise import Noise
from enum import Enum


def get_mesh_data(heightmap: list, texture_scale: float, y_scale: float, terrain_levels: list):
    vertices = []
    uvs = []
    triangles = []

    def v_index(x_cord, z_cord):
        return len(heightmap[0]) *z_cord + x_cord

    uv_increment = 1/ (texture_scale * (len(heightmap[0]) - 1))
    uv_x, uv_z = 0, 0

    max_water = -math.inf
    min_water = math.inf
    for z in range(len(heightmap)):
        for x in range(len(heightmap[0])):
            if heightmap[z][x] <= TerrainLevel.Water.value.threshold:
                max_water = max(max_water, heightmap[z][x])
                min_water = min(min_water, heightmap[z][x])

    wc: Color = TerrainLevel.Water.value.color
    water_color = color.rgba(wc.r, wc.g, wc.b,0.5)
    water = Entity(model="plane", color=water_color)

    for z in range(len(heightmap)):
        for x in range(len(heightmap[0])):
            terrain = None
            for t in terrain_levels:
                if heightmap[z][x] <= t.threshold:
                    terrain = t
                    break

            # noise_val = heightmap[z][x] + max_water*y_scale if terrain and terrain.level_region else heightmap[z][x]*y_scale
            noise_val = heightmap[z][x]*y_scale
            vertices.append((x, noise_val, z))
            uvs.append((uv_x, uv_z))
            uv_x += uv_increment
            uv_z += uv_increment

            if x is len(heightmap[0]) - 1 or z is len(heightmap) - 1:
                continue

            triangles.append(v_index(x, z))
            triangles.append(v_index(x + 1, z + 1))
            triangles.append(v_index(x, z + 1))

            triangles.append(v_index(x + 1, z + 1))
            triangles.append(v_index(x, z))
            triangles.append(v_index(x + 1, z))

    return vertices, triangles, uvs


def get_colors(heightmap, terrain_levels):
    colors = []
    for z in range(len(heightmap)):
        for x in range(len(heightmap[0])):
            terrain = None
            for t in terrain_levels:
                if heightmap[z][x] < t.threshold:
                    terrain = t
                    break

            colors.append(terrain.color if terrain is not None else TerrainLevel.Ground.value.color)

    return colors


def generate_terrain(heightmap: list, y_scale: int, terrain_levels: list, global_parent, shader, grid_pos: tuple,
                     texture_scale: float = 1.0):
    vertices, triangles, uvs = get_mesh_data(heightmap, texture_scale, y_scale, terrain_levels)
    colors = get_colors(heightmap, terrain_levels)

    position = (grid_pos[0] + (len(heightmap[0])-1)//2, grid_pos[1], grid_pos[2] + (len(heightmap)-1)//2)
    model = Mesh(vertices=vertices, triangles=triangles, uvs=uvs, colors=colors)
    model.generate_normals(smooth=True)
    mesh = Entity(model=model, collider="mesh", position=position)

    return mesh


def get_player_position(heightmap, x, z):
    hit_info = raycast((x,100, z) , (0,-1,0), debug=True)
    print(hit_info.world_point)
    return (x, hit_info.world_point[1]+3, z)


class TerrainType:
    def __init__(self, name: str, threshold: float, color: tuple, level_region: bool = False):
        self.name = name
        self.threshold = threshold
        self.color = color
        self.level_region = level_region


class TerrainLevel(Enum):
    Water = TerrainType("Water", 0.4, color.rgba(87, 182, 255), True)
    Sand = TerrainType("Sand", 0.5, color.rgba(194, 178, 128))
    Ground = TerrainType("Ground", 0.7, color.rgba(132, 194, 93))
    Hilly = TerrainType("Hilly", 0.9, color.rgba(159, 148, 132))
    Snowy = TerrainType("Snowy", 1.0, color.rgba(245, 252, 255))


if __name__ == '__main__':
    from ursina import *
    from ursina.shaders import basic_lighting_shader as shdr
    import math

    def input(key):
        if key == input_handler.Keys.escape:
            application.quit()

    app = Ursina()

    size = 100
    d = 2
    def height_val(i,j):
        return math.exp(-(i*i+j*j)/(2*d*d))

    y_scale = 20
    terrain_levels = [TerrainLevel.Water.value, TerrainLevel.Sand.value, TerrainLevel.Ground.value,
    TerrainLevel.Hilly.value, TerrainLevel.Snowy.value]
    heightmap = Noise.noise_map((size,size), seed=1, octaves=3, scale=((size+size)//2))
    mesh = generate_terrain(heightmap=heightmap, y_scale=y_scale, terrain_levels=terrain_levels, global_parent=scene,
                            shader=shdr, texture_scale=1.0, grid_pos=(0,0, 0))

    player = FirstPersonController()

    player.position = get_player_position(heightmap, 0,0)

    # AmbientLight()
    PointLight(position=(20, 50, 20), parent=scene)

    app.run()