# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass

# Game state structures verification utils
from cs_gamestate.structs.verify import VerifiedSubstructures, verify_attribute
# Utility functions for initializing the game state structures
from cs_gamestate.structs.utils import none_or_isinstance


# Structure describing the state of the bomb
@dataclass
class Bomb(VerifiedSubstructures):
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

    # Tries to verify the validity of the component producing a list of messages
    # if something is not right
    def verify(self):
        # Start collecting messages in list, automate verification of
        # substructures
        messages = super().verify()
        # Verify the current bomb state against the enum of known states
        from cs_gamestate.enums.bomb import BombState
        messages.extend(verify_attribute(self, BombState, "state"))
        # Return the collected verification messages
        return messages

    # Post-init the dataclass to sanitize not correctly imported substructures
    def __post_init__(self):
        # If the position has not yet been parsed
        if not none_or_isinstance(self.position, tuple):
            # If this is currently a string, it can be reinterpreted as a
            # coordinate tuple
            if isinstance(self.position, str):
                # Simple string parsing to separate the two numbers by ,
                self.position = tuple(map(float, self.position.split(',')))
            # Sometimes the client seems to provide just a boolean
            # for this field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.position = None  # noqa
