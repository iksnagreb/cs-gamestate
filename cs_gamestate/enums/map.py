# Generic enumeration types
from enum import Enum


# Known map phases and their string representation
class MapPhase(Enum):
    WARMUP = "warmup"
    LIVE = "live"
    INTERMISSION = "intermission"
    GAMEOVER = "gameover"


# Known game modes and their string representation
class GameMode(Enum):
    COMPETITIVE = "competitive"
    CASUAL = "casual"
    DEATHMATCH = "deathmatch"
    # TODO: There might be more


# Known round winning conditions and their string representation
class RoundWinCondition(Enum):
    CT_WIN_ELIMINATION = "ct_win_elimination"
    T_WIN_ELIMINATION = "t_win_elimination"
    CT_WIN_DEFUSE = "ct_win_defuse"
    T_WIN_BOMB = "t_win_bomb"
    CT_WIN_TIME = "ct_win_time"
