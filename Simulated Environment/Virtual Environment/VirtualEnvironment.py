"""Highest Level Interface For Interaction Between The Arcade Environment And The Neural Net."""

import threading
from ArcadeManager import VirtualEnvironment

env: VirtualEnvironment

def createEnv():
    """
    Create a new arcade environment and set the global variable env to that value

    :return: None
    """
    global env
    env = VirtualEnvironment()


if __name__ == '__main__':

    # Create a thread to run the arcade environment in
    env_thread = threading.Thread(target=createEnv)
    env_thread.start()
