# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass


# Game state structure describing provider information
#   Describes the game, version and time by which the game states are provided
@dataclass
class Provider:
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
