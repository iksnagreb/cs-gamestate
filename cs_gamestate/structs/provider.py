# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass

# Game state structures verification utils
from cs_gamestate.structs.verify import VerifiedSubstructures


# Game state structure describing provider information
#   Describes the game, version and time by which the game states are provided
@dataclass
class Provider(VerifiedSubstructures):
    # Name of the game state provider
    name: str = None
    # Steam appid of the game state provider
    #   Note: Should be 730 for Counter Strike
    appid: int = None
    # Version of the app providing the game state
    #   Note: Apparently the version identifier is an integer
    version: int = None
    # Steam ID of the user currently running the game
    #   Note: Apparently the steamid is a string
    steamid: str = None
    # Unis timestamp when this game state has been produced
    timestamp: int = None

    # Tries to verify the validity of the component producing a list of messages
    # if something is not right
    def verify(self):
        # Start collecting messages in list, automate verification of
        # substructures
        messages = super().verify()
        # Counter-Strike should always have the appid 730
        if self.appid != 730:
            # Add verification failure message
            messages.extend([f"{self}: appid is not 730: {self.appid}"])
        # Return the collected verification messages
        return messages
