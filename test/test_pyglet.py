import pyglet
from pyglet.window import key


window = pyglet.window.Window()

label = pyglet.text.Label("Hello sir")


image = pyglet.resource.image('snoovatar.png')


@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)
    label.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        print("<")
    if symbol == key.UP:
        print("^")


if __name__ == '__main__':
    pyglet.app.run()