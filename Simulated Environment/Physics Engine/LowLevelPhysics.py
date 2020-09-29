"""
Low Level Physics Implementation Built On By EasyPhysics.py
"""

__author__ = "Will Richards"
__copyright__ = "Copyright 2020, AEMBOT"

import math
import arcade
import pymunk


class PhysicsSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, filename):
        """
        Creates a new physics object

        :param pymunk_shape: The bounding box created by pymunk
        :param filename: Path to the displayed sprite
        """

        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape

    def apply_impulse(self, impulse, point, is_world):
        """
        Apply an impulse to a location on a sprite

        :param impulse: The impulse force to apply
        :param point: The point to apply the impulse
        :param is_world: Whether or not it is world or local oriented
        :return: None
        """

        if is_world:
            self.pymunk_shape.body.apply_impulse_at_world_point(tuple(impulse), point=tuple(point))
        else:
            self.pymunk_shape.body.apply_impulse_at_local_point(tuple(impulse), point=tuple(point))

    def get_body(self):

        """Gets information regarding the body that is currently in use"""
        return self.pymunk_shape.body

    def get_shape(self):
        """Get the physics shape"""
        return self.pymunk_shape

    def get_position(self):

        """Gets the current position of the physics body"""
        return tuple(self.pymunk_shape.body.position)

    def get_local_position(self):
        """Converts World Space Coordinated To Local Coordinates"""

        return tuple(self.get_body().world_to_local(self.pymunk_shape.body.position))

    def set_position(self, x, y):
        """
        Sets the new position of the object

        :param x: X coord of new position
        :param y: Y coord of new position
        :return: None
        """

        self.pymunk_shape.body.position = pymunk.Vec2d(x, y)

    def get_rotations(self):
        """
        Gets the number of rotations of the body in radians, NOTE: Use get_angle for an angle from 0-360

        :return: Number of rotations in radians
        """
        return self.pymunk_shape.body.angle

    def get_angle(self):
        """
        Get the angle of the object in terms of 0-360 degrees

        :return: The current angle of the object
        """
        angle = math.degrees(self.get_rotations())

        angle = angle % 360

        return angle

    def set_angle(self, angle):
        """
        Allows the setting of a robots angle in degrees

        :param angle: The new angle to set (DEGREES)
        :return: None
        """
        self.pymunk_shape.body.angle = (angle/360)

    def get_velocity(self):
        """
        Get the X and Y velocity values respectively

        :return: Velocity
        """

        return tuple(self.pymunk_shape.body.velocity)


    def set_velocity(self, x_vel, y_vel):
        """Sets a velocity on the body"""
        self.pymunk_shape.body.velocity = pymunk.Vec2d(x_vel, y_vel)


class CircleSprite(PhysicsSprite):
    """Creates a Circular Physics Sprite"""
    def __init__(self, pymunk_shape, filename):
        """
        Create a new Circular Sprite that inherits from the PhysicsSprite class

        :param pymunk_shape: Bounding box of the object
        :param filename: Path to sprite
        """
        super().__init__(pymunk_shape, filename)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2


class BoxSprite(PhysicsSprite):
    """Creates A Box Physics Sprite"""
    def __init__(self, pymunk_shape, filename, width, height):
        """
        Create a new Box Sprite that inherits from the PhysicsSprite class

        :param pymunk_shape: Bounding box of the object
        :param filename: Path to sprite
        :param width: Width of the cube
        :param height: Height of the cube
        """
        super().__init__(pymunk_shape, filename)
        self.width = width
        self.height = height
