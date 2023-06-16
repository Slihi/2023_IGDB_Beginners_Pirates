import pyglet
from pyglet.window import key
import numpy as np

#Variables
Ship_Level = 1
Ship_Max_Level = 3
Ship_Speed = 1
Ship_Max_Speed = 5
Ship_rotation_speed = 3

ScreenSize = (800, 600)
AspectRatio = (ScreenSize[0] / ScreenSize[1])

pygl_assets = pyglet.resource.path = ['Assets']
pyglet.resource.reindex()

#Level 1 Ship, bigger resolution to reduce pixelation from improper scaling transform
Ship_bigger = pyglet.resource.image("Ship_bigger.png")

class ScreenBoi:
    def __init__(self):
        self.width = ScreenSize[0]
        self.height = ScreenSize[1]


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

        #I adjust for the slight offset of the sprite's height
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

        self.rotate(0)
        #print(self.nose_location)