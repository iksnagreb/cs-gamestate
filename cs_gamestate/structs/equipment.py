# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass

# Game state structures verification utils
from cs_gamestate.structs.verify import VerifiedSubstructures, verify_attribute
# Utility functions for initializing the game state structures
from cs_gamestate.structs.utils import none_or_isinstance


# Structure holding information on a single weapon in game
@dataclass
class Weapon(VerifiedSubstructures):
    # Game internal name of the weapon
    name: str = None
    # Game internal name of the skin of the weapon
    #   Note: "default" if the weapon has no skin
    paintkit: str = None
    # Type of the weapon
    type: str = None
    # Current amount of ammunition in the clip
    ammo_clip: int = None
    # Maximum amount of ammunition possible in the clip
    ammo_clip_max: int = None
    # Amount of reserve ammunition available for the weapon
    ammo_reserve: int = None
    # Current state of the weapon: "active" or "holstered"
    state: str = None

    # Tries to verify the validity of the component producing a list of messages
    # if something is not right
    def verify(self):
        # Start collecting messages in list, automate verification of
        # substructures
        messages = super().verify()
        # Verify the weapon is one of the known weapons
        from cs_gamestate.enums.equipment import WeaponName
        messages.extend(verify_attribute(self, WeaponName, "name"))
        # Verify the weapon type is one of the known types
        from cs_gamestate.enums.equipment import WeaponType
        messages.extend(verify_attribute(self, WeaponType, "type"))
        # Verify the weapon state is one of the known valid states
        from cs_gamestate.enums.equipment import WeaponState
        messages.extend(verify_attribute(self, WeaponState, "state"))
        # Return the collected verification messages
        return messages


# Structure holding information on an active grenade effect
@dataclass
class ActiveGrenade(VerifiedSubstructures):
    # Steam ID of the player owning the grenade
    owner: str = None
    # Current position of the grenade in cartesian coordinates
    # Note: Changes over time when the grenade is thrown until it lands or
    # explodes somewhere
    position: tuple[float, ...] = None
    # Current velocity of the grenade in cartesian coordinates
    # Note Changes over time and should correspond to the change in position
    velocity: tuple[float, ...] = None
    # Time since the grenade became active
    lifetime: int = None
    # Type of the grenade: decoy,
    type: str = None
    # Time since the grenade has an effect
    effecttime: int = None
    # Coordinates of each flame piece on the map of molotov/incendiary grenade
    # Note: A dictionary of some flame piece identifier and a coordinate tuple
    flames: dict[str, tuple[float, ...]] = None

    # Tries to verify the validity of the component producing a list of messages
    # if something is not right
    def verify(self):
        # Start collecting messages in list, automate verification of
        # substructures
        messages = super().verify()
        # Verify the grenade type is one of the known types
        from cs_gamestate.enums.equipment import GrenadeType
        messages.extend(verify_attribute(self, GrenadeType, "type"))
        # Return the collected verification messages
        return messages

    # Post-init the dataclass to sanitize not correctly imported substructures
    def __post_init__(self):
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

        # If the velocity has not yet been parsed
        if not none_or_isinstance(self.velocity, tuple):
            # If this is currently a string, it can be reinterpreted as a
            # coordinate tuple
            if isinstance(self.velocity, str):
                # Simple string parsing to separate the two numbers by ,
                self.velocity = tuple(map(float, self.velocity.split(',')))
            # Sometimes the client seems to provide just a boolean
            # for this field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.velocity = None  # noqa

        # Sanitize the flames dictionary if it is present
        if self.flames is not None:
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.flames, dict):
                # Validate each flame piece
                for key, flame in self.flames.items():
                    # If the flame is not coordinate tuple yet
                    if not isinstance(flame, tuple):
                        # If this is currently a string, it can be reinterpreted
                        # as a coordinate tuple
                        if isinstance(flame, str):
                            # Simple string parsing to separate the two numbers
                            # by ,
                            flame = tuple(map(float, flame.split(',')))
                        # Sometimes the client seems to provide just a boolean
                        # for this field (other types possible as well?)
                        else:
                            # Cannot really handle this, treat as "not present"
                            flame = None  # noqa
                    # Reinitialize the flame with key guaranteed to be a string
                    self.flames[str(key)] = flame
            # Sometimes the client seems to provide just a boolean for
            # this field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.flames = None  # noqa


# Structure describing the player's equipment, which is a mapping of weapon
# slots to Weapons
class Equipment(dict[str, Weapon], VerifiedSubstructures):
    # Tries to verify the validity of the component producing a list of messages
    # if something is not right
    def verify(self):
        # Start collecting messages in list, automate verification of
        # substructures
        messages = super().verify()
        # Verifying the player's equipment cannot be automated as it is of type
        # dict
        for slot, weapon in self.items():
            # Verify each weapon using its method and collecting the messages
            messages.extend(
                [f"{self}: {slot}: {msg}" for msg in weapon.verify()]
            )
        # Return the collected verification messages
        return messages

    # Iterates all weapons in the equipment container
    def __iter__(self):
        # Generator dropping the key from the slots
        return (weapon for (_, weapon) in self.items())

    # Gets the weapon at the specified slot by index
    def slot(self, index: int) -> Weapon | None:
        # Check whether the slot is occupied
        if f"weapon_{index}" in self:
            # Return the weapon descriptor at the slot
            return self[f"weapon_{index}"]
        # The slot is not occupied indicate via None value
        return None

    # Get the currently active equipment or weapon
    @property
    def active(self) -> Weapon | None:
        # Iterate all players equipped weapons
        for slot, weapon in self.items():
            # Detect the active item
            if weapon.state == "active":
                # There is always at most one active weapon, thus it is
                # safe to exit with the first one here
                return weapon
        # No weapon is active
        return None

    # Select the subset of grenades from the equipment
    @property
    def grenades(self) -> Equipment:
        # Filter equipment by weapon type
        grenades = {k: v for (k, v) in self.items() if v.type == "Grenade"}
        # Wrap in equipment container
        return Equipment(grenades)
