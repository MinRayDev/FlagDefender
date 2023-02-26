from core.client import Client
from core.game import Game


def get_game() -> Game:
    return Game.instance


def get_client() -> Client:
    return Client.instance
