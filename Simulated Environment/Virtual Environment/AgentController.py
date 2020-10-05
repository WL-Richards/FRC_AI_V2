"""General Agent Controller"""

__author__ = "Will Richards"
__copyright__ = "Copyright 2020, AEMBOT"

import os

from EasyPhysics import *
from CollisionTypes import CollisionType


class AgentController(DynamicObject):
    def __init__(self, physics_environment: PhysicsEnvironment, screen_width, screen_height):
        # Change the current working directory to the sprites director to get relative file access
        os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/Graphics/")

        self.physics_environment = physics_environment

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
                         damping=player_object.damping,
                         initialX=(screen_width / 1.3),
                         initialY=(screen_height / 7))

        # Get local variable of self
        self.player: DynamicObject = super().get_instance()

        self.raycast_handler = None

        # Set the initial rotation offset
        self.player.set_rotational_offset(offset=90)

        # Training variables
        self.current_epsisode = 0
        self.current_step = 0
        self.current_episode_done = False
        self.last_reward = 0
        self.hit_goal = False

        self.goal_position = self.physics_environment.sprite_list[
            len(self.physics_environment.sprite_list) - 1].get_position()

        # Observation Data
        self.starting_distance = self.get_distance_to_goal()

        # Set the last distance to the starting difference so they agent doesnt get a huge penalty at the start
        self.last_distance = self.starting_distance

    def set_raycast_handler(self, raycast_handler):
        """
        Set the local raycast_handler to the global one

        :param raycast_handler: Reference to the global handler
        :return:
        """

        self.raycast_handler = raycast_handler

    def collect_obeservations(self):
        """
        Collect required observations of the space

        Observations:
        0-7: Spacial Observations from the raycast
        8: Robot X
        9: Robot Y
        10: Robot Angle
        11: Goal X
        12: Goal Y


        :param raycast_handler: Reference to the overall raycast handler so collect_observations can get spacial info


        :return: List of all collected observations separated
        """

        # List to contain all observations
        observations = []

        # Get the raycast distances
        spacial_distances = self.raycast_handler.calculate_multiraycast()

        # Current Position Of Agent
        agent_position = self.player.get_position()

        # Get the Current Position Of The Goal

        # The agents current angle
        agent_angle = self.player.get_true_angle()

        # Separate the raycast distances out into single values
        for distance in spacial_distances:
            observations.append(distance)

        # Information about the agents current location
        observations.append(agent_position.x)
        observations.append(agent_position.y)

        # The current angle of the agent
        observations.append(agent_angle)

        # Information about the goals position
        observations.append(self.goal_position.x)
        observations.append(self.goal_position.y)

        return observations

    def on_goal_collision(self, physics_space, collision_info, data):
        """
         When the agent collides with the goal

         :param physics_space: The physics environment its self
         :param collision_info: Info about the objects that collided
         :param data: misc. data
         :return:
         """
        # Set the player to know that the current episode is complete
        self.current_episode_done = True

        print("Collided With Goal")
        self.hit_goal = True

    def on_static_collision(self, physics_space, collision_info, data):
        """
        When the agent collides with anything other than the goal

        :param physics_space: The physics environment its self
        :param collision_info: Info about the objects that collided
        :param data: misc. data

        :return: None
        """

        # Set the player to know that the current episode is complete
        self.current_episode_done = True

    def reset(self):
        """
        Reset the environment

        :return: The new observation
        """

        # Stop the objects movement
        self.player.stop_object()

        self.current_epsisode = 0

        # Reset the angle
        self.player.set_angle(0)

        # Reset the the position of the agent
        self.player.set_position(x=self.player.initialX,
                                 y=self.player.initialY)

        self.last_distance = self.starting_distance  # On reset set the distance from the last step equal to the current distance
        self.last_reward = 0  # Set the reward from the last step equal to 0
        self.hit_goal = False  # Reset whether or not the goal has been reached

        self.current_step = 0  # Reset the current step to 0

        observation = self.collect_obeservations()  # Collect observation at restart

        self.current_episode_done = False # Start a new episode
        return observation # Return the starting observation

    def step(self, action: tuple):
        """
        Called whenever the agent attempts to take an action

        :param delta_time: Simulation delta time
        :param action: The action as a tuple (left_power, right_power)

        :return: Observation, Step reward, and episode completion status
        """



        # If the current episode is still happening process the specified actions
        if not self.current_episode_done:

            # Pass the action values into the step to move us one action forward
            self.control(left_input=action[0],
                         right_input=action[1])
        else:

            # If the episode is done and we are waiting for the next episode to start dont provide any input
            self.control(left_input=0,
                         right_input=0)

        # Collect the observation after the action has been taken
        observations = self.collect_obeservations()

        # Increase the current step count
        self.current_step += 1

        # Calculate the reward received from the action taken
        reward = self.calculate_agent_reward()

        # After the reward has been calculated set the current distance to the goal to be the distance at the previous step
        self.last_distance = self.get_distance_to_goal()

        # If the goal has been reached and the episode is done add 100 to the reward if not then subtract 100
        if self.hit_goal and self.current_episode_done:
            reward += 100
        elif not self.hit_goal and self.current_episode_done:
            reward -= 100

        return observations, reward, self.current_episode_done

    def calculate_agent_reward(self):
        """
        Calculate the reward for the agent at the current step

        :return: The reward obtained for that step
        """
        distance = self.get_distance_to_goal()

        if math.isclose(distance, self.last_distance, rel_tol=0.0001):
            return 0
        elif distance < self.last_distance:
            reward = self.calculate_positive_reward(starting_distance=self.starting_distance,
                                                    current_distance=distance)
            reward = reward - self.last_reward
            self.last_reward = reward
            return reward
        elif distance > self.last_distance:
            reward = self.calculate_negative_reward(last_distance=self.last_distance,
                                                    current_distance=distance)
            reward = reward + self.last_reward
            self.last_reward = reward
            return reward

    def calculate_positive_reward(self, starting_distance, current_distance):
        """
        Calculate the reward based on the quadratic reward function created here: https://www.desmos.com/calculator/onmokaqme8

        :param starting_distance: Starting distance to goal
        :param current_distance: Current distance to goal

        :return: The current positive reward
        """
        a = 0.25 / starting_distance
        y = a * math.pow((current_distance - starting_distance), 2)

        return y

    def calculate_negative_reward(self, last_distance, current_distance):
        """
        Calculate the negative reward if we move backwards

        :param last_distance: The distance we were at the end of the last step
        :param current_distance: The distance we are now

        :return: The negative reward to apply

        """
        a = 0.1

        y = -a * math.pow((current_distance - last_distance), 2)

        return y

    def get_distance_to_goal(self):
        """
        Get the current distance to the goal

        :return:
        """

        return self.player.get_position().get_distance(self.goal_position)

    def control(self, control_array=None, control_speed=None, left_input=None, right_input=None):
        """
        Control of the agent

        :param control_array: Array of bools saying if it should be moving a certain direction
            0 - Right Forward
            1 - Left Forward
            2 - Right Backwards
            3 - Left Backwards
        :param control_speed: Speed to use to control the player, constant for heuristic controls
        :param left_input: Value to directly apply to the left side of the agent, if set it disables heuristic controls
        :param right_input: Value to directly apply to the right side of the agent, if set it disables heuristic controls

        :return: None
        """

        # If both left_input and right_input have not been set assume we are just using normal control
        if left_input is None and right_input is None:
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
        else:

            # Move Right Side
            self.player.impulse_move(impulse=right_input,
                                     point=(-6, 0),
                                     isWorld=False)

            # Move Left Side
            self.player.impulse_move(impulse=left_input,
                                     point=(6, 0),
                                     isWorld=False)
