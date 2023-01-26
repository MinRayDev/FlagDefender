import pygame

from core.game import Game
from core.menus.elements.button import Button
from core.menus.elements.slider import Slider
from core.menus.elements.text import Text
from core.menus.elements.textentry import TextEntry
from core.menus.menu import Menu


class MainMenu(Menu):
    def __init__(self):
        super().__init__("Main Menu")
        self.on = False
        self.base_rect = pygame.Rect(15, 30, 500 - 30, 80)
        self.button = Button(15, 30, 500 - 30, 80, (44, 47, 51))
        self.button.click = lambda: Game.instance.reset_menu()
        self.buttons = [self.button]
        self.text = Text('Start', 0, 0, (153, 170, 181))
        self.text.rectangle.center = (500 // 2, 65)
        self.slider = Slider(10, 150, 100, 4, (255, 255, 255))
        self.slider_text = Text('0', 130, 135, (153, 170, 181))
        self.text_input = TextEntry('Test', 10, 175, (153, 170, 181))
        self.elems = [self.text_input, self.slider, self.button]

    def activity(self, **kwargs):
        for button in self.buttons:
            button.activity(kwargs)
        self.slider.activity(kwargs)
        self.slider_text.change(str(self.slider.get()))
        self.text_input.activity(kwargs)
        for elem in self.elems:
            if elem.hover() is not None:
                if pygame.mouse.get_cursor() != elem.hover():
                    pygame.mouse.set_cursor(elem.hover())
                    break
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, surface):
        for button in self.buttons:
            button.draw(surface)
        self.text.draw(surface)
        self.slider_text.draw(surface)
        self.slider.draw(surface)
        self.text_input.draw(surface)
