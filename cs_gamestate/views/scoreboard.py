# Convert player scores to pandas data frames
import pandas as pd

# Top-Level Game State Structure
from cs_gamestate.structs.gamestate import GameState
# Player information substructure of the game state
from cs_gamestate.structs.player import Player


# Selects those fields of the player structure which belong onto the scoreboard
def select_scores(player: Player):
    # Relevant to the scoreboard are the name, team (for grouping) and stats of
    # the player
    return {
        "name": player.name, "team": player.team, **player.match_stats.__dict__
    }


# Selects the game state subcomponents corresponding to the scoreboard and
# groups players by team
def scoreboard(state: GameState) -> tuple[pd.DataFrame, pd.DataFrame] | None:
    # Scoreboard needs allplayers information
    if state.allplayers is None:
        # Cannot return any scoreboard
        return None
    # Collect the list of scoreboard information for each player
    scores = [
        select_scores(player) for player in state.allplayers.values()
    ]
    # Convert the list of dictionaries to a pandas data frame
    scores = pd.DataFrame(scores)
    # Sort the scoreboard
    scores = scores.sort_values(["score", "kills", "assists"], ascending=False)
    # Create a new index of the sorted data frame
    scores = scores.reset_index(drop=True)
    # Let the index start at 1
    scores.index += 1
    # Group the scores according to team
    scores = scores.groupby("team")
    # Create two separate data frames for each team
    scores_ct, scores_t = scores.get_group("CT"), scores.get_group("T")
    # Return the scores per team
    return scores_ct, scores_t
