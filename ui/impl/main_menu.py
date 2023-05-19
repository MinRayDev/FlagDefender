from __future__ import annotations

import time

import pygame
from pygame import Surface

from ui.element.impl.button_text import ButtonText
from ui.impl.rules_menu import RulesMenu
from ui.impl.score_menu import ScoreMenu
from ui.impl.settings.general_settings import GeneralSettingsMenu
from ui.impl.world_menu import WorldMenu
from ui.menu import Menu
from util.colors import Colors
from util.instance import get_game, get_client
from util.sprites import load
from util.time_util import has_elapsed


class MainMenu(Menu):
    """Class 'MainMenu' is the main menu of the game.

        Extends the class 'Menu'.
        :ivar solo_button: The button to go to the world menu.
        :type solo_button: ButtonText.
        :ivar multi_button: The button to go to the score menu.
        :type multi_button: ButtonText.
        :ivar settings_button: The button to go to the settings menu.
        :type settings_button: ButtonText.
        :ivar rules_button: The button to go to the rules menu.
        :type rules_button: ButtonText.
        :ivar score_button: The button to go to the score menu.
        :type score_button: ButtonText.
        :ivar exit_button: The button to exit the game.
        :type exit_button: ButtonText.

    """
    bg: MenuBackground
    solo_button: ButtonText
    multi_button: ButtonText
    settings_button: ButtonText
    rules_button: ButtonText
    score_button: ButtonText
    exit_button: ButtonText

    def __init__(self):
        """Constructor of the class 'MainMenu'."""
        super().__init__("Main Menu", None)
        base_color: tuple[int, int, int] = Colors.base_color
        hover_color: tuple[int, int, int] = Colors.hover_color
        text_color: tuple[int, int, int] = Colors.text_color
        space: int = 15
        self.frame = 0
        self.bg = MenuBackground()
        width_base = 500
        self.solo_button = ButtonText("CENTER", get_client().get_screen().get_height()//2-80*2-40 - space*2, width_base, 80, "Solo", base_color, text_color)
        self.solo_button.click = lambda: get_game().set_menu(WorldMenu(self))
        self.solo_button.hover_color = hover_color

        self.multi_button = ButtonText("CENTER", get_client().get_screen().get_height()//2-80-40 - space, width_base, 80, "Scores", base_color, text_color)
        self.multi_button.click = lambda: get_game().set_menu(ScoreMenu(self))
        self.multi_button.hover_color = hover_color

        self.rules_button = ButtonText("CENTER", "CENTER", width_base, 80, "Rules", base_color, text_color)
        self.rules_button.click = lambda: get_game().set_menu(RulesMenu(self))
        self.rules_button.hover_color = hover_color

        self.settings_button = ButtonText(get_client().get_screen().get_width()//2 - width_base//2, get_client().get_screen().get_height()//2+40 + space, (width_base-space//2)//2, 80, "Settings", base_color, text_color)
        self.settings_button.click = lambda: get_game().set_menu(GeneralSettingsMenu(self))
        self.settings_button.hover_color = hover_color

        self.leave_button = ButtonText(get_client().get_screen().get_width()//2 + space//2, get_client().get_screen().get_height() // 2 + 40 + space, (width_base-space)//2, 80, "Leave", base_color, text_color)
        self.leave_button.click = lambda: exit(-1)
        self.leave_button.hover_color = hover_color

        self.elems = [self.solo_button, self.rules_button, self.multi_button, self.settings_button, self.leave_button]

    def activity(self) -> None:
        """Method to update the menu."""
        inputs = self.get_queue()
        for elem in self.elems:
            elem.activity(inputs)
            pass

        for elem in self.elems:
            if elem.hover() is not None and get_game().current_menu is not None:
                if pygame.mouse.get_cursor() != elem.hover():
                    pygame.mouse.set_cursor(elem.hover())
                    break
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, surface: Surface) -> None:
        """Method to draw the menu.

            :param surface: The surface to draw on.
            :type surface: Surface.

        """
        pygame.draw.rect(surface, Colors.base_color, pygame.Rect(0, 0, get_client().get_screen().get_width(), get_client().get_screen().get_height()))
        self.bg.draw(surface)
        super().draw(surface)
        self.frame += 1


class MenuBackground:
    """Class 'OverworldBackground'.

        OverworldBackground class is the class for background of the overworld.

        :ivar __last_time: Time of the last time the sprite was modified.
        :type __last_time: float.
        :ivar __last_sprite: Last sprite indexes.
        :type __last_sprite: int.

        :ivar __parts: List of parts making up the background.
        :type __parts: list[Surface].
        :ivar __ratios: List of ratios modifying the scroll.
        :type __ratios: list[float].

    """
    __last_time: float
    __last_sprite: int
    __parts: list[Surface]
    __ratios: list[float]

    def __init__(self):
        """Constructor of the class 'MenuBackground'."""
        self.__last_time = 0
        self.__last_sprite = 2

        surface = get_client().get_screen()
        self.sprites = load(r"./resources/sprites/world/background")
        self.__parts = [
            self.resize(self.sprites["0"], surface.get_width()),
            self.resize(self.sprites["1"], int(surface.get_width() * 1.2)),
            self.resize(self.sprites["20"], int(surface.get_width() * 1.6)),
            self.resize(self.sprites["21"], int(surface.get_width() * 1.6)),
            self.resize(self.sprites["22"], int(surface.get_width() * 1.6)),
            self.resize(self.sprites["23"], int(surface.get_width() * 1.6))
        ]
        self.__ratios = [
            (surface.get_width() / ((11200 * 2 + self.__parts[1].get_width() * 2) * 2 + 11200 / 1.5)) * 0.2,
            (surface.get_width() / ((11200 * 2 + self.__parts[2].get_width() * 2) * 2 + 11200 / 4))
        ]

    def draw(self, surface: Surface) -> None:
        """Draw this object on the client's screen.

            :param surface: Surface to draw.
            :type surface: Surface.

        """
        surface.fill((130, 240, 255))
        surface.blit(self.__parts[0], (0, surface.get_height() - self.__parts[0].get_height() * 1.5))
        surface.blit(
            self.__parts[1],
            (
                - ((self.__parts[1].get_width() - surface.get_width()) // 2) *
                self.__ratios[0] - 25 // 2,
                surface.get_height() - self.__parts[1].get_height() / 2.2
            )
        )
        surface.blit(
            self.__parts[self.__last_sprite],
            (
                - ((self.__parts[2].get_width() - surface.get_width()) // 2) *
                self.__ratios[1] - 25 // 2,
                surface.get_height() - self.__parts[2].get_height() // 2.9
            )
        )

        if has_elapsed(self.__last_time, 0.2):
            self.__last_time = time.time()
            self.__last_sprite += 1
            if self.__last_sprite > 5:
                self.__last_sprite = 2

    @classmethod
    def resize(cls, to_resize: Surface, new_width: int) -> Surface:
        """Resize 'to_resize' with the new width.

            :param to_resize: Surface to resize.
            :type to_resize: Surface.
            :param new_width: Surface's new width.
            :type new_width: int.

        """
        ratio = new_width / to_resize.get_width()
        return pygame.transform.scale(to_resize, (new_width, to_resize.get_height() * ratio))