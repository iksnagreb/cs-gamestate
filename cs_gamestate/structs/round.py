# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass

# Game state structures verification utils
from cs_gamestate.structs.verify import VerifiedSubstructures, verify_attribute


# Structure describing the current state of the round
@dataclass
class Round(VerifiedSubstructures):
    # Current phase of the round: "freezetime", "live" or "over"
    #   Note: During timeouts "freezetime" as well
    phase: str = None
    # The winning team at the end of the round: "T" or "CT
    #   Note: None if the round is not over yet
    win_team: str = None
    # Current state of the bomb, only present if the bomb has been planted
    bomb: str = None

    # Tries to verify the validity of the component producing a list of messages
    # if something is not right
    def verify(self):
        # Start collecting messages in list, automate verification of
        # substructures
        messages = super().verify()
        # Verify the round phase string against the enum
        from cs_gamestate.enums.phase import Phase
        messages.extend(verify_attribute(self, Phase, "phase"))
        # Verify the winning team against the enum of known teams
        from cs_gamestate.enums.team import TeamName
        messages.extend(verify_attribute(self, TeamName, "win_team"))
        # Verify the current bomb state against the enum of known states
        from cs_gamestate.enums.bomb import BombState
        messages.extend(verify_attribute(self, BombState, "bomb"))
        # Return the collected verification messages
        return messages
