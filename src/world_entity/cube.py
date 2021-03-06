from ursina import *


class Cube(Button):
    def __init__(self, parent, position, shader):
        super().__init__(parent=parent, model='cube', scale=(1, 1, 1),
                         position=position, shader=shader, collider="box")
        self.disabled = True
        # self.highlight_color = self.color
        # self.pressed_color = self.color

    def input(self, key):
        if self.hovered:
            if key == input_handler.Keys.right_mouse_down:
                destroy(self)
            if key == input_handler.Keys.left_mouse_down:
                self.another()

    def another(self):
        # has to be implemented in child
        pass

