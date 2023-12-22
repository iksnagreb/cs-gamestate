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
from cs_gamestate.structs.equipment import ActiveGrenade
# Game state structures verification utils
from cs_gamestate.structs.verify import VerifiedSubstructures
# Utility functions for initializing the game state structures
from cs_gamestate.structs.utils import none_or_isinstance


# Top-Level Game State Structure
@dataclass
class GameState(VerifiedSubstructures):
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
    #   Note: Structure similar to GameState but fields con only be "true"
    added: dict = None
    # Previous game state (only parts which changed in this state)
    #   Note: Recursively refers to the GameState root
    previously: GameState = None
    # Information on currently active grenade effects
    grenades: dict[str, ActiveGrenade] = None
    # Information an all players in the game
    allplayers: dict[str, Player] = None

    # Tries to verify the validity of the component producing a list of messages
    # if something is not right
    def verify(self):
        # Start collecting messages in list, automate verification of
        # substructures
        messages = super().verify()
        # The "allplayers" field must be verified separately if it is present
        if self.allplayers is not None:
            # Verifying the "allplayers" field cannot be automated as it is of
            # type dict
            for name, player in self.allplayers.items():
                # Verify each player using its method and collecting the
                # messages
                messages.extend(
                    [f"allplayers: {name}: {msg}" for msg in player.verify()]
                )
        # The "grenades" field must be verified separately if it is present
        if self.grenades is not None:
            # Verifying the "grenades" field cannot be automated as it is of
            # type dict
            for name, grenade in self.grenades.items():
                # Verify each grenade using its method and collecting the
                # messages
                messages.extend(
                    [f"grenades: {name}: {msg}" for msg in grenade.verify()]
                )
        # Return the collected verification messages
        return messages

    # Post-init the structure to sanitize not correctly imported substructures
    def __post_init__(self):
        # Convert the provider information if present but not of the proper type
        # yet
        if not none_or_isinstance(self.provider, Provider):
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.provider, dict):
                # It must be a dictionary, reload from dict unpacking
                self.provider = Provider(**self.provider)
            # Sometimes the client seems to provide just a boolean for this
            # field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.provider = None  # noqa

        # Convert the player information if present but not of the proper type
        # yet
        if not none_or_isinstance(self.player, Player):
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.player, dict):
                # It must be a dictionary, reload from dict unpacking
                self.player = Player(**self.player)
            # Sometimes the client seems to provide just a boolean for this
            # field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.player = None  # noqa

        # Convert the bomb information if present but not of the proper type yet
        if not none_or_isinstance(self.bomb, Bomb):
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.bomb, dict):
                # It must be a dictionary, reload from dict unpacking
                self.bomb = Bomb(**self.bomb)
            # Sometimes the client seems to provide just a boolean for this
            # field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.bomb = None  # noqa

        # Convert the round information if present but not of the proper type
        # yet
        if not none_or_isinstance(self.round, Round):
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.round, dict):
                # It must be a dictionary, reload from dict unpacking
                self.round = Round(**self.round)
            # Sometimes the client seems to provide just a boolean for this
            # field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.round = None  # noqa

        # Convert the phase information if present but not of the proper type
        # yet
        if not none_or_isinstance(self.phase_countdowns, PhaseCountdowns):
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.phase_countdowns, dict):
                # It must be a dictionary, reload from dict unpacking
                self.phase_countdowns = PhaseCountdowns(**self.phase_countdowns)
            # Sometimes the client seems to provide just a boolean for this
            # field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.phase_countdowns = None  # noqa

        # Convert the map information if present but not of the proper type
        # yet
        if not none_or_isinstance(self.map, Map):
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.map, dict):
                # It must be a dictionary, reload from dict unpacking
                self.map = Map(**self.map)
            # Sometimes the client seems to provide just a boolean for this
            # field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.map = None  # noqa

        # # If added game state is present but not yet a GameState
        # if not none_or_isinstance(self.added, GameState):
        #     # If it ist a dictionary, this can be unpacked to initialize
        #     if isinstance(self.added, dict):
        #         # It must be a dictionary, reload from dict unpacking
        #         self.added = GameState(**self.added)
        #     # Sometimes the client seems to provide just a boolean for this
        #     # field (other types possible as well?)
        #     else:
        #         # Cannot really handle this, treat as "not present"
        #         self.added = None  # noqa

        # If previous game state is present but not yet a GameState
        if not none_or_isinstance(self.previously, GameState):
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.previously, dict):
                # It must be a dictionary, reload from dict unpacking
                self.previously = GameState(**self.previously)
            # Sometimes the client seems to provide just a boolean for this
            # field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.previously = None  # noqa

        # Sanitize the allplayers dictionary if it is present
        if self.allplayers is not None:
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.allplayers, dict):
                # Validate each allplayers slot
                for key, player in self.allplayers.items():
                    # If the player is not an instance of the Player structure,
                    # reinitialize it
                    if not isinstance(player, Player):
                        # If it ist a dictionary, this can be unpacked to
                        # initialize
                        if isinstance(player, dict):
                            # It must be a dictionary, reload from dict
                            # unpacking
                            player = Player(**player)
                        # Sometimes the client seems to provide just a boolean
                        # for this field (other types possible as well?)
                        else:
                            # Cannot really handle this, treat as "not present"
                            player = None  # noqa
                    # Reinitialize the player slot with key guaranteed to be a
                    # string
                    self.allplayers[str(key)] = player
            # Sometimes the client seems to provide just a boolean for
            # this field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.allplayers = None  # noqa

        # Sanitize the active grenades dictionary if it is present
        if self.grenades is not None:
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.grenades, dict):
                # Validate each grenades slot
                for key, grenade in self.grenades.items():
                    # If the grenade is not an instance of the ActiveGrenade
                    # structure, reinitialize it
                    if not isinstance(grenade, ActiveGrenade):
                        # If it ist a dictionary, this can be unpacked to
                        # initialize
                        if isinstance(grenade, dict):
                            # It must be a dictionary, reload from dict
                            # unpacking
                            grenade = ActiveGrenade(**grenade)
                        # Sometimes the client seems to provide just a boolean
                        # for this field (other types possible as well?)
                        else:
                            # Cannot really handle this, treat as "not present"
                            grenade = None  # noqa
                    # Reinitialize the grenade with key guaranteed to be a
                    # string
                    self.grenades[str(key)] = grenade
            # Sometimes the client seems to provide just a boolean for
            # this field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.grenades = None  # noqa
