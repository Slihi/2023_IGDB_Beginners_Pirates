import pyglet
import numpy as np
from pyglet.window import key

#TEST GIT PUSH
"""
IGDB Game Jam 2023
Theme: "Pirates"

Starting Ideas:
Player can move ship around by clicking on the screen


"""
#Resources
#Import Assets folder in the same directory as main.py
pygl_assets = pyglet.resource.path = ['Assets']

#Import Images
pyglet.resource.reindex()
X_Mark_Image = pyglet.resource.image("X_Mark.png")

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TAN = (210, 180, 140)

#Variables
ScreenSize = (800, 600)
game_title = "Game"
FPS = 60

#Window
window = pyglet.window.Window(ScreenSize[0], ScreenSize[1], "Game")

#Keys
keys = set()

class curser:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 10
        self.height = 10
        self.color = RED
        self.visibility = False
        self.image = X_Mark_Image
    def reveal(self):
        self.visibility = True
    def hide(self):
        self.visibility = False

    def draw(self):
        if self.visibility:
            self.image.blit(self.x, self.y)

#Objects
X_Mark = curser()

@window.event
def on_mouse_press(x, y, button, modifiers):
    print(f"Mouse pressed at {x}, {y}")
    X_Mark.x = x
    X_Mark.y = y
    X_Mark.reveal()

@window.event
def on_key_press(symbol, modifiers):
    keys.add(symbol)
    if symbol == key.ESCAPE:
        window.close()
@window.event
def on_key_release(symbol, modifiers):
    keys.remove(symbol)

@window.event
def on_draw():
    window.clear()

    #Square_test
    square = pyglet.shapes.Rectangle(0, 0, 50, 100, color=TAN)
    square.draw()

    #Curser/ X_Mark
    X_Mark.draw()

@window.event
def update(dt):
    pass

#Run
if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()