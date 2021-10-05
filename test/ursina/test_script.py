from ursina import *
from ursina import scene
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

# camera.orthographic = True
camera.position = (0, 12, 0)
camera.fov = 90
camera.look_at((0, 0, 0))

# PointLight(position=camera.position)
AmbientLight()

def input(key):
    if key == Keys.escape:
        application.quit()

    changes = False
    new_pos = camera.position[1]
    if key == Keys.scroll_up:
        new_pos = new_pos+0.2
        changes = True
    if key == Keys.scroll_down:
        new_pos = new_pos-0.2
        changes = True

    if changes:
        if new_pos < 2:
            new_pos = 2
        if new_pos > 25:
            new_pos = 25
        camera.position = (0, new_pos, 0)


class Box(Button):
    def __init__(self, position, index):
        rnd = random.randint(100, 200)
        super(Box, self).__init__(parent=scene, model='cube', position=position,
                                  color=color.rgb(rnd, rnd, rnd), highlight_color=color.rgb(rnd+50, rnd+50, rnd+50))
        self.index = index
        self.selected = False

    def input(self, key):
        if self.hovered:
            if key == Keys.left_mouse_down:
                self.selected = not self.selected
                if self.selected:
                    self.color = color.white
                    self.texture = Texture("lava.jpg")
                else:
                    rnd = random.randint(100, 200)
                    self.color = color.rgb(rnd, rnd, rnd)
                    # destroy(self, 1)


size = (10, 10)
box_dist = 1.2
box_size = 1
grid_offset = (-size[0]//2*box_dist, -size[1]//2*box_dist)

grid = []
for i in range(size[1]):
    arr = []
    for j in range(size[0]):
        position = (grid_offset[0]+j*box_dist, 0, grid_offset[1]+i*box_dist)
        arr.append(Box(position=position, index=(j, i)))


if __name__ == '__main__':
    app.run()
