# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass


# Structure describing the current state of the round
@dataclass
class Round:
    # Current phase of the round: "freezetime", "live" or "over
    #   Note: During timeouts "freezetime" as well
    phase: str = None
    # The winning team at the end of the round: "T" or "CT
    #   Note: None if the round is not over yet
    win_team: str = None
    # Current state of the bomb, only present if the bomb has been planted
    bomb: str = None
