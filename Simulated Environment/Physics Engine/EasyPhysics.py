"""
High Level Physics Interface Meant To Be Used By The Environment Itself
"""

__author__ = "Will Richards"
__copyright__ = "Copyright 2020, AEMBOT"

from LowLevelPhysics import *

# Gravity to be used in the simulated environment, its None because damping is used to regulate object speed
GRAVITY = (0, 0)

STEP_LENGTH: float = 0.0


class PhysicsEnvironment:
    """Class to manager the overall physics environment"""

    def __init__(self, window_width, window_height, simulation_accuracy, step_length: float):
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

        # Set the step length globally
        global STEP_LENGTH
        STEP_LENGTH = step_length
        self.step_length = STEP_LENGTH

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

    def simulateStep(self):
        """
        Move the simulation the amount of time set by the step_length variable

        :return: None
        """

        self.physics_space.step(STEP_LENGTH)

    def draw_static_objects(self):
        """Draw all elements in the static sprite list"""

        self.sprite_list.draw()

    def createCollisionHandler(self, firstCollisionType: CollisionType, secondCollisionType: CollisionType, callback):
        """
        Create a new collision handler watching for specific collisions

        :param firstCollisionType: Collision type of one object
        :param secondCollisionType: Collision type of the other object
        :param callback: Function to be called when the objects collide (method name without parameters Eg. this.test)

        :return: None
        """

        # Create a new handler watching for the specified collisions
        collision_handler = self.physics_space.add_collision_handler(collision_type_a=firstCollisionType.value,
                                                                     collision_type_b=secondCollisionType.value)

        # Set the method to preform the callback to
        collision_handler.post_solve = callback


class StaticPhysics:
    """Class to manage creation of static physics object within the environment"""

    def __init__(self, physics_environment: PhysicsEnvironment):
        """
        Create a new manager for the static physical objects

        :param physics_environment: Reference to the overarching physics manager
        """
        self.physic_environment = physics_environment

    def createStaticRectangularObject(self, width, height, initialX, initialY, collision_type: CollisionType,
                                      sprite_path):
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
        bounding_box = pymunk.Poly.create_box(physics_body, (width, height))

        # Set the collision type to the value of the enum given by the parameter
        bounding_box.collision_type = collision_type.value

        # Add the physical object and its bounding box to the physics simulation space
        self.physic_environment.physics_space.add(physics_body, bounding_box)

        # Create the full object with physics and a sprite
        completed_object = BoxSprite(bounding_box=bounding_box,
                                     filename=sprite_path,
                                     width=width,
                                     height=height)

        # Finally add the full object to the list of sprites in the scene
        self.physic_environment.sprite_list.append(completed_object)

    def createPhysicalWindowBounds(self):
        """
        Create a bounding box around the window so that the Agent cannot escape

        :return: None
        """

        # Create the bottom bound
        self.physic_environment.lines.createLine(body_type=pymunk.Body.STATIC,
                                                 collision_type=CollisionType.STATIC_OBJECT,
                                                 first_endpoint=(0, self.physic_environment.window_height),
                                                 second_endpoint=(self.physic_environment.window_width,
                                                                  self.physic_environment.window_height),
                                                 thickness=2)

        # Create the top bound
        self.physic_environment.lines.createLine(body_type=pymunk.Body.STATIC,
                                                 collision_type=CollisionType.STATIC_OBJECT,
                                                 first_endpoint=(0, 0),
                                                 second_endpoint=(self.physic_environment.window_width, 0),
                                                 thickness=2)

        # Create the right side bound
        self.physic_environment.lines.createLine(body_type=pymunk.Body.STATIC,
                                                 collision_type=CollisionType.STATIC_OBJECT,
                                                 first_endpoint=(0, 0),
                                                 second_endpoint=(0, self.physic_environment.window_height),
                                                 thickness=2)

        # Create the left side bound
        self.physic_environment.lines.createLine(body_type=pymunk.Body.STATIC,
                                                 collision_type=CollisionType.STATIC_OBJECT,
                                                 first_endpoint=(self.physic_environment.window_width, 0),
                                                 second_endpoint=(self.physic_environment.window_width,
                                                                  self.physic_environment.window_height),
                                                 thickness=2)

        # Draw the lines to the screen
        self.physic_environment.lines.drawLines()


class DynamicPhysics:

    @staticmethod
    def createDynamicRectangularObject(physics_environment: PhysicsEnvironment, width, height, mass, friction, damping,
                                       initialX, initialY,
                                       collision_type: CollisionType, sprite_path):
        """
        Create a new dynamic physics object

        :param physics_environment: Reference to the current physics environment
        :param width: Width of object (PX)
        :param height: Height of object (PX)
        :param mass: The mass of the object
        :param friction: How much friction the object should create
        :param damping: How quickly the velocity should fall off when it is no longer being applied (Lower numbers = more damping)
        :param initialX: Object's initial X coordinate
        :param initialY: Object's initial Y coordinate
        :param collision_type: What kind of collision the object has
        :param sprite_path: Path to the objects sprite

        :return: The created object
        """

        # How likely the object is to rotate around its center
        object_moment = pymunk.moment_for_box(mass=mass,
                                              size=(width, height))

        # Create an actual physics body with mass
        physics_body = pymunk.Body(mass=mass,
                                   moment=object_moment)

        # Set the starting location of the object
        physics_body.position = pymunk.Vec2d(initialX, initialY)

        # Complete physics object (without a sprite)
        bounding_box = pymunk.Poly.create_box(body=physics_body,
                                              size=(width, height))

        # The amount of friction the object should generate when it moves
        bounding_box.friction = friction

        # The type of collision this object has
        bounding_box.collision_type = collision_type.value

        bounding_box.filter = pymunk.ShapeFilter(categories=0b1)

        # Add the object to the physics space
        physics_environment.physics_space.add(physics_body, bounding_box)

        # Finally create the entire object with a sprite
        completed_object = DynamicObject(bounding_box=bounding_box,
                                         sprite_path=sprite_path,
                                         width=width,
                                         height=height,
                                         damping=damping,
                                         initialX=initialX,
                                         initialY=initialY)
        return completed_object


class DynamicObject(BoxSprite):
    """Inherits from the Box Sprite to simply add more functionality to that object"""

    def __init__(self, bounding_box: pymunk.shapes.Poly, sprite_path, width, height, damping, initialX, initialY):
        """
        Create a new object

        :param bounding_box: The bounding box of the physics object
        :param sprite_path: Path to the sprite being used
        :param width: Width of the object
        :param height: Height of the object
        :param damping: The amount of damping used to slow down and object
        """

        super().__init__(bounding_box=bounding_box, filename=sprite_path, width=width, height=height)
        self.damping = damping
        self.sprite_path = sprite_path
        self.initialX = initialX
        self.initialY = initialY

    def get_damping(self):
        """
        Get the amount of damping to be applied to the object

        :return: damping amount
        """

        return self.damping

    def get_instance(self):
        return self

    def apply_forward_impulse(self, impulse: float, point: tuple, is_world: bool):
        """
        Apply A Certain Impulse To the Forward Direction of the Object And Move The Object There

        :param impulse: How much force to apply
        :param point: The point at which to apply the force to the object
        :param is_world: Whether or not the the point is relative to the world or the object

        :return: None
        """

        # Use the parent method to just apply the force to the forward direction of the object
        super().apply_impulse(impulse=(0, impulse),
                              point=point,
                              is_world=is_world)

        # Update the entire player object to the position of the physics object
        x, y = self.get_position()  # Get position of player and split to X and Y
        self.center_x = x  # Set the values gotten from get_position and set them to the total object
        self.center_y = y
        self.angle = self.get_true_angle()  # Set the angle of the object

    def apply_damping(self, dt):
        """
        Applies a certain amount of damping to the object to slow it down

        :return: None
        """

        pymunk.Body.update_velocity(body=self.bounding_box.body,
                                    gravity=GRAVITY,
                                    damping=self.damping,
                                    dt=dt)

    def stop_object(self):
        """
        Applies an absurdly high amount of damping instantly to stop the object from moving

        :return: None
        """

        pymunk.Body.update_velocity(body=self.bounding_box.body,
                                    gravity=GRAVITY,
                                    damping=0.0000001,
                                    dt=0)

    def impulse_move(self, impulse: float, point: tuple, isWorld: bool):
        """
        Move the object by applying an impulse and then applying damping

        :param impulse: Force to apply to the forward vector of the object
        :param point: The point on the object where it is applied
        :param isWorld: Whether or not that point is in local or world space

        :return: None
        """

        # Apply initial force
        self.apply_forward_impulse(impulse=impulse,
                                   point=point,
                                   is_world=isWorld)


class RaycastHandler:
    from AgentController import AgentController

    # Length of the rays
    RAYCAST_LENGTH = 150

    """Handler to contain many raycasts to get distances to objects and other information"""

    def __init__(self, physics_environment: PhysicsEnvironment, player: AgentController):
        from AgentController import AgentController

        self.ray_casts = []

        self.physics_environment = physics_environment
        self.player: AgentController = player

    def clear_raycasts(self):
        self.ray_casts.clear()

    def create_raycast(self, start: tuple, end: tuple, radius):
        """
        Create a single raycast and the list

        :param start: Start of the cast
        :param end: End of the cast
        :param radius: Radius around the cast to consider collided

        :return: None
        """

        # Create a a generic raycast with the given information that ignores dynamic objects
        ray = self.physics_environment.physics_space.segment_query_first(start=start,
                                                                         end=end,
                                                                         radius=radius,
                                                                         shape_filter=pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b1))
        ray_info = (ray, start, end, radius)

        # Add the ray to the list
        self.ray_casts.append(ray_info)

    def calculate_multiraycast(self):
        """
        Create a ring of raycasts around the object

        :return: None
        """

        # Create raycast at 90 degrees
        self.create_raycast(start=(self.player.get_position().x, self.player.get_position().y),
                            end=((self.player.get_position().x + (
                                        math.cos(math.radians(self.player.get_angle())) * self.RAYCAST_LENGTH)),
                                 (self.player.get_position().y + (
                                             math.sin(math.radians(self.player.get_angle())) * self.RAYCAST_LENGTH))),
                            radius=2)

        # Create raycast at 270 degrees
        self.create_raycast(start=(self.player.get_position().x, self.player.get_position().y),
                            end=((self.player.get_position().x + (
                                        math.cos(math.radians(self.player.get_angle())) * -self.RAYCAST_LENGTH)),
                                 (self.player.get_position().y + (
                                             math.sin(math.radians(self.player.get_angle())) * -self.RAYCAST_LENGTH))),
                            radius=2)

        # Create raycast at 180 degrees
        self.create_raycast(start=(self.player.get_position().x, self.player.get_position().y),
                            end=(
                                (self.player.get_position().x + (math.cos(
                                    math.radians(self.player.get_angle() + 90)) * self.RAYCAST_LENGTH)),
                                (self.player.get_position().y + (math.sin(
                                    math.radians(self.player.get_angle() + 90)) * self.RAYCAST_LENGTH))),
                            radius=2)

        # Create raycast at 360/0
        self.create_raycast(start=(self.player.get_position().x, self.player.get_position().y),
                            end=(
                                (self.player.get_position().x + (
                                        math.cos(math.radians(self.player.get_angle() + 90)) * -self.RAYCAST_LENGTH)),
                                (self.player.get_position().y + (
                                        math.sin(math.radians(self.player.get_angle() + 90)) * -self.RAYCAST_LENGTH))),
                            radius=2)

        # Create raycast at 45
        self.create_raycast(start=(self.player.get_position().x, self.player.get_position().y),
                            end=(
                                (self.player.get_position().x + (
                                        math.cos(math.radians(self.player.get_angle() - 45)) * self.RAYCAST_LENGTH)),
                                (self.player.get_position().y + (
                                        math.sin(math.radians(self.player.get_angle() - 45)) * self.RAYCAST_LENGTH))),
                            radius=2)

        # Create raycast at 225
        self.create_raycast(start=(self.player.get_position().x, self.player.get_position().y),
                            end=(
                                (self.player.get_position().x + (
                                        math.cos(math.radians(self.player.get_angle() - 45)) * -self.RAYCAST_LENGTH)),
                                (self.player.get_position().y + (
                                        math.sin(math.radians(self.player.get_angle() - 45)) * -self.RAYCAST_LENGTH))),
                            radius=2)

        # Create raycast at 135
        self.create_raycast(start=(self.player.get_position().x, self.player.get_position().y),
                            end=(
                                (self.player.get_position().x + (
                                        math.cos(math.radians(self.player.get_angle() + 45)) * self.RAYCAST_LENGTH)),
                                (self.player.get_position().y + (
                                        math.sin(math.radians(self.player.get_angle() + 45)) * self.RAYCAST_LENGTH))),
                            radius=2)

        # Create raycast at 315
        self.create_raycast(start=(self.player.get_position().x, self.player.get_position().y),
                            end=(
                                (self.player.get_position().x + (
                                        math.cos(math.radians(self.player.get_angle() + 45)) * -self.RAYCAST_LENGTH)),
                                (self.player.get_position().y + (
                                        math.sin(math.radians(self.player.get_angle() + 45)) * -self.RAYCAST_LENGTH))),
                            radius=2)

        """
            0 - Top Ray
            1 - Bottom Ray
            2 - Left Ray
            3 - Right Ray
            4 - Upper Right Ray
            5 - Bottom Right Ray
            6 - Upper Left Ray
            7 - Bottom Left Ray
        """

        # List to hold all distances from the
        ray_hit_distances = [self.player.get_position().get_distance(self.ray_casts[0][0].point) if self.ray_casts[0][0] is not None else None,
                             self.player.get_position().get_distance(self.ray_casts[1][0].point) if self.ray_casts[1][0] is not None else None,
                             self.player.get_position().get_distance(self.ray_casts[2][0].point) if self.ray_casts[2][0] is not None else None,
                             self.player.get_position().get_distance(self.ray_casts[3][0].point) if self.ray_casts[3][0] is not None else None,
                             self.player.get_position().get_distance(self.ray_casts[4][0].point) if self.ray_casts[4][0] is not None else None,
                             self.player.get_position().get_distance(self.ray_casts[5][0].point) if self.ray_casts[5][0] is not None else None,
                             self.player.get_position().get_distance(self.ray_casts[6][0].point) if self.ray_casts[6][0] is not None else None,
                             self.player.get_position().get_distance(self.ray_casts[7][0].point) if self.ray_casts[7][0] is not None else None]

        return ray_hit_distances

    def draw_raycasts(self, show_hit_point: bool):
        """
        Draw the raycasts to the screen to see if they are working correctly

        :param show_hit_point: Whether or not we should show the point of contact of the rays

        :return: None
        """

        # Draw the raycast lines
        for ray in self.ray_casts:
            # Draw the line using the arcade library
            arcade.draw_line(start_x=ray[1][0],
                             start_y=ray[1][1],
                             end_x=ray[2][0],
                             end_y=ray[2][1],
                             color=arcade.color.DARK_GRAY,
                             line_width=1)

            # Draw the hit point of the ray
            if ray[0] is not None and show_hit_point:
                arcade.draw_point(ray[0].point.x, ray[0].point.y, arcade.color.RED, 10)
