from __future__ import annotations

import base64
import uuid

import pygame
from pygame import Surface

from util import settings
from util.input.controllers import Controller
from util.input.controls import Sources


class Client:
    instance: Client = None

    def __init__(self):
        from util import files
        self.init_game()
        self.screen: Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.init_scrapper()
        self.scroll: int = 0
        self.run: bool = True
        self.online: bool = False
        self.controllers: list[Controller] = []
        self.volume = 100
        self.init_files()
        self.load_settings()
        self.datas = files.get_datas()
        self.id = self.datas["client_id"]
        self.controllers.append(Controller(Sources.keyboard))
        self.controllers.append(Controller(Sources.mouse))

    @classmethod
    def get_screen(cls):
        return Client.instance.screen

    @classmethod
    def init_game(cls):
        from core.game import Game
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(Game.name)

    @classmethod
    def init_scrapper(cls):
        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

    @classmethod
    def init_files(cls):
        from util import files
        if not files.directory_exists(files.get_base_path()):
            files.create_directory(files.get_base_path())
        if not files.directory_exists(files.get_save_path()):
            files.create_directory(files.get_save_path())
        if not files.file_exists(files.get_settings_file()):
            files.create_settings_file()
            settings.write_settings(files.get_settings_file())
        if not files.file_exists(files.get_data_file()):
            files.create_data_file()
            files.write_datas({"client_id": str(base64.b64encode(str(uuid.uuid4()).encode("utf-8")).decode("utf-8")), "user_id": str(uuid.uuid4()), "scores": []})

    @classmethod
    def load_settings(cls):
        from util import files
        settings.load_settings(files.get_settings_file())
