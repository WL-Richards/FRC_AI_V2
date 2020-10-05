"""Implementation Layer For The Arcade Environment"""

__author__ = "Will Richards"
__copyright__ = "Copyright 2020, AEMBOT"

import os, signal, threading
from Keymapping.Keymap import Keymap

from EasyPhysics import *
from CollisionTypes import CollisionType
from EnvironmentObjectManager import EnvironmentGameObjects
from AgentController import AgentController

# Create window parameters
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 525
WINDOW_TITLE = "AI FRC Drive Training"

ENVIRONMENT_RUNNING = False

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



        # Manager to manage all static objects in the simulation
        self.StaticObjectManager = EnvironmentGameObjects(physics_environment=self.physics_environment,
                                                          screen_width=SCREEN_WIDTH,
                                                          screen_height=SCREEN_HEIGHT)

        # Create the dynamic player object
        self.player: AgentController = AgentController(physics_environment=self.physics_environment,
                                                       screen_width=SCREEN_WIDTH,
                                                       screen_height=SCREEN_HEIGHT)

        self.raycast_handler = RaycastHandler(physics_environment=self.physics_environment,
                                              player=self.player)

        # Create a handler for general static object collisions
        self.physics_environment.createCollisionHandler(firstCollisionType=CollisionType.STATIC_OBJECT,
                                                        secondCollisionType=CollisionType.DYNAMIC_OBJECT,
                                                        callback=self.player.on_static_collision)

        # Create handler for collisions with goal
        self.physics_environment.createCollisionHandler(firstCollisionType=CollisionType.GOAL_OBJECT,
                                                        secondCollisionType=CollisionType.DYNAMIC_OBJECT,
                                                        callback=self.player.on_goal_collision)



        self.player.set_raycast_handler(self.raycast_handler)
        self.player.reset()

        # Which action is being taken
        self.movement_values = [False, False, False, False]
        self.total_reward = 0


    def on_draw(self):
        """Called by the arcade lib when a draw call has been made"""

        # Initiate draw updates
        arcade.start_render()

        self.StaticObjectManager.draw_environment_objects()

        # Draw the raycasts being cast
        self.raycast_handler.draw_raycasts(show_hit_point=True)

        # Draw the player object
        self.player.draw()


    def on_key_press(self, symbol: int, modifiers: int):

        # Just kill the program I don't care how
        if symbol == Keymap.Esc.value:
            arcade.close_window()
            signal.pthread_kill(threading.current_thread().ident, signal.SIGKILL)

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

    def debug(self):
        """Temporary Debug Method"""
        pass

    def step(self, action: tuple):
        """
        Simulation Step, replaces on_update for a manually controlled step as opposed to based on what the simulation clock is doing

        :param action: The action in the form of tuple shaped like (left_power, right_power) to supply to the agent

        :return: Observation, Step Reward, Episode Completion Status
        """
        # Clear casts at at the beginning of update
        self.player.raycast_handler.clear_raycasts()

        self.physics_environment.simulateStep()

        obs, reward, done = self.player.step(action=action)

        self.player.apply_damping(dt=self.physics_environment.step_length)

        return obs,reward,done

    def reset(self):
        """
        Wrapper for player reset inside the environment

        :return: Observation at reset
        """
        return self.player.reset()

    def startEnvironment(self):
        """
        Start the arcade simulation

        :return: None
        """
        arcade.run()

        global ENVIRONMENT_RUNNING
        ENVIRONMENT_RUNNING = True

