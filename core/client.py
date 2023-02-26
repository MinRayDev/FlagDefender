from __future__ import annotations

import base64
import json
import uuid

import pygame
from pygame import Surface, SurfaceType
from core.game import Game
from network.event import EventType

from util.controllers import load_controllers, Controller


class Client:
    instance: Client = None

    def __init__(self):
        from network.websocket_client import WsClient
        self.init_game()
        self.screen: Surface | SurfaceType = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen: Surface | SurfaceType = pygame.display.set_mode((1080, 720))
        self.clock = pygame.time.Clock()
        self.init_scrapper()
        self.scroll: int = 0
        self.run: bool = True
        self.online: bool = False
        self.controllers: list[Controller] = load_controllers()
        self.id: str = base64.b64encode(str(uuid.uuid4()).encode("utf-8")).decode("utf-8")
        self.game_websocket: WsClient = WsClient("127.0.0.1", "5000", self.id)
        self.pseudo: str = "Test-1"
        self.party_id = None
        self.is_party_host: bool = False
        self.init_files()

    @classmethod
    def get_screen(cls):
        return Client.instance.screen

    @classmethod
    def init_game(cls):
        pygame.init()
        pygame.display.set_caption(Game.instance.name)

    @classmethod
    def init_scrapper(cls):
        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

    def start_websocket(self, party_id):
        self.online = True
        self.game_websocket.run(party_id)

    def send_event(self, event: EventType, content):
        if self.online:
            self.game_websocket.send(json.dumps({"event_type": event, "content": content}))

    def is_host(self):
        return not self.online or self.is_party_host

    @classmethod
    def init_files(cls):
        from util import files
        if not files.directory_exists(files.get_base_path()):
            files.create_directory(files.get_base_path())
        if not files.directory_exists(files.get_save_path()):
            files.create_directory(files.get_save_path())
        if not files.file_exists(files.get_settings_file()):
            files.create_settings_file()
