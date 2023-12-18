# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass

# Utility functions for initializing the game state structures
from .utils import none_or_isinstance


# Structure describing the state of the bomb
@dataclass
class Bomb:
    # The current state of the bomb:
    #   "carried", "dropped", "planting", "planted", "defusing", or "defused"
    state: str = None
    # Bomb position in cartesian coordinates
    position: tuple[float, ...] = None
    # Bombs countdown timer
    #   Note: If state is "planted" this is the time until explosion
    #   Note: If state is "planting" this is the time until fully planted
    #   Note: If state is "defusing" this is the time until fully defused
    countdown: float = None
    # Steam ID of the player currently interacting with the bomb
    #   Note: This can be the carrier, the planter or the defuser
    player: str = None

    # Post-init the dataclass to sanitize not correctly imported substructures
    def __post_init__(self):
        # If the position has not yet been parsed
        if not none_or_isinstance(self.position, tuple):
            # Must currently a string representation
            assert isinstance(self.position, str)
            # Simple string parsing to separate the two numbers by ,
            self.position = tuple(map(float, self.position.split(',')))
