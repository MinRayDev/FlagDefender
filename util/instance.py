from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.client import Client
    from core.game import Game


def get_game() -> 'Game':
    from core.game import Game
    return Game.instance


def get_client() -> 'Client':
    from core.client import Client
    return Client.instance
