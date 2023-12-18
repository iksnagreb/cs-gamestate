# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass


# Structure describing the phase countdowns of a round
@dataclass
class PhaseCountdowns:
    # The current phase of the round: Similar to the "round" state, but also
    # includes "bomb" when the bomb has been planted, ""defuse" when the bomb
    # has been defused and "warmup" during the pre-game warmup period
    phase: str = None
    # Time left before the current phase ends, e.g. time left for planting when
    # the phase is "live" or time left until the bomb explodes if the bomb has
    # been planted and the phase is "bomb"
    phase_ends_in: float = None
