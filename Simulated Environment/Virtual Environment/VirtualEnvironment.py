"""Highest Level Interface For Interaction Between The Arcade Environment And The Neural Net."""

import threading
from time import sleep

from ArcadeManager import VirtualEnvironment

env: VirtualEnvironment = None

def createEnv():
    """
    Create a new arcade environment and set the global variable env to that value

    :param env: Created environment

    :return: None
    """
    global env
    env = VirtualEnvironment()
    env.startEnvironment()

if __name__ == '__main__':

    # Create a thread to run the arcade environment in
    env_thread = threading.Thread(target=createEnv)
    env_thread.start()

    print("Booting Environment Please Wait...")
    # Wait for environment to boot
    sleep(3)

    env.player.set_rotational_offset(offset=90)

    print("Environment Booted!")

    while True:
        # Calls to a debug method one level lower to allow for easy debugging
        env.debug()
