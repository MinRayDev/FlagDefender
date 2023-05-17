from __future__ import annotations

import pygame
from pygame import Surface

from ui.element.impl.button_text import ButtonText
from ui.impl.rules_menu import RulesMenu
from ui.impl.score_menu import ScoreMenu
from ui.impl.settings.general_settings import GeneralSettingsMenu
from ui.impl.world_menu import WorldMenu
from ui.menu import Menu
from util.colors import Colors
from util.instance import get_game
from util.sprites import load


class MainMenu(Menu):
    def __init__(self):
        from util.instance import get_client
        super().__init__("Main Menu", None)
        self.client = get_client()
        base_color = Colors.base_color
        hover_color = Colors.hover_color
        text_color = Colors.text_color
        space = 15
        self.frame = 0
        self.sprite_index = 0
        self.sprites = load(r"./resources/menu")
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

    def activity(self):
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
        pygame.draw.rect(surface, Colors.base_color, pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        if self.frame >= self.client.clock.get_fps()/9:
            self.frame = 0
            self.sprite_index += 1
        if self.sprite_index >= len(self.sprites):
            self.sprite_index = 0
        surface.blit(pygame.transform.scale(list(self.sprites.values())[self.sprite_index], (self.client.get_screen().get_width(), self.client.get_screen().get_height())), (0, 0))
        super().draw(surface)
        self.frame += 1
