import pyglet
from pyglet.window import key
import numpy as np

#Variables
Ship_Level = 1
Ship_Max_Level = 3
Ship_Speed = 0
Ship_Max_Speed = 5
Ship_rotation_speed = 3

ScreenSize = (800, 600)
AspectRatio = (ScreenSize[0] / ScreenSize[1])

pygl_assets = pyglet.resource.path = ['Assets']
pyglet.resource.reindex()

#Level 1 Ship, bigger resolution to reduce pixelation from improper scaling transform
Ship_bigger = pyglet.resource.image("Ship_bigger.png")

class Player:
    def __init__(self):

        #window stuff
        self.screen_width = ScreenSize[0]
        self.screen_height = ScreenSize[1]


        #sprite and dimensions
        self.nose_location = [0, 0]
        self.sprite = pyglet.sprite.Sprite(Ship_bigger)
        self.sprite.scale_x = self.screen_width / (self.sprite.width * 14)
        self.sprite.scale_y = self.screen_height / (self.sprite.height * 5)
        self.scale_ratio = self.sprite.scale_x / self.sprite.scale_y
        self.x = self.screen_width / 2 - (self.sprite.width / 2)
        self.y = self.screen_height / 2 - (self.sprite.height / 2)
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
        self.x = self.screen_width / 2 - (self.sprite.width / 2)
        self.y = self.screen_height / 2 - (self.sprite.height / 2)
        self.sprite.x = self.x
        self.sprite.y = self.y

        #Recalculate center and nose
        self.nose_locator()

        print(f"nose location: {self.nose_location}")

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

    def rotate(self, angle):
        # Sets rotation of ship and sprite
        # Angle in degrees, CW is positive
        self.sprite.rotation = angle
        self.rotation = angle

        self.nose_locator()

        relative_coordinates = np.array([self.nose_location[0] - self.center[0], self.nose_location[1] - self.center[1]])

        rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                                    [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])

        rotated_coordinates = np.dot(rotation_matrix, relative_coordinates)

        self.sprite.x = self.center[0] + rotated_coordinates[0]
        self.sprite.y = self.center[1] + rotated_coordinates[1]

    #Move only based on where the ship is facing
    def move_forward(self):
        self.nose_locator()

        ship_direction = np.array([self.nose_location[0] - self.center[0],
                                    self.nose_location[1] - self.center[1]])
        ship_direction /= np.linalg.norm(ship_direction)
        move_vector = ship_direction * (Ship_Speed * self.sprite.scale_x * self.screen_width / self.sprite.width)

        #Move the ship
        self.x += move_vector[0]
        self.y += move_vector[1]
        self.sprite.x = self.x
        self.sprite.y = self.y


    def update(self, destination):
        """
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

        """
        self.rotate(60)
        self.move_forward()

        #print(self.nose_location)