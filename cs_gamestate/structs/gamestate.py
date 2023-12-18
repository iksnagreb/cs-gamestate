# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass

# The game state root structure contains the other game state structures as
# sub-fields
from cs_gamestate.structs.provider import Provider
from cs_gamestate.structs.player import Player
from cs_gamestate.structs.bomb import Bomb
from cs_gamestate.structs.round import Round
from cs_gamestate.structs.phase import PhaseCountdowns
from cs_gamestate.structs.map import Map

# Utility functions for initializing the game state structures
from cs_gamestate.structs.utils import none_or_isinstance


# Top-Level Game State Structure
@dataclass
class GameState:
    # Provider of the game state information
    provider: Provider = None
    # The player currently active or spectated
    player: Player = None
    # The current state of the bomb if currently in a match
    bomb: Bomb = None
    # The current state of the round if in a match
    round: Round = None
    # Information of the current phase of a match and when it ends
    phase_countdowns: PhaseCountdowns = None
    # Information of the map (nad game mode, history, ...) if  in a match
    map: Map = None
    # Game state information added in this state, i.e., not present before
    #   Note: Recursively refers to the GameState root
    added: GameState = None
    # Previous game state (only parts which changed in this state)
    #   Note: Recursively refers to the GameState root
    previously: GameState = None
    # Information on currently active grenade effects
    grenades: dict = None
    # Information an all players in the game
    allplayers: dict[str, Player] = None

    # Post-init the structure to sanitize not correctly imported substructures
    def __post_init__(self):
        # Convert the provider information if present but not of the proper type
        # yet
        if not none_or_isinstance(self.provider, Provider):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.provider, dict)
            # It must be a dictionary, reload from dict unpacking
            self.provider = Provider(**self.provider)

        # Convert the player information if present but not of the proper type
        # yet
        if not none_or_isinstance(self.player, Player):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.player, dict)
            # It must be a dictionary, reload from dict unpacking
            self.player = Player(**self.player)

        # Convert the bomb information if present but not of the proper type yet
        if not none_or_isinstance(self.bomb, Bomb):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.bomb, dict)
            # It must be a dictionary, reload from dict unpacking
            self.bomb = Bomb(**self.bomb)

        # Convert the round information if present but not of the proper type
        # yet
        if not none_or_isinstance(self.round, Round):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.round, dict)
            # It must be a dictionary, reload from dict unpacking
            self.round = Round(**self.round)

        # Convert the phase information if present but not of the proper type
        # yet
        if not none_or_isinstance(self.phase_countdowns, PhaseCountdowns):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.phase_countdowns, dict)
            # It must be a dictionary, reload from dict unpacking
            self.phase_countdowns = PhaseCountdowns(**self.phase_countdowns)

        # Convert the map information if present but not of the proper type
        # yet
        if not none_or_isinstance(self.map, Map):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.map, dict)
            # It must be a dictionary, reload from dict unpacking
            self.map = Map(**self.map)

        # If added game state is present but not yet a GameState
        if not none_or_isinstance(self.added, GameState):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.added, dict)
            # It must be a dictionary, reload from dict unpacking
            self.added = GameState(**self.added)

        # If added game state is present but not yet a GameState
        if not none_or_isinstance(self.previously, GameState):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.previously, dict)
            # It must be a dictionary, reload from dict unpacking
            self.previously = GameState(**self.previously)

        # Sanitize the allplayers dictionary if it is present
        if self.allplayers is not None:
            # Validate each allplayers slot
            for key, player in self.allplayers.items():
                # If the player is not an instance of the Player structure,
                # reinitialize it
                if not isinstance(player, Player):
                    # Something went severely wrong if it is not even a
                    # dictionary
                    assert isinstance(player, dict)
                    # It must be a dictionary, reload from dict unpacking
                    player = Player(**player)
                # Reinitialize the player slot with key guaranteed to be a
                # string
                self.allplayers[str(key)] = player
