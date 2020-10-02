from EasyPhysics import StaticPhysics, PhysicsEnvironment
from CollisionTypes import CollisionType

class EnvironmentGameObjects:
    """Manager for static objects within the scene"""

    def __init__(self, physics_environment: PhysicsEnvironment, screen_width, screen_height):
        self.environment = physics_environment

        # Create a new static object manager to manage all the game elements
        self.static_object_manager = StaticPhysics(physics_environment=self.environment)
        
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.create_game_objects()

    def create_game_objects(self):
        """Create all the required objects in the scene"""

        # Create the window bounds of the game and then draw them
        self.static_object_manager.createPhysicalWindowBounds()

        # Create the cargo ship in the middle
        self.static_object_manager.createStaticRectangularObject(width=80,
                                                                 height=238,
                                                                 initialX=(self.screen_width/2),
                                                                 initialY=(self.screen_height/2),
                                                                 collision_type=CollisionType.STATIC_OBJECT,
                                                                 sprite_path="Cargo Ship.png")
        # Create the 4 rocket objects on the sides of the arena
        self.create_rocket_objects()

        # Create the placement station
        self.static_object_manager.createStaticRectangularObject(width=130,
                                                                 height=30,
                                                                 initialX=(self.screen_width / 2.1),
                                                                 initialY=(self.screen_height - 15),
                                                                 collision_type=CollisionType.STATIC_OBJECT,
                                                                 sprite_path="Placement.png")

        # Create the placement station goal
        self.static_object_manager.createStaticRectangularObject(width=30,
                                                                 height= 12,
                                                                 initialX=((self.screen_width / 2.1) + 1),
                                                                 initialY=((self.screen_height - 15) - 18),
                                                                 collision_type=CollisionType.GOAL_OBJECT,
                                                                 sprite_path="Placement_Goal.png")

    def create_rocket_objects(self):
        """Create all the rocket objects"""

        # Create the Top Left Rocket
        self.static_object_manager.createStaticRectangularObject(width=35,
                                                                 height=58,
                                                                 initialX=17,
                                                                 initialY=(self.screen_height / 1.6),
                                                                 collision_type=CollisionType.STATIC_OBJECT,
                                                                 sprite_path="Rocket_Left.png")

        # Create the Bottom Left Rocket
        self.static_object_manager.createStaticRectangularObject(width=35,
                                                                 height=58,
                                                                 initialX=17,
                                                                 initialY=(self.screen_height / 2.6666666667),
                                                                 collision_type=CollisionType.STATIC_OBJECT,
                                                                 sprite_path="Rocket_Left.png")

        # Create the Top Right Rocket
        self.static_object_manager.createStaticRectangularObject(width=35,
                                                                 height=58,
                                                                 initialX=(self.screen_width - 17),
                                                                 initialY=(self.screen_height / 1.6),
                                                                 collision_type=CollisionType.STATIC_OBJECT,
                                                                 sprite_path="Rocket_Right.png")

        # Create the Bottom Right Rocket
        self.static_object_manager.createStaticRectangularObject(width=35,
                                                                 height=58,
                                                                 initialX=(self.screen_width - 17),
                                                                 initialY=(self.screen_height / 2.6666666667),
                                                                 collision_type=CollisionType.STATIC_OBJECT,
                                                                 sprite_path="Rocket_Right.png")

    def draw_environment_objects(self):
        """Draw the needed environment objects"""
        self.environment.draw_static_objects()