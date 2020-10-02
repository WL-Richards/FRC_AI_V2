"""General Agent Controller"""

__author__ = "Will Richards"
__copyright__ = "Copyright 2020, AEMBOT"

import os

from EasyPhysics import DynamicObject, PhysicsEnvironment, DynamicPhysics
from CollisionTypes import CollisionType


class AgentController(DynamicObject):
    def __init__(self, physics_environment: PhysicsEnvironment, screen_width, screen_height):
        # Change the current working directory to the sprites director to get relative file access
        os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/Graphics/")

        # Create the dynamic player object
        player_object: DynamicObject = DynamicPhysics.createDynamicRectangularObject(
            physics_environment=physics_environment,
            width=50,
            height=60,
            mass=1.0,
            friction=0.9,
            damping=0.92,
            initialX=(screen_width / 1.3),
            initialY=(screen_height / 7),
            collision_type=CollisionType.DYNAMIC_OBJECT,
            sprite_path="Player.png")

        # Inherit the dynamic object
        super().__init__(bounding_box=player_object.bounding_box,
                         sprite_path=player_object.sprite_path,
                         width=player_object.width,
                         height=player_object.height,
                         damping=player_object.damping)

        # Get local variable of self
        self.player: DynamicObject = super().get_instance()

    def control(self, control_array, control_speed):
        """
        Heuristic controlled values

        :param control_array: Array of bools saying if it should be moving a certain direction
            0 - Right Forward
            1 - Left Forward
            2 - Right Backwards
            3 - Left Backwards
        :param control_speed: Speed to use to control the player, constant for heuristic controls

        :return: None
        """
        left_power = 0
        right_power = 0

        if control_array[0]:
            right_power = control_speed

        if control_array[1]:
            left_power = control_speed

        if control_array[2]:
            right_power = -control_speed

        if control_array[3]:
            left_power = -control_speed

        # Move Right Side
        self.player.impulse_move(impulse=right_power,
                                 point=(-6, 0),
                                 isWorld=False)

        # Move Left Side
        self.player.impulse_move(impulse=left_power,
                                 point=(6, 0),
                                 isWorld=False)
