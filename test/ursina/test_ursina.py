import math

import screeninfo
from ursina import *
from ursina.shaders import lit_with_shadows_shader as shader
from ursina.scripts import generate_normals
from numpy import cross
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
window.borderless = False
window.fullscreen = True
camera.world_rotation = (0, 0, 0)


def plane_normal(a, b, c):
    for i in range(0, len(ts), 3):
        v1 = [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
        v2 = [a[0] - c[0], a[1] - c[1], a[2] - c[2]]
        return cross(v1, v2).data


def vector(t, f):
    return [t[0] - f[0], t[1] - f[1], t[2] - f[2]]


def calculate_normals(vertices, triangles):
    neighbor_tris = dict()
    for i in range(0, len(triangles), 3):
        if not neighbor_tris.__contains__(triangles[i]):
            neighbor_tris[triangles[i]] = []
        neighbor_tris[triangles[i]].append(i)

        if not neighbor_tris.__contains__(triangles[i + 1]):
            neighbor_tris[triangles[i + 1]] = []
        neighbor_tris[triangles[i + 1]].append(i)

        if not neighbor_tris.__contains__(triangles[i + 2]):
            neighbor_tris[triangles[i + 2]] = []
        neighbor_tris[triangles[i + 2]].append(i)

    result = list()
    for i in range(len(vertices)):
        v = vertices[i]
        if not neighbor_tris.__contains__(i):
            result.append([0, 0, 0])
            continue

        nts = neighbor_tris[i]

        sum_vect = [0, 0, 0]
        for nt in nts:
            n = plane_normal(vertices[triangles[nt]], vertices[triangles[nt + 1]], vertices[triangles[nt + 2]])
            sum_vect = [sum_vect[0] + n[0], sum_vect[1] + n[1], sum_vect[2] + n[2]]

        result.append([sum_vect[0] / len(nts), sum_vect[1] / len(nts), sum_vect[2] / len(nts)])

    return result


position = (0, 5, 0)
vs = ((-1, -1, 1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (1, 1, 1), (-1, 1, -1), (1, -1, -1), (1, 1, -1))
ts = (0, 2, 1, 0, 3, 2, 0, 1, 3, 7, 1, 2, 7, 2, 3, 7, 3, 1)
norms = calculate_normals(vs, ts)



vs = tuple(map(lambda v: (v[0] + position[0], v[1] + position[1], v[2] + position[2]), vs))

uvs = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))

game_entity_parent = Entity(parent=scene)

entities = set()


class HitObj:
    def __init__(self):
        self.models = [
            Entity(model="cube", scale=(1, 1, 1), texture='crate', shader=shader, color=color.rgba(0, 1, 0, 0.3),
                   collider=None),
            Entity(model="sphere", scale=(1, 1, 1), texture='lava', shader=shader, color=color.rgba(0, 1, 0, 0.3),
                   collider=None)]

        self.models_name = ["cube", "sphere"]

        for model in self.models:
            model.__setattr__("hit_rotation", model.rotation)
            model.disable()

        self.active = 0

    def get_model(self):
        return self.models[self.active]

    def get_model_name(self):
        return self.models_name[self.active]

    def next(self):
        self.get_model().disable()
        self.active = (self.active+1) % len(self.models)
        self.models[self.active].enable()

    def __str__(self) -> str:
        return str(self.active)

    def __repr__(self) -> str:
        return repr(self.active)


models = HitObj()


class GameEntity(Button):
    def __init__(self, position, rotation, model, texture, main=False, name=None):
        super().__init__(parent=game_entity_parent, model=model, position=position, rotation=rotation,
                         shader=shader, scale=(1, 1, 1), texture=texture,
                         collider="box", color=color.white)
        self.main = main
        self.name = "game_entity" if not name else name

    def input(self, key):
        if self.hovered:
            if key == input_handler.Keys.right_mouse_down:
                if not self.main:
                    entities.remove(self)
                    destroy(self)

    def __hash__(self):
        return hash(self.name)


# entity = GameEntity((0, 8, 0), main=True)

ground = Entity(
    model="plane",
    # model=Terrain('ground', skip=8),
    collider='mesh',
    shader=shader,
    texture="ground",
    uvs=uvs,
    scale=50,
    x=0, y=0, z=0,
    texture_scale=(25, 25)
)

s = Sky(shader=shader)


def input(key):
    global models
    if key == input_handler.Keys.escape:
        application.quit()

    if key == input_handler.Keys.left_shift:
        models.next()

    if key == input_handler.Keys.left_mouse_down:
        if mouse.world_point:
            new_entity = GameEntity(position=models.get_model().position, rotation=models.get_model().rotation,
                                    model=models.get_model_name(), texture=models.get_model().texture, name="game_entity_" + str(len(entities)))
            entities.add(new_entity)


pivot = Entity()

# AmbientLight()

# PointLight(parent=pivot, y=20, x=10, z=-10, shadows=True)
# PointLight(parent=pivot, y=10, x=-10, z=-10, shadows=True)
# PointLight(parent=pivot, y=10, x=0, z=0, shadows=True)
# PointLight(parent=pivot, y=10, x=10, z=10, shadows=True)
# DirectionalLight(parent=pivot, y=2, z=3, shadows=True)
# SpotLight(parent=pivot, y=0, x=0, z=0, rotation_x=-90)


# EditorCamera()
# camera_radius = 20
# camera.position = (camera_radius, 0, 0)
# camera_angle_x = 0
# camera_angle_y = 90
#
# camera_init = False

# camera.collider

Text.default_resolution = 1080 * Text.size
infohandler = Text(text="Starting ...", origin=(0, 15), background=False)


class Player(FirstPersonController):
    def __init__(self, position, init_health):
        super(Player, self).__init__()
        self.position = position
        self.health = init_health
        self.last_max_jump_pos = 0


player = Player(position=(0, 4, 0), init_health=51)
player.update()


def get_direction(angles: tuple):
    zh = angles[1] * math.pi / 180
    zv = angles[0] * math.pi / 180

    y = -math.sin(zv)
    x = math.cos(zv) * math.sin(zh)
    z = math.cos(zv) * math.cos(zh)

    return x, y, z


def update():
    global models
    rotation_y = models.get_model().hit_rotation[1]
    rotation_y += held_keys[input_handler.Keys.right_arrow] * 1
    rotation_y -= held_keys[input_handler.Keys.left_arrow] * 1

    models.get_model().hit_rotation = (models.get_model().hit_rotation[0], rotation_y, models.get_model().hit_rotation[2])

    # game_entity_parent.x += held_keys[input_handler.Keys.right_arrow] * .1
    # game_entity_parent.x -= held_keys[input_handler.Keys.left_arrow] * .1
    #
    # old_y = game_entity_parent.y
    # game_entity_parent.y += held_keys[input_handler.Keys.left_shift] * .1
    # game_entity_parent.y -= held_keys[input_handler.Keys.left_control] * .1

    # if entity.intersects(ground):
    #     game_entity_parent.y = old_y

    # global camera_angle_x, camera_angle_y, camera_radius, camera_init
    #
    # prev_x = camera_angle_x
    # prev_y = camera_angle_y
    # camera_angle_y += held_keys[input_handler.Keys.up_arrow] * 1
    # camera_angle_y -= held_keys[input_handler.Keys.down_arrow] * 1
    # camera_angle_x += held_keys[input_handler.Keys.right_arrow] * 1
    # camera_angle_x -= held_keys[input_handler.Keys.left_arrow] * 1
    #
    # camera_angle_x = camera_angle_x % 360
    #
    # if camera_angle_y < 1:
    #     camera_angle_y = 1
    # if camera_angle_y > 180:
    #     camera_angle_y = 180
    #
    # if prev_x != camera_angle_x or prev_y != camera_angle_y or not camera_init:
    #     camera.y = camera_radius * math.cos(math.radians(camera_angle_y))
    #     camera.x = camera_radius * math.sin(math.radians(camera_angle_y)) * math.cos(math.radians(camera_angle_x))
    #     camera.z = -camera_radius * math.sin(math.radians(camera_angle_y)) * math.sin(math.radians(camera_angle_x))
    #     print(camera_radius, camera_angle_x, camera_angle_y, camera.position)
    #     camera.look_at((0, 0, 0))
    #     camera_init = True

    # global texoffset
    # texoffset += time.dt * 0.2
    # setattr(entity, "texture_offset", (texoffset, texoffset))

    if not player.grounded:
        player.last_max_jump_pos = max(player.last_max_jump_pos, player.y)

    if player.grounded and player.last_max_jump_pos >= 5:
        damage = round(player.last_max_jump_pos - 4)
        if damage > 0:
            player.health -= damage
            player.health = max(player.health, 0)
        player.last_max_jump_pos = 0

    # origin = player.world_position + Vec3(0, 2, 0)
    # direction = get_direction(camera.world_rotation)
    # hit_info = raycast(origin, direction, ignore=(player, ), distance=10, debug=True)

    if mouse.world_point:
        models.get_model().enable()
        if mouse.hovered_entity.name.startswith("game_entity"):
            models.get_model().position = mouse.hovered_entity.world_position + mouse.world_normal.normalized()
            models.get_model().world_rotation = mouse.hovered_entity.world_rotation
        else:
            models.get_model().rotation = models.get_model().hit_rotation
            models.get_model().position = mouse.world_point + mouse.world_normal.normalized() / 2
    else:
        models.get_model().disable()

    # print(models.get_model().intersects(debug=True).entities)

    if player.y < -50:
        player.position = (0, 4, 0)

    # if hit_info.hit:
    #     print(origin, camera.world_rotation, hit_info.point)
    #
    # dir = str(("{:.2f}".format(direction[0]), "{:.2f}".format(direction[1]), "{:.2f}".format(direction[2])))
    info = "<green>Object " + \
           str(mouse.hovered_entity) + \
           "<red>Grounded " + str(player.health)
    # print(Text.get_width(info))
    infohandler.text = info


if __name__ == '__main__':
    app.run()
