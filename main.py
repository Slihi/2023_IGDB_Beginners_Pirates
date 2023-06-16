import pyglet
from pyglet.window import key
import numpy as np

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

Need to implement proper movement of ship with Vectors



"""
#Game modes
Main_Menu = True
Game_Mode = False

#Variables
Ship_Level = 1
Ship_Max_Level = 3
Ship_Speed = 1
Ship_Max_Speed = 5
Ship_rotation_speed = 3

#Resources
#Import Assets folder in the same directory as main.py
pygl_assets = pyglet.resource.path = ['Assets']
pyglet.resource.reindex()

#Import Images
X_Mark_Image = pyglet.resource.image("X_Mark.png")
X_Mark_Image_Sprite = pyglet.sprite.Sprite(X_Mark_Image)
Attack_Image = pyglet.resource.image("Attack_Sprite.png")
Attack_Image_Sprite = pyglet.sprite.Sprite(Attack_Image)

#Level 1 Ship, bigger resolution to reduce pixelation from improper scaling transform
Ship_bigger = pyglet.resource.image("Ship_bigger.png")

#Ocean Tiles
Ocean_Tile1 = pyglet.resource.image("Ocean1.png")

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
        self.attacking = False

    def reveal(self):
        self.visibility = True
    def hide(self):
        self.visibility = False

    def attack_mode(self):
        if self.attacking:
            self.sprite = pyglet.sprite.Sprite(Attack_Image)
            self.sprite.scale_x = self.width / self.sprite.width
            self.sprite.scale_y = self.height / self.sprite.height
            self.sprite.x = self.x
            self.sprite.y = self.y

    def move_mode(self):
        if not self.attacking:
            self.sprite = pyglet.sprite.Sprite(X_Mark_Image)
            self.sprite.scale_x = self.width / self.sprite.width
            self.sprite.scale_y = self.height / self.sprite.height
            self.sprite.x = self.x
            self.sprite.y = self.y



    def draw(self):
        if self.visibility:
            self.sprite.draw()

#As a test object
class Dot:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = RED
    def draw(self):
        dot = pyglet.shapes.Circle(self.x, self.y, self.radius, color=self.color)
        dot.draw()

class Player:
    def __init__(self):

        #sprite and dimensions
        self.nose_location = [0, 0]
        self.sprite = pyglet.sprite.Sprite(Ship_bigger)
        self.sprite.scale_x = ScreenSize[0] / (self.sprite.width * 14)
        self.sprite.scale_y = ScreenSize[1] / (self.sprite.height * 5)
        self.x = ScreenSize[0] / 2 - (self.sprite.width / 2)
        self.y = ScreenSize[1] / 2 - (self.sprite.height / 2)
        self.sprite.x = self.x
        self.sprite.y = self.y

        #attack
        self.attack_destination = (0, 0)
        self.attacking = False


        #rotation
        self.rotation = 0
        #remember that even though the sprite starts 'up', the rotation is 0,
        # so the nose is actually pointing to the right angle wise

        #Nose stuff
        self.initial_nose_angle = np.degrees(np.arctan2(self.sprite.width / 2, self.sprite.height))
        #Nose length Pythagorean Theorem
        self.nose_length = np.sqrt((self.sprite.width / 2) ** 2 + self.sprite.height ** 2)

        #Center stuff
        self.center = np.array([self.x + (self.sprite.width / 2), self.y + (self.sprite.height / 2)])
        self.initial_center_angle = np.degrees(np.arctan2(self.sprite.width / 2, self.sprite.height / 2))
        self.center_length = np.sqrt((self.sprite.width / 2) ** 2 + (self.sprite.height / 2) ** 2)

        # movement
        self.destination = (self.center[0], self.center[1])



    def draw(self):
        self.sprite.draw()

    def rotate(self, angle):
        #Sets rotation of ship and sprite
        #Angle in degrees, CW is positive
        #Let's start off and assume the angle  is less than 90 degrees
        self.sprite.rotation = angle
        self.rotation = angle
    #Returns the location of the center of the ship, based on the angle
    def center_locator(self):
        self.center_angle = -np.radians(self.initial_center_angle + self.rotation)
        self.center_location = [self.x + self.center_length * np.cos(self.center_angle + np.pi / 2),
                                    self.y + self.center_length * np.sin(self.center_angle + np.pi / 2)]
        self.center = self.center_location

    # Returns the location of the nose of the ship, based on the angle
    # Lol I have no idea how this works, but it does?
    def nose_locator(self):

        self.center_locator()

        self.nose_angle = -np.radians(self.initial_nose_angle + self.rotation)
        self.nose_location = [self.x + self.nose_length * np.cos(self.nose_angle + np.pi / 2),
                                    self.y + self.nose_length * np.sin(self.nose_angle + np.pi / 2)]
        print(self.nose_angle)

    def update(self, destination):
        self.destination = destination
        #Updates nose location
        self.nose_locator()

        #Make a vector from ship nose to destination
        direction = np.array([self.destination[0] - self.nose_location[0],
                                     self.destination[1] - self.nose_location[1]])

        # Move the ship towards the destination
        distance = np.linalg.norm(self.destination - np.array(self.center))
        if distance >= Ship_Speed:
            direction /= distance  # Normalize the direction vector
            move_vector = direction * Ship_Speed
            self.x += move_vector[0]
            self.y += move_vector[1]
            self.sprite.x = self.x
            self.sprite.y = self.y
            self.nose_location[0] += move_vector[0]
            self.nose_location[1] += move_vector[1]


        if self.attacking:
            self.attack_destination = np.array([X_Mark.x, X_Mark.y])
            attack_vector = self.attack_destination - self.center

        self.rotate(30)
        #print(self.nose_location)

#Objects
X_Mark = curser()
player = Player()
dot = Dot(100, 100, 5)

@window.event
#Resize window
def on_resize(width, height):
    global ScreenSize
    ScreenSize = (width, height)
    #Update Player dimensions and position
@window.event
def on_mouse_press(x, y, button, modifiers):
    global keys
    print(f"Mouse pressed at {x}, {y}")
    if key.LSHIFT not in keys:
    #update X_Mark
        X_Mark.attacking = False
        X_Mark.move_mode()
        X_Mark.x = x
        X_Mark.sprite.x = x - (X_Mark.width / 2)
        X_Mark.y = y
        X_Mark.sprite.y = y - (X_Mark.height / 2)
        X_Mark.reveal()



    #Set Player destination
        player.destination = (x, y)

    elif key.LSHIFT or key.RSHIFT in keys:
        if X_Mark.attacking:
            X_Mark.attacking = False
            player.attacking = False
            X_Mark.hide()
        elif not X_Mark.attacking:
            X_Mark.attacking = True
            player.attacking = True
            player.attack_destination = (x, y)
            X_Mark.reveal()
        X_Mark.attack_mode()
        X_Mark.x = x
        X_Mark.sprite.x = x - X_Mark.width / 2
        X_Mark.y = y
        X_Mark.sprite.y = y - X_Mark.height / 2





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

    #OceanFirst,Render
    Ocean_Tile1_Sprite = pyglet.sprite.Sprite(Ocean_Tile1)
    Ocean_Tile1_Sprite.scale_y = 1
    Ocean_Tile1_Sprite.scale_x = 1

    #Need to turn into a batch
    for i in range(0, int(ScreenSize[0] / Ocean_Tile1_Sprite.width) + 1):
        for j in range(0, int(ScreenSize[1] / Ocean_Tile1_Sprite.height) + 1):
            Ocean_Tile1_Sprite.x = i * Ocean_Tile1_Sprite.width
            Ocean_Tile1_Sprite.y = j * Ocean_Tile1_Sprite.height
            Ocean_Tile1_Sprite.draw()

    #Ocean_Tile1_Sprite.scale_x = ScreenSize[0] / Ocean_Tile1_Sprite.width
    #Ocean_Tile1_Sprite.scale_y = ScreenSize[1] / Ocean_Tile1_Sprite.height
    #Ocean_Tile1_Sprite.draw()

    #Square_test
    #square = pyglet.shapes.Rectangle(0, 0, 50, 100, color=TAN)
    #square.draw()

    #Ship Test
    player.draw()

    X_Mark.draw()

    #Dot Test
    player.nose_locator()
    dot = Dot(player.center[0], player.center[1], 5)
    dot.draw()




@window.event
def update(dt):
    #Update Player Movement
    player.update(player.destination)
    pass

#Run
if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()