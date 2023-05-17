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
from util.instance import get_game
from util.time_util import has_elapsed


def save_game(menu):
    # loading screen
    game = get_game()  # TODO: loading bar
    game.current_level.save()
    # fin loading screen
    info(menu, "Game saved")


class EscMenu(GameMenu):
    def __init__(self):
        from util.instance import get_client
        super().__init__("Esc Menu")
        self.client = get_client()
        base_color = Colors.base_color
        hover_color = Colors.hover_color
        text_color = Colors.text_color
        self.time = time.time()
        space = 15
        width_base = 500
        self.solo_button = ButtonText("CENTER", get_client().get_screen().get_height() // 2 - 80 * 2 - 40 - space * 2,
                                      width_base, 80, "Continue", base_color, text_color)
        self.solo_button.click = lambda: get_game().reset_menu()
        self.solo_button.hover_color = hover_color

        self.coop_button = ButtonText("CENTER", get_client().get_screen().get_height() // 2 - 80 - 40 - space,
                                      width_base, 80, "Save", base_color, text_color)
        self.coop_button.click = lambda: save_game(self)
        self.coop_button.hover_color = hover_color

        self.settings_button = ButtonText(get_client().get_screen().get_width() // 2 - width_base // 2, "CENTER",
                                          (width_base - space // 2) // 2, 80, "Settings", base_color, text_color)
        self.settings_button.click = lambda: get_game().set_menu(GeneralSettingsMenu(self))
        self.settings_button.hover_color = hover_color

        self.leave_button = ButtonText(get_client().get_screen().get_width() // 2 + space // 2, "CENTER",
                                       (width_base - space) // 2, 80, "Leave", base_color, text_color)

        def leave():
            get_game().set_menu(MainMenu())
            time.sleep(0.02)
            get_game().reset_level()

        self.leave_button.click = lambda: leave()
        self.leave_button.hover_color = hover_color

        self.elems = [self.solo_button, self.coop_button, self.settings_button, self.leave_button]

    def activity(self):
        inputs = self.get_queue()
        if pygame.K_ESCAPE in inputs.get_codes() and has_elapsed(self.time, 0.25):
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

    def draw(self, surface: Surface) -> None:
        super().draw(surface)
