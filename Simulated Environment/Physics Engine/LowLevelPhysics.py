"""
Low Level Physics Implementation Built On By EasyPhysics.py
"""

__author__ = "Will Richards"
__copyright__ = "Copyright 2020, AEMBOT"

import math
import arcade
import pymunk

from CollisionTypes import CollisionType

class PhysicsSprite(arcade.Sprite):
    def __init__(self, bounding_box: pymunk.shapes.Poly, filename):
        """
        Creates a new physics object

        :param pymunk_shape: The bounding box created by pymunk
        :param filename: Path to the displayed sprite
        """

        super().__init__(filename, center_x=bounding_box.body.position.x, center_y=bounding_box.body.position.y)
        self.bounding_box = bounding_box

        self.rotational_offset = 0

    def apply_impulse(self, impulse, point, is_world):
        """
        Apply an impulse to a location on a sprite

        :param impulse: The impulse force to apply
        :param point: The point to apply the impulse
        :param is_world: Whether or not it is world or local oriented
        :return: None
        """

        if is_world:
            self.bounding_box.body.apply_impulse_at_world_point(impulse, point=point)
        else:
            self.bounding_box.body.apply_impulse_at_local_point(impulse, point=point)

    def get_body(self):

        """Gets information regarding the body that is currently in use"""
        return self.bounding_box.body

    def get_shape(self):
        """Get the physics shape"""
        return self.bounding_box

    def get_position(self):

        """Gets the current position of the physics body"""
        return tuple(self.bounding_box.body.position)

    def get_local_position(self):
        """Converts World Space Coordinated To Local Coordinates"""

        return tuple(self.get_body().world_to_local(self.bounding_box.body.position))

    def set_position(self, x, y):
        """
        Sets the new position of the object

        :param x: X coord of new position
        :param y: Y coord of new position
        :return: None
        """

        self.bounding_box.body.position = pymunk.Vec2d(x, y)

    def get_rad_rotations(self):
        """
        Gets the number of rotations of the body in radians, NOTE: Use get_angle for an angle from 0-360

        :return: Number of rotations in radians
        """
        return self.bounding_box.body.angle

    def get_rotations(self):
        """
        Gets the number of rotations of the body

        :return: Number of rotations
        """

        return (self.bounding_box.body.angle / (2*math.pi))

    def get_angle(self):
        """
        Get the angle of the object taking into account the initial offset to a standard unit cirlce

        :return: The angle world oriented angle
        """

        return ((self.get_rotations() * 360) + self.rotational_offset) % 360

    def get_true_angle(self):
        """
        Get the angle of the object in terms of 0-360 degrees

        :return: The current angle of the object
        """
        angle = math.degrees(self.get_rad_rotations())

        angle = angle % 360

        return angle

    def set_rotational_offset(self, offset):
        """
        Set the offset value to use for the rotations

        :param offset: Angle in degrees

        :return: None
        """

        self.rotational_offset = offset

    def set_angle(self, angle):
        """
        Allows the setting of a robots angle in degrees

        :param angle: The new angle to set (DEGREES)
        :return: None
        """
        self.bounding_box.body.angle = (angle/360)

    def get_velocity(self):
        """
        Get the X and Y velocity values respectively

        :return: Velocity
        """

        return tuple(self.bounding_box.body.velocity)


    def set_velocity(self, x_vel, y_vel):
        """Sets a velocity on the body"""

        self.bounding_box.body.velocity = pymunk.Vec2d(x_vel, y_vel)


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

    def __init__(self, bounding_box, filename, width, height):
        """
        Create a new Box Sprite that inherits from the PhysicsSprite class

        :param bounding_box: Bounding box of the object
        :param filename: Path to sprite
        :param width: Width of the cube
        :param height: Height of the cube
        """
        super().__init__(bounding_box, filename)
        self.width = width
        self.height = height


class LineHandler:
    """Allows for the creation and management of many different line segments"""

    def __init__(self, physics_space):
        """
        Create a new LineSegments class and make a list to hold different line segments

        :param physics_space: Reference to the physics space that these lines will be created within
        """

        self.lines = []
        self.physics_space = physics_space

    def createLine(self, body_type, collision_type: CollisionType, first_endpoint: tuple, second_endpoint: tuple, thickness):
        """
        Create a new line and add it to the list of lines

        :param body_type: The physical property of the line, Static or Dynamic
        :param collision_type: The type of collision the line should register if it collides with another object
        :param first_endpoint: The first coordinate of the line segment
        :param second_endpoint: The second coordinate of the line segment
        :param thickness: The thickness of the line
        :return: None
        """

        # Physical body of the line segment
        physics_body = pymunk.Body(body_type=body_type)

        # Create the line segment with the given parameters
        line_segment = pymunk.Segment(physics_body, [first_endpoint[0], first_endpoint[1]], [second_endpoint[0], second_endpoint[1]], thickness)

        # Set what kind of collision it should register
        line_segment.collision_type = collision_type.value

        # Add the line to the physics simulation and finally add it to the list of lines in the simulation
        self.physics_space.add(line_segment)
        self.lines.append(line_segment)

    def drawLines(self):
        """Draw all the lines within the lines array"""

        for line in self.lines:

            # The physical body of the line
            line_body = line.body

            # Get the start and end point of the line
            startPoint = line_body.position + line.a.rotated(line_body.angle)
            endPoint = line_body.position + line.b.rotated(line_body.angle)

            # Draw the line using the arcade library
            arcade.draw_line(start_x=startPoint.x,
                             start_y=startPoint.y,
                             end_x=endPoint.x,
                             end_y=endPoint.y,
                             color=arcade.color.DARK_GRAY,
                             line_width=1)



