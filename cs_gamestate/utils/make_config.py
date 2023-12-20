# Use the argparse library to set up a command line interface
import argparse

# Structure game state integration service configuration
from cs_gamestate.config import GSIConfig


# Script entrypoint for command line execution
if __name__ == "__main__":
    # Convenience action to set all boolean options registered to True
    class SetAllAction(argparse.BooleanOptionalAction):
        # Method called upon setting the option to which this action is
        # registered
        def __call__(self, p, namespace, values, option_string=None):
            # Run over all options in the namespace
            for option in namespace.__dict__:
                # Only change the value of boolean options
                if isinstance(getattr(namespace, option), bool):
                    # Select the option
                    setattr(namespace, option, True)
            # Remove the auxiliary argument selecting everything
            delattr(namespace, self.dest)


    # Create a new command line parser
    parser = argparse.ArgumentParser()

    # Mandatory arguments to configure name and address of  the service
    parser.add_argument(
        "name", type=str, help="Unique name to identify the service"
    )
    parser.add_argument(
        "uri", type=str, help="Address of the endpoint including port and path"
    )
    # Continuous control variables setting rate and precision of information
    # provided
    continuous = parser.add_argument_group("Rate and resolution")
    continuous.add_argument("--timeout", type=float, default=1.1)
    continuous.add_argument("--buffer", type=float, default=0.1)
    continuous.add_argument("--throttle", type=float, default=0.1)
    continuous.add_argument("--heartbeat", type=float, default=20.0)
    continuous.add_argument("--precision_time", type=float, default=0.01)
    continuous.add_argument("--precision_position", type=float, default=0.1)
    continuous.add_argument("--precision_vector", type=float, default=0.1)
    # Discrete flags subscribing to specific information components
    discrete = parser.add_argument_group(
        "Game state components to subscribe to"
    )
    discrete.add_argument("--provider", action="store_true")
    discrete.add_argument("--player-id", action="store_true")
    discrete.add_argument("--player-state", action="store_true")
    discrete.add_argument("--map", action="store_true")
    discrete.add_argument("--map-round-wins", action="store_true")
    discrete.add_argument("--player-match-stats", action="store_true")
    discrete.add_argument("--player-weapons", action="store_true")
    discrete.add_argument("--round", action="store_true")
    # Discrete flags subscribing to specific information components only
    # available as observer
    discrete = parser.add_argument_group(
        "Observer only game state components to subscribe to"
    )
    discrete.add_argument("--player-position", action="store_true")
    discrete.add_argument("--allgrenades", action="store_true")
    discrete.add_argument("--allplayers-id", action="store_true")
    discrete.add_argument("--allplayers-state", action="store_true")
    discrete.add_argument("--allplayers-match-stats", action="store_true")
    discrete.add_argument("--allplayers-weapons", action="store_true")
    discrete.add_argument("--allplayers-position", action="store_true")
    discrete.add_argument("--bomb", action="store_true")
    discrete.add_argument("--phase-countdowns", action="store_true")

    # Convenience option to select all game state components
    parser.add_argument("--subscribe-to-all", action=SetAllAction)

    # Collect and parse the arguments supplied via command line
    args = parser.parse_args()
    # Remove the "--subscribe-to-all" auxiliary argument
    if hasattr(args, "subscribe_to_all"):
        del args.subscribe_to_all
    # Create a new configuration object from command line arguments unpacked
    # from dictionary to keyword arguments
    config = GSIConfig(**args.__dict__)
    # Print the generated configuration file
    print(config.generate_cfg())
    # Print some instructions on what to do next
    print("\n".join([
        f"// To register this service with the game, place the configuration",
        f"// above as \"gamestate_integration_{args.name}.cfg\" into the",
        f"// game's configuration directory."
    ]))
