import pygame

from core.game import Game
from core.menus.elements.impl.button import Button
from core.menus.elements.impl.button_text import ButtonText
from core.menus.elements.impl.checkbox import Checkbox
from core.menus.elements.impl.slider import Slider
from core.menus.elements.impl.text import Text
from core.menus.elements.impl.textentry import TextEntry
from core.menus.menu import Menu


class MPJoinMenu(Menu):
    def __init__(self):
        super().__init__("Multiplayer Menu")
        self.on = False
        self.base_rect = pygame.Rect(15, 30, 500 - 30, 80)
        self.button = ButtonText(15, 30, 500 - 30, 80, "Send", (44, 47, 51))
        self.button.click = lambda: Game.instance.reset_menu()
        self.text_input = TextEntry('Test', 10, 175, 150, 50, (153, 170, 181))
        self.elems = [self.text_input, self.button]

    def activity(self):
        inputs = self.get_queue()
        for elem in self.elems:
            elem.activity(inputs)
            if elem.hover() is not None and Game.instance.actual_menu is not None:
                if pygame.mouse.get_cursor() != elem.hover():
                    pygame.mouse.set_cursor(elem.hover())
                    break
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, surface):
        for elem in self.elems:
            elem.draw(surface)