"""
Counter-Strike Game State Integration Server
"""

# Run server in separate thread
import threading
# HTTP server (endpoint for game state integration POST requests)
from flask import Flask, request

# Top-Level Game State Structure
from cs_gamestate.structs.gamestate import GameState


# Counter Strike: Game State Integration Server
#   HTTP POST endpoint
class GSIServer:
    """
    HTTP POST request endpoint server for Counter-Strike: Game State Integration
    requests run in a separate thread.
    """

    # Configures game state integration service
    def __init__(self, path, port):
        """
        Initializes the HTTP server, current game state and thread lock for
        accessing the game state
        """
        # Current game state
        self.state = None
        # Thread lock to synchronize access to the game state
        self.lock = threading.Lock()

        # Server thread running Flask in the background
        def server():
            # Setup flask http service
            _server = Flask(__name__)

            # Handle HTTP POST request to the specified path
            @_server.route(path, methods=['POST'])
            def post():
                # Lock access to the game state
                with self.lock:
                    # Interpret request as json and write to wrapping object
                    self.state = request.get_json()
                # Send response
                return 'OK'

            # Run the flask service listening on the specified port
            _server.run(port=port)

        # Create and start server thread
        threading.Thread(target=server, daemon=True).start()

    # Reads the current game state if available
    def read(self, reset=False, block=False):
        """
        Reads the current game state.
        :param reset: Reset the state to None after the access
        :param block: Block while there is no game state
        :return: Returns the current game state as a GameState object
        """
        # Wait for new current state
        while block and not self.state:
            pass
        # Get the current state
        state = self.state
        # Reset current state (if not already being set by server thread)
        if reset and self.lock.acquire(blocking=False):
            # Set state back to None (empty)
            self.state = None
            # Release access to the game state
            self.lock.release()
        # Return the current state
        return GameState(**state)
