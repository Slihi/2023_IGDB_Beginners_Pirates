import pyglet
from pyglet.window import key
import numpy as np

#Variables
Ship_Level = 1
Ship_Max_Level = 3
Ship_Speed_portion = 8
Ship_rotation_speed = 3

ScreenSize = (800, 600)
AspectRatio = (ScreenSize[0] / ScreenSize[1])

pygl_assets = pyglet.resource.path = ['Assets']
pyglet.resource.reindex()

#Level 1 Ship, bigger resolution to reduce pixelation from improper scaling transform
Ship_bigger = pyglet.resource.image("Ship_bigger.png")

class Player:
    def __init__(self, initial_x, initial_y):

        #window stuff
        self.screen_width = ScreenSize[0]
        self.screen_height = ScreenSize[1]


        #sprite and dimensions
        self.nose_location = [0, 0]
        self.sprite = pyglet.sprite.Sprite(Ship_bigger)

        #Scale the sprite
        self.sprite.scale_x = self.screen_width / (self.sprite.width * 14)
        self.sprite.scale_y = self.screen_height / (self.sprite.height * 5)
        self.scale_ratio = self.sprite.scale_x / self.sprite.scale_y

        self.x = initial_x
        self.y = initial_y
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
        #Calculating speed based on a distance per second along the diagonal of the screen
        self.speed = np.sqrt(self.screen_width**2 + self.screen_height**2) / (Ship_Speed_portion * 60)

    def set_sprite_scale(self, width, height):

        screen_dimensions_before = (self.screen_width, self.screen_height)

        self.screen_height = height
        self.screen_width = width

        #Scale the sprite
        scale_x_ratio = self.screen_width / screen_dimensions_before[0]
        self.sprite.scale_x *= scale_x_ratio
        #Makes it look better, but doesn't work for extremely wide screens
        # as ship huge and field small
        self.sprite.scale_y *= scale_x_ratio

        #Recalculate ship position based on new screen size
        self.x = self.screen_width / screen_dimensions_before[0] * self.x
        self.y = self.screen_height / screen_dimensions_before[1] * self.y
        self.sprite.x = self.x
        self.sprite.y = self.y

        #Recalculate speed, not working
        self.speed = np.sqrt(self.screen_width**2 + self.screen_height**2) / (Ship_Speed_portion * 60)

        #Recalculate center and nose
        self.nose_locator()

        #print(f"nose location: {self.nose_location}")

    def draw(self):
        self.sprite.draw()


    #Returns the location of the center of the ship, based on the angle
    def center_locator(self):

        self.center_angle = -np.radians(self.initial_center_angle + self.rotation)
        self.center_length = np.sqrt((self.sprite.width / 2) ** 2 + (self.sprite.height / 2) ** 2)

        #I adjust for the slight offset of the sprite's height
        self.center = [self.x + self.center_length * np.cos(self.center_angle + np.pi / 2),
                                    self.y + self.center_length * np.sin(self.center_angle + np.pi / 2)]

    # Returns the location of the nose of the ship, based on the angle
    # Lol I have no idea how this works, but it does?
    # It also has center locator in it
    def nose_locator(self):

        self.center_locator()

        self.nose_length = np.sqrt((self.sprite.width / 2) ** 2 + self.sprite.height ** 2)
        self.nose_angle = -np.radians(self.initial_nose_angle + self.rotation)
        self.nose_location = [self.x + self.nose_length * np.cos(self.nose_angle + np.pi / 2),
                                    self.y + self.nose_length * np.sin(self.nose_angle + np.pi / 2)]

    def rotate_CW(self):
        #LAST ATTEMPT/METHOD TO ROTATE THE SHIP (Lol why is everything in pyglet broken)
        #I am going to pretend that it rotates by eye.

        angle = 260/60
        self.move_left()
        self.move_left()
        self.move_forward()
        self.sprite.rotation += angle
        self.rotation += angle

        #lol, wow, this is so broken but I guess it works

    def rotate_CCW(self):

        angle = 260/60
        self.move_right()
        self.move_right()
        self.move_backward()
        self.sprite.rotation -= angle
        self.rotation -= angle




    #Move only based on where the ship is facing
        pass
    def move_forward(self):
        self.nose_locator()

        ship_direction = np.array([self.nose_location[0] - self.center[0],
                                    self.nose_location[1] - self.center[1]])
        ship_direction /= np.linalg.norm(ship_direction)
        move_vector = ship_direction * self.speed

        #Move the ship
        self.x += move_vector[0]
        self.y += move_vector[1]
        self.sprite.x = self.x
        self.sprite.y = self.y

    def move_backward(self):
        self.nose_locator()

        ship_direction = np.array([self.nose_location[0] - self.center[0],
                                   self.nose_location[1] - self.center[1]])
        ship_direction /= np.linalg.norm(ship_direction)
        move_vector = ship_direction * self.speed

        # Move the ship
        self.x -= move_vector[0]
        self.y -= move_vector[1]
        self.sprite.x = self.x
        self.sprite.y = self.y

    def move_left(self):
        self.nose_locator()

        ship_direction = np.array([self.nose_location[0] - self.center[0],
                                   self.nose_location[1] - self.center[1]])
        ship_direction /= np.linalg.norm(ship_direction)
        move_vector = ship_direction * self.speed

        # Move the ship
        self.x -= move_vector[1]
        self.y += move_vector[0]
        self.sprite.x = self.x
        self.sprite.y = self.y
    def move_right(self):
        self.nose_locator()

        ship_direction = np.array([self.nose_location[0] - self.center[0],
                                   self.nose_location[1] - self.center[1]])
        ship_direction /= np.linalg.norm(ship_direction)
        move_vector = ship_direction * self.speed

        # Move the ship
        self.x += move_vector[1]
        self.y -= move_vector[0]
        self.sprite.x = self.x
        self.sprite.y = self.y

    def update(self, destination):

        self.nose_locator()
        self.rotate_CW()
        #print(f"Ship x and y: {self.x}, {self.y}, Sprite x and y: {self.sprite.x}, {self.sprite.y}")

        #self.move_forward()