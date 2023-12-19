# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass

# Game state structures verification utils
from cs_gamestate.structs.verify import VerifiedSubstructures, verify_attribute


# Structure describing the phase countdowns of a round
@dataclass
class PhaseCountdowns(VerifiedSubstructures):
    # The current phase of the round: Similar to the "round" state, but also
    # includes "bomb" when the bomb has been planted, "defuse" when the bomb
    # has been defused and "warmup" during the pre-game warmup period
    phase: str = None
    # Time left before the current phase ends, e.g. time left for planting when
    # the phase is "live" or time left until the bomb explodes if the bomb has
    # been planted and the phase is "bomb"
    phase_ends_in: float = None

    # Tries to verify the validity of the component producing a list of messages
    # if something is not right
    def verify(self):
        # Start collecting messages in list, automate verification of
        # substructures
        messages = super().verify()
        # Verify the current phase against the enum of known phases
        from cs_gamestate.enums.phase import Phase
        messages.extend(verify_attribute(self, Phase, "phase"))
        # Return the collected verification messages
        return messages
