from __future__ import annotations

import time
from typing import Optional

import pygame
from pygame import Surface

from core.chat.chat import Chat
from core.level import Level
from core.ui.impl.ingame_menu.chat_message import ChatMessageMenu
from core.ui.impl.ingame_menu.hud import HUD
from core.ui.menu import Menu
from util.time_util import has_elapsed


class Game:
    instance: Game = None
    name: str = "UwU"
    version: str = "0.0.1"

    def __init__(self):
        from core.ui.impl.main_menu import MainMenu
        self.is_init = False
        self.current_menu: Optional[Menu] = MainMenu()
        self.run: bool = True
        self.chat: Chat = Chat()
        self.chat_menu = ChatMessageMenu(self)
        self.hud = HUD()
        self.levels: list[Level] = []
        self.current_level: Optional[Level] = None
        self.TPS: float = 60

        # win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def reset_menu(self) -> None:
        self.current_menu = None

    def set_menu(self, menu: Menu) -> None:
        self.current_menu = menu

    def has_menu(self) -> bool:
        return self.current_menu is not None

    def create_level(self, name="") -> Level:
        if name == "":
            name = str(time.time())
        level: Level = Level(name)
        self.levels.append(level)
        self.current_level = level
        return level

    def set_level(self, level: Level) -> None:
        if level is None:
            print("Attempted to set level to None, prefer using #reset_level()")
        self.levels.append(level)
        self.current_level = level

    def reset_level(self) -> None:
        print("Reset level")
        self.levels.clear()
        self.current_level = None

    def update_logic(self):
        from core.ui.game_menu import GameMenu
        from entities.livingentities.entity_player import PlayerEntity
        if self.current_menu is not None and not isinstance(self.current_menu, GameMenu):
            self.current_menu.activity()
        else:
            if not self.is_init:
                self.current_level.day_start = time.time()
                self.is_init = True

            if isinstance(self.current_menu, GameMenu):
                self.current_menu.activity()
            if self.current_level is not None:
                for world in self.current_level.worlds:
                    if world.has_player():
                        for entity_ in world.entities:
                            if not isinstance(entity_, PlayerEntity) and entity_.source == 0:
                                entity_.activity()
                if self.current_level is not None:
                    for player_ in self.current_level.players:
                        player_.activity()
                        player_.entity.activity(keys=player_.keys, events=player_.events)
                        player_.reset_queues()
                        break
                    if self.current_level.round_manager.round.is_finished():
                        if self.current_level.round_manager.round.end_time == 0:
                            self.current_level.round_manager.round.end_time = time.time()
                        if has_elapsed(self.current_level.round_manager.round.end_time, 5):
                            if self.current_level.round_manager.can_summon:
                                self.current_level.round_manager.next_round()

    def render(self, surface: Surface) -> None:
        from core.ui.game_menu import GameMenu
        if isinstance(self.current_menu, GameMenu) or self.current_menu is None:
            # Draw world
            if self.current_level.main_player.entity.world.background is not None:
                self.current_level.main_player.entity.world.background.draw(surface)
            # floor.draw(client.screen)

            for entity in self.current_level.main_player.entity.world.entities:
                entity.draw(surface)
            if self.current_level.main_player.entity.world.name == "overworld":
                if self.current_level.is_day():
                    if self.current_level.skycolor_alpha > 0:
                        s = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
                        self.current_level.skycolor_alpha -= 2
                        s.fill((0, 0, 20, self.current_level.skycolor_alpha))
                        surface.blit(s, (0, 0))
                if self.current_level.day_start + self.current_level.day_duration < time.time() < self.current_level.day_start + self.current_level.day_duration * 1.5:
                    s = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
                    if self.current_level.skycolor_alpha < 170:
                        self.current_level.skycolor_alpha += 2
                    s.fill((0, 0, 20, self.current_level.skycolor_alpha))
                    surface.blit(s, (0, 0))
            if self.current_level.day_start + self.current_level.day_duration * 1.5 < time.time():
                self.current_level.day_start = time.time()
            self.chat_menu.draw(surface)
            self.hud.draw(surface)
        if self.current_menu is not None:
            self.current_menu.draw(surface)
