"""
High Level Physics Interface Meant To Be Used By The Environment Itself
"""

__author__ = "Will Richards"
__copyright__ = "Copyright 2020, AEMBOT"

import math
import pymunk
from LowLevelPhysics import *

# Gravity to be used in the simulated environment, its None because dampening is used to regulate object speed
GRAVITY = (0, 0)


class PhysicsEnvironment:

    def __init__(self, window_width, window_height, step_length):
        """
        Create general variables that will be used throughout the class

        :param window_width: Width of the entire window
        :param window_height: Height of the entire window
        :param step_length: The amount of time in seconds to move the simulation forward (Smaller numbers = higher simulation accuracy)
        """

        self.physics_space = self.createPhysicsSpace(simulation_accuracy=35)

        # Values for the width and Height of the window
        self.window_width = window_width
        self.window_height = window_height

        self.step_length = step_length

    def createPhysicsSpace(self, simulation_accuracy):
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


