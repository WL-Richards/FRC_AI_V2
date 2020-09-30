"""
Enum of different collision types
"""

__author__ = "Will Richards"
__copyright__ = "Copyright 2020, AEMBOT"

from enum import Enum


class CollisionType(Enum):
    STATIC_OBJECT = 1
    DYNAMIC_OBJECT = 2
    GOAL_OBJECT = 3
