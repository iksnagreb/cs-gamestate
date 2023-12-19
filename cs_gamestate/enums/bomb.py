# Generic enumeration types
from enum import Enum


# Known bomb states and their string representation
class BombState(Enum):
    CARRIED = "carried"
    DROPPED = "dropped"
    PLANTING = "planting"
    PLANTED = "planted"
    DEFUSING = "defusing"
    DEFUSED = "defused"
    EXPLODED = "exploded"
