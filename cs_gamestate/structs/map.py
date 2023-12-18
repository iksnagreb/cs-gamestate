# Postponed evaluation of annotations, allows to type-hint methods with their
# own enclosing class type
from __future__ import annotations
# Use dataclasses to define game state structures
from dataclasses import dataclass

# Utility functions for initializing the game state structures
from .utils import none_or_isinstance


# Structure describing the "map" of the game which includes more general
# information on the game mode and team state and history as well
@dataclass
class Map:
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
    round_wins: tuple[int, str] = None
    # How many matches a team has to win before winning the series
    #   Note: Probably only relevant during tournaments
    num_matches_to_win_series: int = None

    # Post-init the dataclass to sanitize not correctly imported substructures
    def __post_init__(self):
        # If the terrorists team is not an instance of the Team structure,
        # reinitialize it
        if not none_or_isinstance(self.team_t, Map.Team):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.team_t, dict)
            # It must be a dictionary, reload from dict unpacking
            self.team_t = Map.Team(**self.team_t)

        # If the counter-terrorists team is not an instance of the Team
        # structure, reinitialize it
        if not none_or_isinstance(self.team_ct, Map.Team):
            # Something went severely wrong if it is not even a dictionary
            assert isinstance(self.team_ct, dict)
            # It must be a dictionary, reload from dict unpacking
            self.team_ct = Map.Team(**self.team_ct)
