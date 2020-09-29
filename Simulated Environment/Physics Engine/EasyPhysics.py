"""
High Level Physics Interface Meant To Be Used By The Environment Itself
"""

__author__ = "Will Richards"
__copyright__ = "Copyright 2020, AEMBOT"

import math
import pymunk
import arcade
from LowLevelPhysics import *

# Gravity to be used in the simulated environment, its None because dampening is used to regulate object speed
GRAVITY = (0, 0)


class PhysicsEnvironment:

    def __init__(self, window_width, window_height, simulation_accuracy, step_length):
        """
        Create general variables that will be used throughout the class

        :param window_width: Width of the entire window
        :param window_height: Height of the entire window

        :param simulation_accuracy: How accurately it will attempt to get the simulation (higher numbers = higher accuracy)
        :param step_length: The amount of time in seconds to move the simulation forward, (Smaller numbers = higher simulation accuracy as updates are more frequent)
        """

        # Create a new physics space with a simulation accuracy of 40
        self.physics_space = self.createPhysicsSpace(simulation_accuracy=simulation_accuracy)

        # Create a list of static sprites to render as static physics objects
        self.sprite_list: arcade.SpriteList[PhysicsSprite] = arcade.SpriteList()

        # Values for the width and Height of the window
        self.window_width = window_width
        self.window_height = window_height

        self.step_length = step_length

    @staticmethod
    def createPhysicsSpace(simulation_accuracy):
        """
        Create the physics simulation environment for all the objects

        :return: The created physics space
        """

        # Create a new empty physics space
        space = pymunk.Space()

        # Set simulation accuracy
        space.iterations = simulation_accuracy
        space.gravity = GRAVITY

        return space

    def simulationStep(self):
        """
        Move the simulation the amount of time set by the step_length variable

        :return: None
        """

        self.physics_space.step(self.step_length)

    def createRectangularObject(self, width, height, initialX, initialY, sprite_path):
        """
        Create a static physics sprite with the given properties and add it to the sprites list

        :param width: The width of the physics bounding box
        :param height: The height of the physics bounding box
        :param initialX: The initial X location of the object
        :param initialY: The initial Y location of the object
        :param sprite_path: The file path of the sprite to use
        :return: None
        """

        # Create a new static physics body
        physics_body = pymunk.Body(body_type=pymunk.Body.STATIC)

        # Set the initial position of the object
        physics_body.position = pymunk.Vec2d(initialX, initialY)




