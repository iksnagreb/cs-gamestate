# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass

# A player holds equipment and weapons as substructures
from cs_gamestate.structs.equipment import Weapon, Equipment
# Game state structures verification utils
from cs_gamestate.structs.verify import VerifiedSubstructures, verify_attribute
# Utility functions for initializing the game state structures
from cs_gamestate.structs.utils import none_or_isinstance


# Game state structure describing player information
@dataclass
class Player(VerifiedSubstructures):
    # Substructure describing the state of the player in the current round
    @dataclass
    class State(VerifiedSubstructures):
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
        # Specifies whether the player is carrying a defusekit
        defusekit: bool = None

    # Substructure describing the stats of the player in the overall match
    @dataclass
    class Stats(VerifiedSubstructures):
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

    # Tries to verify the validity of the component producing a list of messages
    # if something is not right
    def verify(self):
        # Start collecting messages in list, automate verification of
        # substructures
        messages = super().verify()
        # Verify the player's team against the enum of known teams
        from cs_gamestate.enums.team import TeamName
        messages.extend(verify_attribute(self, TeamName, "team"))
        # Verify the player's activity against the enum of known activities
        from cs_gamestate.enums.player import PlayerActivity
        messages.extend(verify_attribute(self, PlayerActivity, "activity"))
        # Return the collected verification messages
        return messages

    # Post-init the dataclass to sanitize not correctly imported substructures
    def __post_init__(self):
        # If the state is not an instance of the State structure,
        # reinitialize it
        if not none_or_isinstance(self.state, Player.State):
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.state, dict):
                # It must be a dictionary, reload from dict unpacking
                self.state = Player.State(**self.state)
            # Sometimes the client seems to provide just a boolean for this
            # field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.state = None  # noqa

        # If the match stats are not an instance of the Stats structure,
        # reinitialize it
        if not none_or_isinstance(self.match_stats, Player.Stats):
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.match_stats, dict):
                # It must be a dictionary, reload from dict unpacking
                self.match_stats = Player.Stats(**self.match_stats)
            # Sometimes the client seems to provide just a boolean for this
            # field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.match_stats = None  # noqa

        # If the player weapons are not an instance of the equipment container,
        # reinitialize it
        if not none_or_isinstance(self.weapons, Equipment):
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.weapons, dict):
                # Validate each weapon slot
                for key, weapon in self.weapons.items():
                    # If the weapon is not an instance of the Weapon structure,
                    # reinitialize it
                    if not isinstance(weapon, Weapon):
                        # If it ist a dictionary, this can be unpacked to
                        # initialize
                        if isinstance(weapon, dict):
                            # It must be a dictionary, reload from dict
                            # unpacking
                            weapon = Weapon(**weapon)
                        # Sometimes the client seems to provide just a boolean
                        # for this field (other types possible as well?)
                        else:
                            # Cannot really handle this, treat as "not present"
                            weapon = None  # noqa
                    # Reinitialize the weapon slot with key guaranteed to be a
                    # string
                    self.weapons[str(key)] = weapon
                # Reinterpret the weapons dictionary as the Equipment container,
                # which is derived from dictionary
                self.weapons = Equipment(self.weapons)

        # If the position has not yet been parsed
        if not none_or_isinstance(self.position, tuple):  # noqa Duplicate
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

        # If the forward direction has not yet been parsed
        if not none_or_isinstance(self.forward, tuple):
            # If this is currently a string, it can be reinterpreted as a
            # coordinate tuple
            if isinstance(self.forward, str):
                # Simple string parsing to separate the two numbers by ,
                self.forward = tuple(map(float, self.forward.split(',')))
            # Sometimes the client seems to provide just a boolean
            # for this field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.forward = None  # noqa
