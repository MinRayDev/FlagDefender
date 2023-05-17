from __future__ import annotations

import base64
import uuid
from typing import Any

import pygame
from pygame import Surface
from pygame.time import Clock

from util import settings
from util.input.controllers import Controller
from util.input.controls import Sources


class Client:
    """Class 'Client'.

        :cvar instance: Client's instance.
        :type instance: Client.

        :ivar screen: Client's screeen.
        :type screen: Surface.
        :ivar clock: Pygame's clock.
        :type clock: Clock.
        :ivar controllers: Client's controllers (ex: keyboard, mouse).
        :type controllers: list[Controller].

        :ivar datas: Client's datas (json format) (ex: client_id, scores, volume).
        :type datas: Any.
        :ivar volume: Client's sound volume.
        :type volume: float.
        :ivar id: Client's ID.
        :type id: str.

    """

    instance: Client = None

    screen: Surface
    clock: Clock
    controllers: list[Controller]
    datas: Any
    volume: float
    id: str

    def __init__(self):
        """Constructor function for Client class."""
        from util import files
        self.init_game()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.init_scrapper()
        self.controllers = []

        self.init_files()
        settings.load_settings(files.get_settings_file())
        self.datas = files.get_datas()
        self.volume = self.datas["volume"]
        self.id = self.datas["client_id"]
        self.controllers.append(Controller(Sources.keyboard))
        self.controllers.append(Controller(Sources.mouse))

    def get_screen(self) -> Surface:
        """Gets client's screen surface.

            :return: Client's screen.
            :rtype: Surface.

        """
        return self.screen

    @classmethod
    def init_game(cls) -> None:
        """Inits pygame.

            Inits pygame and pygame mixer.

        """
        from core.game import Game
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(Game.name)

    @classmethod
    def init_scrapper(cls) -> None:
        """Inits pygame's scrapper."""
        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

    @classmethod
    def init_files(cls) -> None:
        """Inits Game's files."""
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
            files.write_datas({"client_id": str(base64.b64encode(str(uuid.uuid4()).encode("utf-8")).decode("utf-8")), "user_id": str(uuid.uuid4()), "scores": [], "volume": 100})
