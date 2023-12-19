# Generic enumeration types
from enum import Enum


# Known round phases and their string representation
class RoundPhase(Enum):
    FREEZETIME = "freezetime"
    LIVE = "live"
    OVER = "over"
