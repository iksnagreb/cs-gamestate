# Generic enumeration types
from enum import Enum


# Known player activities and their string represnetation
class PlayerActivity(Enum):
    PLAYING = "playing"
    MENU = "menu"
    TEXTINPUT = "textinput"
