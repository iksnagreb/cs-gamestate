# System to print to standard error stream
import sys
# Use the argparse library to set up a command line interface
import argparse
# Use json so serialize the game state
import json
# Convert structured defined as dataclass to dictionary
from dataclasses import asdict

# Game state integration endpoint server
from cs_gamestate.endpoint import GSIServer

# Script entrypoint for command line execution
if __name__ == "__main__":
    # Create a new command line parser
    parser = argparse.ArgumentParser()
    # Mandatory arguments to configure the address to listen on
    parser.add_argument(
        "path", type=str, help="Path component of the endpoint address"
    )
    parser.add_argument(
        "port", type=int, help="Port on which the server listens"
    )
    # Optional argument specifying JSON formatted output
    parser.add_argument(
        "--json", action="store_true", help="Format output as JSON"
    )
    # Optional argument specifying game state verification output
    parser.add_argument(
        "--verify", action="store_true", help="Verifies each gamestate"
    )
    # Collect and parse the arguments supplied via command line
    args = parser.parse_args()  # @formatter:off Inserts too many newlines here

    # Output formatting auxiliary function, optionally formatting the game state
    # object as json
    def maybe_json(s):
        # If command line argument specifies to produce jason output, convert
        # game state to dictionary and serialize as JSON
        return json.dumps(asdict(s)) if args.json else s
    # @formatter:on

    # Create an endpoint listening on the specified path and port
    server = GSIServer(path=args.path, port=args.port)
    # Log until terminated, e.g., via CTRL+C
    while True:
        # Read the next game state received by the server
        #   Reset the state buffer and block to only receive unique new states
        state = server.read(reset=True, block=True)
        # Optionally verify the gema state
        if args.verify:
            # Print verification to standard error
            print("\n".join(state.verify()), file=sys.stderr)
        # Log the state as string representation to the console output
        print(maybe_json(state))
