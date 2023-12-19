# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass

# Game state structures verification utils
from cs_gamestate.structs.verify import VerifiedSubstructures, verify_attribute


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
