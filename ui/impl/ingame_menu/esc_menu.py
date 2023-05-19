from __future__ import annotations

import time

import pygame
from pygame import Surface

from ui.element.impl.button_text import ButtonText
from ui.element.impl.notification import info
from ui.game_menu import GameMenu
from ui.impl.main_menu import MainMenu
from ui.impl.settings.general_settings import GeneralSettingsMenu
from util.colors import Colors
from util.instance import get_game, get_client
from util.time_util import has_elapsed


def save_game(menu: EscMenu) -> None:
    """Saves the game.

        :param menu: The menu.
        :type menu: EscMenu.

    """
    game = get_game()
    game.current_level.save()
    info(menu, "Game saved")


def leave() -> None:
    """Leaves the game."""
    get_game().set_menu(MainMenu())
    time.sleep(0.02)
    get_game().reset_level()


class EscMenu(GameMenu):
    """Class 'EscMenu' is the menu when the player presses the escape key.

        Extends the class 'GameMenu'.
        :ivar continue_button: The button to continue the game.
        :type continue_button: ButtonText.
        :ivar save_button: The button to save the game.
        :type save_button: ButtonText.
        :ivar settings_button: The button to go to the settings menu.
        :type settings_button: ButtonText.
        :ivar leave_button: The button to leave the game.
        :type leave_button: ButtonText.
        :ivar time_: The time.
        :type time_: float.

    """
    continue_button: ButtonText
    save_button: ButtonText
    settings_button: ButtonText
    leave_button: ButtonText
    time_: float

    def __init__(self):
        """Constructor of the class 'EscMenu'."""
        super().__init__("Esc Menu")
        self.client = get_client()
        base_color = Colors.base_color
        hover_color = Colors.hover_color
        text_color = Colors.text_color
        self.time_ = time.time()
        space = 15
        width_base = 500
        self.continue_button = ButtonText("CENTER", get_client().get_screen().get_height() // 2 - 80 * 2 - 40 - space * 2,
                                          width_base, 80, "Continue", base_color, text_color)
        self.continue_button.click = lambda: get_game().reset_menu()
        self.continue_button.hover_color = hover_color

        self.save_button = ButtonText("CENTER", get_client().get_screen().get_height() // 2 - 80 - 40 - space,
                                      width_base, 80, "Save", base_color, text_color)
        self.save_button.click = lambda: save_game(self)
        self.save_button.hover_color = hover_color

        self.settings_button = ButtonText(get_client().get_screen().get_width() // 2 - width_base // 2, "CENTER",
                                          (width_base - space // 2) // 2, 80, "Settings", base_color, text_color)
        self.settings_button.click = lambda: get_game().set_menu(GeneralSettingsMenu(self))
        self.settings_button.hover_color = hover_color

        self.leave_button = ButtonText(get_client().get_screen().get_width() // 2 + space // 2, "CENTER",
                                       (width_base - space) // 2, 80, "Leave", base_color, text_color)

        self.leave_button.click = lambda: leave()
        self.leave_button.hover_color = hover_color

        self.elems = [self.continue_button, self.save_button, self.settings_button, self.leave_button]

    def activity(self) -> None:
        """The activity of the menu."""
        inputs = self.get_queue()
        if pygame.K_ESCAPE in inputs.get_codes() and has_elapsed(self.time_, 0.25):
            get_game().reset_menu()
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
