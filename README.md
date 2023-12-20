# cs-gamestate
Counter-Strike Game State Integration for Python: Game State Integration (GSI
for short) allows to receive various types of information, for example the name,
state and match statistics of the player, from a running Counter-Strike game
via the HTTP POST method in JSON format. This package aims to provide
structures, documentation and convenience methods for configuring, receiving and
verifying the GSI in python. To learn more about the Counter-Strike Game State
Integration, have a look at the [Valve Developer Community](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration)
or this [excellent reddit post](https://www.reddit.com/r/GlobalOffensive/comments/cjhcpy/game_state_integration_a_very_large_and_indepth/).

# Installation
> Note: This package is still in early stages of development, installing might
> miss dependencies or does not work at all.
```
pip install cs-gamestate
```

# Configuration
The GSI service needs to be configured in the game configuration directory. The
next time the game is launched, this configuration will be loaded automatically.

To generate a configration, the `make_config` tool provided with this package
can be used, save the generated output as a file
`gamestate_integration_<service-name>.cfg` into the game configuration directory:
```
python -m cs_gamestate.utils.make_config "My GSI Service" http://127.0.0.1:1234/my-gsi --subscribe-to-all
```
This configures a GSI service called "My GSI Service" expecting an endpoint
server running on the localhost, i.e., `127.0.0.1`, listening on port `1234`
where HTTP POST requests are handled under the `/my-gsi` path. This example
service uses default configuration and subscribes to all possible information
components of the game state, even those only available in observer mode.

For more information on the available configuration options, try the `--help`
option of the configuration util, look into the source code or the
aforementioned articles.

# Receiving Game States
Once configured, the game will start transmitting game states as JSON structures
to the specified endpoint address. You can either implement your own service
handling HTTP POST requests under the specified address and process the raw JSON
data, or use the simple server based on
[flask](https://github.com/pallets/flask) provided with this package:
```python
# Game state integration endpoint server
from cs_gamestate.endpoint import GSIServer

# Create an endpoint listening on the specified path and port
server = GSIServer(path="/my-gsi", port=1234)
# Read the next game state received by the server
#   Reset the state buffer and block to only receive unique new states
state = server.read(reset=True, block=True)
```
When running the game and this server on the same host, i.e., the localhost,
this should work with the example configuration as generated above.

The returned state object will be of type
`cs_gamestate.structs.gamestate.GameState`, where subcomponents can be accessed
as object attributes, e.g., `state.player` gives access to the player
subcomponent if it has been subscribed to, otherwise this attribute will be
`None`. The state object can be printed to give a string representation of the
game state or can be converted back to JSON (but including `None` or `null` for
fields which are not present) via `json.dumps(asdict(s))` using the `json`
package and `asdict` from the `dataclasses` package.

The package provides a simple utility program receiving and logging game states
to the console or standard output:
```
python -m cs_gamestate.utils.logger /my-gsi 123
```
This will create a service listening on the localhost, again corresponding to
the example configuration above. Received game states will be printed to the
terminal. Note: this *might* be a lot of output in an active game or just one
update every 30 seconds in the main menu.

# Verifying Game States
This package offers some basic verification of game states against known values
for *some* of the subcomponents, e.g., check received weapon names against the
set of known weapon names collected in `cs_gamestate.enums.equipment`.
Verification is possible via the `verify` method of the `GameState` objects and
yields a list of strings containing a message for each component which cannot
be verified. The `logger` util can be used to verify each game state it receives
by specifiyng the `--verify`command line option, printing verification messages
to the terminal, actually the standard error output, as well.

Please consider reporting any verification issues, especially those regarding
weapon names, types and states still missing in `cs_gamestate.enums` by
opening an issue on the GitHub repository.
