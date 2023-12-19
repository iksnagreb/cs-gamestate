# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass

# Game state structures verification utils
from cs_gamestate.structs.verify import VerifiedSubstructures, verify_attribute
# Utility functions for initializing the game state structures
from cs_gamestate.structs.utils import none_or_isinstance


# Structure describing the "map" of the game which includes more general
# information on the game mode and team state and history as well
@dataclass
class Map(VerifiedSubstructures):
    # Substructure giving information on a team playing on the map
    @dataclass
    class Team:
        # Current score of the team
        score: int = None
        # How many rounds the team has lost in succession
        consecutive_round_losses: int = None
        # Remaining timeouts to be called by the team
        timeouts_remaining: int = None
        # How many games a team has won in a "Best of X" series
        #   Note: Only used for tournaments.
        matches_won_this_series: int = None

    # Name of the map as it is identified for console commands, e.g. de_dust2
    name: str = None
    # The game mode played on the map, e.g., "competitive"
    mode: str = None
    # The current phase of the game on the map:
    #   "warmup", "live", "intermission", "gameover"
    phase: str = None
    # The number of round currently played
    round: int = None
    # Information of the terrorists team
    team_t: Team = None
    # Information on the counter-terrorists team
    team_ct: Team = None
    # History of the match, keeping track of the winning team and condition for
    # each round
    round_wins: dict[int, str] = None
    # How many matches a team has to win before winning the series
    #   Note: Probably only relevant during tournaments
    num_matches_to_win_series: int = None
    # Number of people currently spectating this game
    current_spectators: int = None
    # Number of souvenir cases dropped this game
    #   Note: Probably only relevant during tournaments
    souvenirs_total: int = None

    # Tries to verify the validity of the component producing a list of messages
    # if something is not right
    def verify(self):
        # Start collecting messages in list, automate verification of
        # substructures
        messages = super().verify()
        # Verify the current phase against the enum of known phases
        from cs_gamestate.enums.map import MapPhase
        messages.extend(verify_attribute(self, MapPhase, "phase"))
        # Verify the game mode against the enum of known modes
        from cs_gamestate.enums.map import GameMode
        messages.extend(verify_attribute(self, GameMode, "mode"))
        # Verify each round winning condition against the known conditions
        from cs_gamestate.enums.map import RoundWinCondition
        # If there is a history of round wins
        if self.round_wins is not None:
            # Run over all round number - condition pairs from the history
            for round, condition in self.round_wins.items():  # noqa: Shadows
                # Verify by detecting failure of initializing the enum from the
                # attribute
                try:
                    # Initialize the enum from the attribute value
                    RoundWinCondition(condition)
                # Failing to initialize the enum from the attribute value will
                # be signaled by raising a ValueError
                except ValueError:
                    # Verification failed, return list containing a message
                    # explaining the cause:
                    messages.extend([
                        f"{self}: 'round_wins': {round}: '{condition}' not in"
                        f" {[x.value for x in RoundWinCondition]}"
                    ])
        # Return the collected verification messages
        return messages

    # Post-init the dataclass to sanitize not correctly imported substructures
    def __post_init__(self):
        # If the terrorists team is not an instance of the Team structure,
        # reinitialize it
        if not none_or_isinstance(self.team_t, Map.Team):
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.team_t, dict):
                # It must be a dictionary, reload from dict unpacking
                self.team_t = Map.Team(**self.team_t)
            # Sometimes the client seems to provide just a boolean for this
            # field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.team_t = None  # noqa

        # If the counter-terrorists team is not an instance of the Team
        # structure, reinitialize it
        if not none_or_isinstance(self.team_ct, Map.Team):
            # If it ist a dictionary, this can be unpacked to initialize
            if isinstance(self.team_ct, dict):
                # It must be a dictionary, reload from dict unpacking
                self.team_ct = Map.Team(**self.team_ct)
            # Sometimes the client seems to provide just a boolean for this
            # field (other types possible as well?)
            else:
                # Cannot really handle this, treat as "not present"
                self.team_ct = None  # noqa
