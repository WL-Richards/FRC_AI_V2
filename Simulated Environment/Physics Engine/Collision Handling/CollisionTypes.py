"""
Enum of different collision types
"""

from enum import Enum
class CollisionType(Enum):
    STATIC_OBJECT = 1
    DYNAMIC_OBJECT = 2
    GOAL_OBJECT = 3