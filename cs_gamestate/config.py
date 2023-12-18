# Use dataclasses to represent structured configuration options
from dataclasses import dataclass


# Configuration file structure with defaults enabling everything
@dataclass
class GSIConfig:
    # Name of the game state integration service to be registered
    #   Note: Multiple services can be registered with the game
    name: str
    # Address of the endpoint server including port and path
    uri: str
    # Time the game waits for the "OK" response from the endpoint
    timeout: float = 1.1
    # The amount of time the game will collect in-game events before sending the
    # next state update
    buffer: float = 0.1
    # Do not send another game state update for this period of time after
    # receiving the "OK" response from the endpoint
    throttle: float = 0.1
    # Period of heartbeat signale, i.e., transmitting a game state update even
    # if not state has actually changed
    heartbeat: float = 30.0

    # Precision of time information included in the game state
    precision_time: float = 0.01
    # Precision of position information included in the game state
    precision_position: float = 0.1
    # Precision of vector information included in the game state
    precision_vector: float = 0.1

    # Subscribes to the provider information
    provider: bool = True
    # Subscribes to the player ID
    player_id: bool = True
    # Subscribes to the player state
    player_state: bool = True
    # Subscribes to the map information
    map: bool = True
    # Subscribes to the history of round wins on the map
    map_round_wins: bool = True
    # Subscribes to the player match statistics
    player_match_stats: bool = True
    # Subscribes to the player weapons information
    player_weapons: bool = True
    # Subscribes to the current round information
    round: bool = True

    # The following components are only available when spectating or replaying a
    # game recording

    # Subscribes to the player position information
    player_position: bool = True

    # Subscribes to the information on all currently active grenade effects
    allgrenades: bool = True
    # Subscribes to all player IDs in the game
    allplayers_id: bool = True
    # Subscribes to all players states
    allplayers_state: bool = True
    # Subscribes to all players match statistics
    allplayers_match_stats: bool = True
    # Subscribes to all players weapons
    allplayers_weapons: bool = True
    # Subscribes to all players positions
    allplayers_position: bool = True
    # Subscribes to the bomb state and information
    bomb: bool = True
    # Subscribes to phase countdowns of a round
    phase_countdowns: bool = True

    # Generates the configuration file
    def generate_cfg(self):
        # Converts a named config attribute to the configuration string
        def set_cfg(name):
            # Represents booleans as "1" or "0"
            def bool_as_int(flag):
                return int(flag) if (type(flag) is bool) else flag

            # Format the configuration option as a string following the "cfg"
            return f'"{name}" "{bool_as_int(getattr(self, name))}"'

        # Collect all configuration file lines as a list
        cfg = [
            # Start the configuration block of this service
            f"\"{self.name}\"",
            f"{{",
            # Configure the endpoint and the rate at which information shall be
            # transmitted
            set_cfg("uri"),
            set_cfg("timeout"),
            set_cfg("buffer"),
            set_cfg("throttle"),
            set_cfg("heartbeat"),
            # Configure the output section setting the resolution of
            # information
            f"\"output\"",
            f"{{",
            set_cfg("precision_time"),
            set_cfg("precision_position"),
            set_cfg("precision_vector"),
            # End of output section
            f"}}",
            # Configure the data section specifying to which components to
            # subscribe
            f"\"data\"",
            f"{{",
            set_cfg("provider"),
            set_cfg("player_id"),
            set_cfg("player_state"),
            set_cfg("map"),
            set_cfg("map_round_wins"),
            set_cfg("player_match_stats"),
            set_cfg("player_weapons"),
            set_cfg("round"),
            set_cfg("player_position"),
            set_cfg("allgrenades"),
            set_cfg("allplayers_id"),
            set_cfg("allplayers_state"),
            set_cfg("allplayers_match_stats"),
            set_cfg("allplayers_weapons"),
            set_cfg("allplayers_position"),
            set_cfg("bomb"),
            set_cfg("phase_countdowns"),
            # End of data section
            f"}}",
            # End the outer block of the service
            f"}}",
            # Close with an empty line
            f""
        ]

        # Join all lines into single string separated by newlines
        return "\n".join(cfg)
