import pyglet
from pyglet.window import key

#TEST GIT PUSH
"""
IGDB Game Jam 2023
Theme: "Pirates"

Starting Ideas:
Player can move ship around by clicking on the screen
Player can shoot cannon balls at other ships
Player can upgrade level of ship by capture other ships (up to 3)
Getting hit loses a level of ship
Player can go collect resources from islands (gold)
If you have enough gold, you win the game
Other ships trying to stop you.



"""
#Game modes
Main_Menu = True
Game_Mode = False

#Resources
#Import Assets folder in the same directory as main.py
pygl_assets = pyglet.resource.path = ['Assets']
pyglet.resource.reindex()

#Import Images
X_Mark_Image = pyglet.resource.image("X_Mark.png")
X_Mark_Image_Sprite = pyglet.sprite.Sprite(X_Mark_Image)
#Level 1 Ship, bigger resolution to reduce pixelation from improper scaling transform
Ship_bigger = pyglet.resource.image("Ship_bigger.png")

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TAN = (210, 180, 140)

#Variables
ScreenSize = (800, 600)
AspectRatio = (ScreenSize[0] / ScreenSize[1])
game_title = "Game"
FPS = 60

#Window
window = pyglet.window.Window(ScreenSize[0], ScreenSize[1], game_title, resizable=True)

#Keys
keys = set()

class curser:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = int(ScreenSize[0] / 32)
        self.height = int(ScreenSize[1] / 24)
        self.color = RED
        self.visibility = False
        self.sprite = pyglet.sprite.Sprite(X_Mark_Image)
        self.sprite.scale_x = self.width / self.sprite.width
        self.sprite.scale_y = self.height / self.sprite.height
        self.sprite.x = self.x
        self.sprite.y = self.y
    def reveal(self):
        self.visibility = True
    def hide(self):
        self.visibility = False

    def draw(self):
        if self.visibility:
            self.sprite.draw()

class Player:
    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(Ship_bigger)
        self.sprite.scale_x = ScreenSize[0] / (self.sprite.width * 14)
        self.sprite.scale_y = ScreenSize[1] / (self.sprite.height * 5)
        self.x = ScreenSize[0] / 2 - (self.sprite.width / 2)
        self.y = ScreenSize[1] / 2 - (self.sprite.height / 2)
        self.sprite.x = self.x
        self.sprite.y = self.y

    def draw(self):
        self.sprite.draw()


#Objects
X_Mark = curser()
player = Player()

@window.event
#Resize window
def on_resize(width, height):
    global ScreenSize
    ScreenSize = (width, height)
    #Update Player dimensions and position
@window.event
def on_mouse_press(x, y, button, modifiers):
    print(f"Mouse pressed at {x}, {y}")

    #update X_Mark
    X_Mark.x = x
    X_Mark.sprite.x = x - (X_Mark.width / 2)
    X_Mark.y = y
    X_Mark.sprite.y = y - (X_Mark.height / 2)
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
    #square = pyglet.shapes.Rectangle(0, 0, 50, 100, color=TAN)
    #square.draw()

    #Ship Test
    player.draw()

    X_Mark.draw()


@window.event
def update(dt):
    pass

#Run
if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()