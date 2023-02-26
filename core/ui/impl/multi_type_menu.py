import pygame
from catppuccin import Flavour

from core.client import Client
from core.ui.element.impl.button_text import ButtonText
from core.ui.impl.multi_world_menu import MPWorldMenu
from core.ui.impl.multiplayer_join_menu import MPJoinMenu
from core.ui.menu import Menu
from util.instance import get_game, get_client


class MultiType(Menu):
    def __init__(self, prev):
        self.client = get_client()
        super().__init__("Multi Menu", prev)
        self.solo_button = ButtonText(15, 30, 500 - 30, 80, "Host", (44, 47, 51))
        self.solo_button.click = lambda: get_game().set_menu(MPWorldMenu(self))
        self.coop_button = ButtonText(15, 120, 500 - 30, 80, "Join", (44, 47, 51))
        self.coop_button.click = lambda: get_game().set_menu(MPJoinMenu(self))
        self.back_button = ButtonText(Client.get_screen().get_width() / 9 * 2 + Client.get_screen().get_width() / 3, Client.get_screen().get_height() - 100, Client.get_screen().get_width() / 3, 70, "Back", (44, 47, 51))
        self.back_button.click = lambda: get_game().set_menu(prev)
        self.elems = [self.solo_button, self.coop_button, self.back_button]

    def activity(self):
        inputs = self.get_queue()
        for elem in self.elems:
            elem.activity(inputs)
            pass

        for elem in self.elems:
            if elem.hover() is not None and get_game().actual_menu is not None:
                if pygame.mouse.get_cursor() != elem.hover():
                    pygame.mouse.set_cursor(elem.hover())
                    break
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, surface):
        pygame.draw.rect(surface, Flavour.frappe().base.rgb, pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        for elem in self.elems:
            elem.draw(surface)
