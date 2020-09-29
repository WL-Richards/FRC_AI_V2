"""
High Level Physics Interface Meant To Be Used By The Environment Itself
"""

__author__ = "Will Richards"
__copyright__ = "Copyright 2020, AEMBOT"

import math
import pymunk
import arcade
from LowLevelPhysics import *
from CollisionTypes import CollisionType

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

        # Maintains a list of all lines within the scene
        self.lines = LineHandler(physics_space=self.physics_space)

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

    def createRectangularObject(self, width, height, initialX, initialY, collision_type: CollisionType, sprite_path):
        """
        Create a static physics sprite with the given properties and add it to the sprites list

        :param width: The width of the physics bounding box
        :param height: The height of the physics bounding box
        :param initialX: The initial X location of the object
        :param initialY: The initial Y location of the object
        :param collision_type: Enum to represent the type of object it is and in turn how it should handle collisions
        :param sprite_path: The file path of the sprite to use
        :return: None
        """

        # Create a new static physics body
        physics_body = pymunk.Body(body_type=pymunk.Body.STATIC)

        # Set the initial position of the object
        physics_body.position = pymunk.Vec2d(initialX, initialY)

        # Create a new rectangular bounding box with the given physics information and the given width and height
        object_bounding_box = pymunk.Poly.create_box(physics_body, (width, height))

        # Set the collision type to the value of the enum given by the parameter
        object_bounding_box.collision_type = collision_type.value

        # Add the physical object and its bounding box to the physics simulation space
        self.physics_space.add(physics_body, object_bounding_box)

        # Create the full object with physics and a sprite
        completed_object = BoxSprite(object_bounding_box, sprite_path, width=width, height=height)

        # Finally add the full object to the list of sprites in the scene
        self.sprite_list.append(completed_object)

    def createPhysicalWindowBounds(self):
        """
        Create a bounding box around the window so that the Agent cannot escape

        :return: None
        """

        # Create the bottom bound
        self.lines.createLine(body_type=pymunk.Body.STATIC,
                              collision_type=CollisionType.STATIC_OBJECT,
                              first_endpoint=(0, self.window_height),
                              second_endpoint=(self.window_width,self.window_height),
                              thickness=1)

        # Create the top bound
        self.lines.createLine(body_type=pymunk.Body.STATIC,
                              collision_type=CollisionType.STATIC_OBJECT,
                              first_endpoint=(0, 0),
                              second_endpoint=(self.window_width, 0),
                              thickness=1)

        # Create the right side bound
        self.lines.createLine(body_type=pymunk.Body.STATIC,
                              collision_type=CollisionType.STATIC_OBJECT,
                              first_endpoint=(0, 0),
                              second_endpoint=(0, self.window_height),
                              thickness=1)

        # Create the left side bound
        self.lines.createLine(body_type=pymunk.Body.STATIC,
                              collision_type=CollisionType.STATIC_OBJECT,
                              first_endpoint=(self.window_width, 0),
                              second_endpoint=(self.window_width, self.window_height),
                              thickness=1)



