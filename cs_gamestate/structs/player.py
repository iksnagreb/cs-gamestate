# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass

# A player holds equipment and weapons as substructures
from .equipment import Weapon, Equipment

# Utility functions for initializing the game state structures
from .utils import none_or_isinstance


# Game state structure describing player information
@dataclass
class Player:
    # Substructure describing the state of the player in the current round
    @dataclass
    class State:
        # Current level of health of the player
        #   Note: Typically a value between 0 and 100
        health: int = None
        # Current level of armor of the player
        #   Note: Typically a value between 0 and 100
        armor: int = None
        # Flag indicating whether the player is wearing a helmet
        helmet: bool = None
        # The degree to which the player is currently blinded by a flash grenade
        #   Note: Ranges from 0 (not blind) to 255 (fully blind)
        flashed: int = None
        # The degree to which the player's vision is obscured from smoke
        #   Note: Ranges from 0 (clear vision) to 255 (fully obscured vision)
        smoked: int = None
        # The degree to which the player is set on fire
        #   Note: Ranges from 0 (not burning) to 255 (fully on fire)
        #   Note: Practically it seems like 254-0 corresponds to not burning
        #   Note: When set on fire jumps to 255 and starts decreasing once the
        #       player leaves the fire. Probably values 254-0 are for animation.
        burning: int = None
        # Money currently available to the player
        #   Note: Typically between 0 and 16000
        money: int = None
        # Number of kills by the player in the current round
        round_kills: int = None
        # Number of kills by the player made by head-shot in the current round
        #   Note: Should probably be < round_kills
        round_killhs: int = None
        # Total value (in money) of the player's equipment
        equip_value: int = None
        # Total damage dealt by the player in the current round
        round_totaldmg: int = None

    # Substructure describing the stats of the player in the overall match
    @dataclass
    class Stats:
        # Number of kills by the player in the current game
        kills: int = None
        # Number of kill assists by the player in the current game
        assists: int = None
        # Number of deaths of the player in the current game
        deaths: int = None
        # Number of MVPs received by the player in the current game
        mvps: int = None
        # Current score of the player in the game
        score: int = None

    # In-game name of the player
    name: str = None
    # Name of the player's clan
    #   Note: This is optional
    clan: str = None
    # Steam ID of the player
    #   Note: Might differ from the steamid in the provider information
    steamid: str = None
    # Observer slot when spectating the player
    observer_slot: int = None
    # Team the player belongs to: either "T" or "CT", maybe None in menu
    team: str = None
    # Current activity of the player: playing, menu, textinput
    activity: str = None
    # Steam ID of the spectated player
    #   Note: Not yet observed this field in-game
    spectarget: str = None
    # Player position in cartesian coordinates
    position: tuple[float, ...] = None
    # Player forward movement direction
    forward: tuple[float, ...] = None
    # Current player state
    state: State = None
    # Current player stats
    match_stats: Stats = None
    # Weapons equipped by the player
    weapons: Equipment = None

    # Post-init the dataclass to sanitize not correctly imported substructures
    def __post_init__(self):
        # If the state is not an instance of the State structure,
        # reinitialize it
        if not none_or_isinstance(self.state, Player.State):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.state, dict)
            # It must be a dictionary, reload from dict unpacking
            self.state = Player.State(**self.state)

        # If the match stats are not an instance of the Stats structure,
        # reinitialize it
        if not none_or_isinstance(self.match_stats, Player.Stats):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.match_stats, dict)
            # It must be a dictionary, reload from dict unpacking
            self.match_stats = Player.Stats(**self.match_stats)

        # If the player weapons are not an instance of the equipment container,
        # reinitialize it
        if not none_or_isinstance(self.weapons, Equipment):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.weapons, dict)
            # Validate each weapon slot
            for key, weapon in self.weapons.items():
                # If the weapon is not an instance of the Weapon structure,
                # reinitialize it
                if not isinstance(weapon, Weapon):
                    # Something went severely wrong if it is not even a
                    # dictionary
                    assert isinstance(weapon, dict)
                    # It must be a dictionary, reload from dict unpacking
                    weapon = Weapon(**weapon)
                # Reinitialize the weapon slot with key guaranteed to be a
                # string
                self.weapons[str(key)] = weapon
            # Reinterpret the weapons dictionary as the Equipment container,
            # which is derived from dictionary
            self.weapons = Equipment(self.weapons)

        # If the position has not yet been parsed
        if not none_or_isinstance(self.position, tuple):
            # Must currently a string representation
            assert isinstance(self.position, str)
            # Simple string parsing to separate the two numbers by ,
            self.position = tuple(map(float, self.position.split(',')))

        # If the forward direction has not yet been parsed
        if not none_or_isinstance(self.position, tuple):
            # Must currently a string representation
            assert isinstance(self.forward, str)
            # Simple string parsing to separate the two numbers by ,
            self.forward = tuple(map(float, self.forward.split(',')))
