from __future__ import annotations

from typing import Optional

import pygame

from core.menus.menu import Menu
from network.websocket_client import WsClient
from utils.controllers import load_controllers
import core.world


class Game:
    instance: Game = None

    def __init__(self):
        self.name = "UwU"
        self.version = "0.0.1"
        self.menus = []
        self.actual_menu: Optional[Menu] = None
        self.worlds = [core.world.World("overworld", 80, (5000, 720))]
        self.queue = []
        self.controllers = load_controllers()
        self.actual_world = self.worlds[0]
        self.online = False
        self.game_websocket = WsClient("127.0.0.1", "5000")
        if self.online:
            self.game_websocket.run()
        self.screen = pygame.display.set_mode((1080, 720))
        self.players: list = []
        self.TPS: float = 60
        self.scroll = 0
        self.run = True
        self.main_player = None
        # win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def reset_world(self):
        self.actual_world = None

    def reset_menu(self):
        self.actual_menu = None

    def set_menu(self, menu: Menu):
        self.actual_menu = menu