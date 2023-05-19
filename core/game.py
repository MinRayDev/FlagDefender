from __future__ import annotations

import time
from typing import Optional

import pygame
from pygame import Surface

from core.chat.chat import Chat
from core.level import Level
from ui.impl.ingame_menu.chat_message import ChatMessageMenu
from ui.impl.ingame_menu.hud import HUD
from ui.menu import Menu
from util.logger import log
from util.time_util import has_elapsed


class Game:
    """Class 'Game'.

        :cvar instance: Game's instance.
        :type instance: Game.
        :cvar name: Game's name.
        :type name: str.
        :cvar version: Game's version.
        :type version: str.

        :ivar is_init: True if the game is inited else False.
        :type is_init: bool.
        :ivar current_menu: Game's current menu.
        :type current_menu: Optional[Menu].
        :ivar run: True if the game is running else False.
        :type run: bool.

        :ivar chat: Game's chat instance.
        :type chat: Chat.
        :ivar chat_menu: Game's chat menu instance.
        :type chat_menu: ChatMessageMenu.
        :ivar hud: Game's HUD instance.
        :type hud: HUD.

        :ivar levels: Game's level list.
        :type levels: list[Level].
        :ivar current_level: Game's current level.
        :type current_level: Level.

        :ivar TPS: Game's tick per second.
        :type TPS: float.

    """
    instance: Game = None
    name: str = "Flag Defender"
    version: str = "1"

    is_init: bool
    current_menu: Optional[Menu]
    run: bool
    chat: Chat
    chat_menu: ChatMessageMenu
    hud: HUD
    levels: list[Level]
    current_level: Optional[Level]
    TPS: float

    def __init__(self):
        """Constructor function for Game class."""
        from ui.impl.main_menu import MainMenu
        self.is_init = False
        self.current_menu = MainMenu()
        self.run = True
        self.chat = Chat()
        self.chat_menu = ChatMessageMenu(self)
        self.hud = HUD()
        self.levels = []
        self.current_level = None
        self.TPS = 60
        self.init_mobs()

    def reset_menu(self) -> None:
        """Reset the current menu."""
        self.current_menu = None

    def set_menu(self, menu: Menu) -> None:
        """Set the current menu.

            :param menu: New menu.
            :type menu: Menu.

        """
        self.current_menu = menu

    def has_menu(self) -> bool:
        """Check if the game has a menu.

            :return: True if game has a menu else False.
            :rtype: bool.

        """
        return self.current_menu is not None

    def create_level(self, name: str = "") -> Level:
        """Create a new level.

            :return: The new level.
            :rtype: Level.

        """
        if name == "":
            name = str(time.time())
        level: Level = Level(name)
        self.levels.append(level)
        self.current_level = level
        return level

    def set_level(self, level: Level) -> None:
        """Set a new level.

            :param level: The new level.
            :type level: Level.

        """
        if level is None:
            log("Attempted to set level to None, prefer using #reset_level()")
        self.levels.append(level)
        self.current_level = level

    def reset_level(self) -> None:
        """Reset current level."""
        self.levels.clear()
        self.current_level = None

    def update_logic(self) -> None:
        """
        Update the game logic.

        This function is called every tick (every 1/60 secondes).
        It calls the activity function of the current menu if it's not None and not an instance of GameMenu.
        Else it calls the activity function of the current level.

        When the current level is not None, it calls the activity function of each entity of each world of the current level.
        Then it calls the activity function of each player of the current level.
        Then it checks if the round is finished and if it is, it calls the next_round function of the round manager.
        If the round is finished and the end_time is 0, it sets the end_time to the current time.
        If the end_time is not 0 and 5 seconds has elapsed, it calls the next_round function of the round manager.

        :return:
        """
        from ui.game_menu import GameMenu
        from entities.livingentities.player_entity import PlayerEntity
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
                for player_ in self.current_level.players:
                    player_.activity()
                    player_.entity.activity(keys=player_.keys, events=player_.events)
                    player_.reset_queues()
                    break
                if self.current_level.round_manager.round_.is_finished():
                    if self.current_level.round_manager.round_.end_time == 0:
                        self.current_level.round_manager.round_.end_time = time.time()
                    if has_elapsed(self.current_level.round_manager.round_.end_time, 5):
                        if self.current_level.round_manager.can_summon:
                            self.current_level.round_manager.next_round()
                for entity in self.current_level.worlds[0].entities:
                    from entities.world_objects.flag import Flag
                    if isinstance(entity, Flag):
                        break
                else:
                    self.current_level.game_over()

    def render(self, surface: Surface) -> None:
        """Render the whole game.

            For each entity for each world, for each menu (current menu if it's an instance of a game menu, HUD, Chat) the code calls its function 'draw'.

        """
        from ui.game_menu import GameMenu
        if isinstance(self.current_menu, GameMenu) or self.current_menu is None:
            # Draw world
            if self.current_level.main_player.entity.world.background is not None:
                self.current_level.main_player.entity.world.background.draw(surface)
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

    @classmethod
    def init_mobs(cls) -> None:
        """Import mobs to initialize them and add them to the registered_entities list."""
        from entities.livingentities.mobs.mob_fly_1 import MobFly1
        from entities.livingentities.mobs.mob_fly_2 import MobFly2
        from entities.livingentities.mobs.mob_tank import MobTank
        from entities.livingentities.mobs.mob_basic import MobBasic
        from entities.livingentities.mobs.mob_mortar import MobMortar
        from entities.livingentities.mobs.mob_speed import MobSpeed
        from entities.livingentities.mobs.mob_speed_physical import MobSpeedPhysical
