import pyglet
import numpy as np
from pyglet.window import key

#TEST GIT PUSH

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Variables
ScreenSize = (800, 600)
game_title = "Game"
FPS = 60

#Window
window = pyglet.window.Window(ScreenSize[0], ScreenSize[1], "Game")

#Events
@window.event
def on_draw():
    window.clear

    #Square_test
    square = pyglet.shapes.Rectangle(0, 0, 50, 100, color=RED)
    square.draw()

@window.event
def update(dt):
    pass

#Run
if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()