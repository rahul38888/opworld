from ursina import *

from app import Application

app = Application()


def input(key):
    if key == input_handler.Keys.escape:
        application.quit()


def update():
    if app.player.y < -50:
        app.player.position = (0, 4, 0)

    # app.light.position = camera.world_position


if __name__ == '__main__':
    app.run()
