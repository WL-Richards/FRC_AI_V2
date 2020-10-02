"""Implementation Layer For The Arcade Environment"""

__author__ = "Will Richards"
__copyright__ = "Copyright 2020, AEMBOT"

import arcade
import os
from Keymap import Keymap

from EasyPhysics import *
from CollisionTypes import CollisionType
from EnvironmentObjectManager import EnvironmentGameObjects

# Create window parameters
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 525
WINDOW_TITLE = "AI FRC Drive Training"

# The speed to move the robot during non AI debugging
TEST_CONTROL_SPEED = 35

class VirtualEnvironment(arcade.Window):
    """Create a new class to manage the virtual environment"""

    def __init__(self):

        # Create a new window
        super().__init__(width=SCREEN_WIDTH,
                         height=SCREEN_HEIGHT,
                         title=WINDOW_TITLE)

        # Set the background to black
        arcade.set_background_color(arcade.color.BLACK)

        # Change the current working directory to the sprites director to get relative file access
        os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/Graphics/")

        # Create a new physics environment to control physics from
        self.physics_environment = PhysicsEnvironment(window_width=SCREEN_WIDTH,
                                                      window_height=SCREEN_HEIGHT,
                                                      simulation_accuracy=45,
                                                      step_length=0.01)

        # Create the player object with all the given parameters
        self.player: DynamicObject = DynamicPhysics.createDynamicRectangularObject(physics_environment=self.physics_environment,
                                                                                   width=50,
                                                                                   height=60,
                                                                                   mass=1.0,
                                                                                   friction=0.9,
                                                                                   damping=0.92,
                                                                                   initialX=(SCREEN_WIDTH / 1.3),
                                                                                   initialY=(SCREEN_HEIGHT / 7),
                                                                                   collision_type=CollisionType.DYNAMIC_OBJECT,
                                                                                   sprite_path="Player.png")

        # Manager to manage all static objects in the simulation
        self.StaticObjectManager = EnvironmentGameObjects(physics_environment=self.physics_environment,
                                                          screen_width=SCREEN_WIDTH,
                                                          screen_height=SCREEN_HEIGHT)

        # Which action is being taken
        self.movement_values = [False, False, False, False]

        # Once all variables have been created start the environment
        self.startEnvironment()

    def on_draw(self):
        """Called by the arcade lib when a draw call has been made"""

        # Initiate draw updates
        arcade.start_render()

        self.StaticObjectManager.draw_environment_objects()

        # Draw the player object
        self.player.draw()


    def on_key_press(self, symbol: int, modifiers: int):
        # Forward
        if symbol == Keymap.W.value:
           self.movement_values[0] = True

        if symbol == Keymap.Up.value:
            self.movement_values[1] = True

        # Reverse
        if symbol == Keymap.S.value:
            self.movement_values[2] = True

        if symbol == Keymap.Down.value:
            self.movement_values[3] = True

    def on_key_release(self, symbol: int, modifiers: int):
        # Forward
        if symbol == Keymap.W.value:
            self.movement_values[0] = False

        if symbol == Keymap.Up.value:
            self.movement_values[1] = False

        # Reverse
        if symbol == Keymap.S.value:
            self.movement_values[2] = False

        if symbol == Keymap.Down.value:
            self.movement_values[3] = False

    def on_update(self, delta_time: float):
        """Called when the game tries to update"""

        self.physics_environment.simulateStep()

        self.control_player()
        self.player.apply_damping(dt=delta_time)

    def control_player(self):
        """
        Set the power values

        :return:
        """
        left_power = 0
        right_power = 0

        if self.movement_values[0]:
            right_power = TEST_CONTROL_SPEED

        if self.movement_values[1]:
            left_power = TEST_CONTROL_SPEED

        if self.movement_values[2]:
            right_power = -TEST_CONTROL_SPEED

        if self.movement_values[3]:
            left_power = -TEST_CONTROL_SPEED

        # Move Right Side
        self.player.impulse_move(impulse=right_power,
                                 point=(-6, 0),
                                 isWorld=False)

        # Move Left Side
        self.player.impulse_move(impulse=left_power,
                                 point=(6, 0),
                                 isWorld=False)

    def startEnvironment(self):
        arcade.run()

