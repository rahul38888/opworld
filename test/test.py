from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader as shader

app = Ursina()
window.fullscreen = True


def input(key):
    if key == Keys.escape:
        application.quit()


Sky()

AmbientLight()

ground = Entity(model="plane", scale=20, color=color.green, shader=shader, collider="mesh")

player = FirstPersonController(position=(0, 3, 0))

if __name__ == '__main__':
    app.run()
