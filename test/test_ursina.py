from ursina import *
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

# entity = Entity(
#     model='cube',
#     color=color.red,
#     collider='box',
#     shader=lit_with_shadows_shader
# )

vs = ((-1, -1, 1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (1, 1, 1), (-1, 1, -1), (1, -1, -1), (1, 1, -1))
ts = (0, 2, 1,  0, 3, 2,  0, 1, 3,  7, 1, 2,  7, 2, 3,  7, 3, 1)
norms = ((0, 0, 1), (-1, 0, 0), (0, -1, 0), )
uvs = ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0), (1.0, 1.0))
entity = Entity(model=Mesh(vertices=vs, triangles=ts, uvs=uvs, mode='triangle',
                           colors=(color.red, color.red, color.red, color.red), normals=norms),
                shader=lit_with_shadows_shader, scale=(2, 2, 2))

EditorCamera()
pivot = Entity()
# AmbientLight('quad_ambient_light')
PointLight(parent=pivot, y=10, x=10, z=-10, shadows=True)

PointLight(parent=pivot, y=-10, x=-10, z=10, shadows=True)


def update():
    entity.x += held_keys['d'] * .1
    entity.x -= held_keys['a'] * .1
    entity.y += held_keys['w'] * .1
    entity.y -= held_keys['s'] * .1

    entity.rotation_x += held_keys[input_handler.Keys.up_arrow] * 1
    entity.rotation_x -= held_keys[input_handler.Keys.down_arrow] * 1
    entity.rotation_y += held_keys[input_handler.Keys.right_arrow] * 1
    entity.rotation_y -= held_keys[input_handler.Keys.left_arrow] * 1


def input(key):
    if key == 'space':
        entity.y += 1
        invoke(setattr, entity, 'y', entity.y - 1, delay=.25)


if __name__ == '__main__':
    app.run()
