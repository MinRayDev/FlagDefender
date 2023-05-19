from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.client import Client
    from core.game import Game


def get_game() -> 'Game':
    """Returns the game instance."""
    from core.game import Game
    return Game.instance


def get_client() -> 'Client':
    """Returns the client instance."""
    from core.client import Client
    return Client.instance
