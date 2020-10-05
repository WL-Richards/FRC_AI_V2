"""Highest Level Interface For Interaction Between The Arcade Environment And The Neural Net."""

import threading
from time import sleep

from ArcadeManager import VirtualEnvironment

env: VirtualEnvironment = None

ENVIRONMENT_RUNNING = False

def createEnv():
    """
    Create a new arcade environment and set the global variable env to that value

    :param env: Created environment

    :return: None
    """
    global env
    env = VirtualEnvironment()

    global ENVIRONMENT_RUNNING
    ENVIRONMENT_RUNNING = True

    env.startEnvironment()

if __name__ == '__main__':

    # Create a thread to run the arcade environment in
    env_thread = threading.Thread(target=createEnv)
    env_thread.start()

    print("Booting Environment Please Wait...")

    # Wait for environment to start before doing anything
    while not ENVIRONMENT_RUNNING:
        sleep(0.01)

    # Reset player
    obs = env.reset()

    print("Environment Booted!")

    # All Neural Network prediction done after this point

    while True:
        sleep(env.physics_environment.step_length)
        obs, reward, done = env.step(action=(50,50))

        print("Observations: " + str(obs))
        print("Reward: " + str(reward))
        print("Done: " + str(done))

        if done:
            env.reset()

