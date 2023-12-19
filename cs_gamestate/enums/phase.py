# Generic enumeration types
from enum import Enum


# Known phases and their string representation
class Phase(Enum):
    FREEZETIME = "freezetime"
    LIVE = "live"
    OVER = "over"
    BOMB = "bomb"
    DEFUSE = "defuse"
    WARMUP = "warmup"
