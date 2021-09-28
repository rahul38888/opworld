from ursina import *
from ursina.shaders import texture_blend_shader as shader
from ursina.scripts import generate_normals
from numpy import cross
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
window.borderless = False


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


position = (0,5,0)
vs = ((-1, -1, 1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (1, 1, 1), (-1, 1, -1), (1, -1, -1), (1, 1, -1))
ts = (0, 2, 1, 0, 3, 2, 0, 1, 3, 7, 1, 2, 7, 2, 3, 7, 3, 1)
norms = calculate_normals(vs, ts)

vs = tuple(map(lambda v: (v[0]+position[0], v[1]+position[1], v[2]+position[2]), vs))

uvs = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))


class GameEntity(Button):
    def __init__(self, **kwargs):
        super().__init__(parent=scene, model='cube', position=(0, 5, 0),
                         shader=shader, scale=(2, 2, 2), texture="crate", collider="box", color=color.white)

    def entity_input(self, key):
        if self.hovered:
            self.texture =Texture('ground')


entity = GameEntity()

ground = Entity(
    model='plane',
    collider='box',
    shader=shader,
    texture="ground",
    scale=50, x=0, y=-10, z=0
)

s = Sky(shader=shader)


def input(key):
    if key == input_handler.Keys.escape:
        application.quit()


pivot = Entity()
pivot.input = input
# AmbientLight()
# PointLight(parent=pivot, y=0, x=10, z=-10, shadows=True)
# PointLight(parent=pivot, y=0, x=-10, z=-10, shadows=True)
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

def update():
    entity.y += held_keys[input_handler.Keys.up_arrow] * .1
    entity.y -= held_keys[input_handler.Keys.down_arrow] * .1

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


def input(key):
    if key == 'space':
        entity.y += 1
        invoke(setattr, entity, 'y', entity.y - 1, delay=.25)


player = FirstPersonController()
player.position = (0, -7, 0)

if __name__ == '__main__':
    app.run()
