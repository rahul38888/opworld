from ursina import *


class Inventory(Entity):
    def __init__(self, capacity):
        super(Inventory, self).__init__(
            parent=camera.ui, model='quad',
            origin=(-0.5, 0.5), texture="white_cube",
            color=color.dark_gray
        )
        self.capacity = capacity
        self.scale=(capacity/10, 0.1)
        self.position=(-capacity/20, -0.35)
        self.texture_scale= (capacity, 1)

        self.item_parent = Entity(parent=self, scale=(1/capacity, 1))
        self.spots = [None for i in range(capacity)]

    def next_slot(self) -> int:
        for i in range(self.capacity):
            if self.spots[i] is None:
                return i

        return -1

    def append(self, index: int=-1):
        spot = index if index>=0 else self.next_slot()
        if spot >= 0:
            item = Button(parent=self.item_parent, model = "quad", color=color.random_color(),
               position=(spot, 0), origin=(-0.5, 0.5))
            self.spots[spot] = item


def input(key):
    if key == input_handler.Keys.escape:
        application.quit()


if __name__ == '__main__':
    app = Ursina()
    window.fullscreen = True
    inventory = Inventory(8)
    inventory.append(0)
    inventory.append(1)
    app.run()