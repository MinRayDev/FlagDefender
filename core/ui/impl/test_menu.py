import pygame

from core.ui.element.impl.button import Button
from core.ui.element.impl.checkbox import Checkbox
from core.ui.element.impl.slider import Slider
from core.ui.element.impl.text import Text
from core.ui.element.impl.textentry import TextEntry
from core.ui.menu import Menu
from util.instance import get_game


class TestMenu(Menu):
    def __init__(self, prev):
        super().__init__("Main Menu", prev)
        self.on = False
        self.base_rect = pygame.Rect(15, 30, 500 - 30, 80)
        self.button = Button(15, 30, 500 - 30, 80, (44, 47, 51))
        self.button.click = lambda: get_game().reset_menu()
        self.buttons = [self.button]
        self.text = Text('Start', 0, 0, (153, 170, 181))
        self.text.rectangle.center = (500 // 2, 65)
        self.slider = Slider(10, 150, 100, 4, (255, 255, 255))
        self.slider_text = Text('0', 130, 135, (153, 170, 181))
        self.text_input = TextEntry('Test', 10, 175, 150, 50, (153, 170, 181))
        self.im = pygame.image.load(r".//resources/ingame-controller.svg")
        self.checkbox = Checkbox(20, 300, 100, 50, (0, 0, 0))
        self.elems = [self.text_input, self.slider, self.button, self.checkbox]

    def activity(self):
        inputs = self.get_queue()
        for button in self.buttons:
            button.activity(inputs)
            pass
        self.slider.activity(inputs)
        self.slider_text.change(str(self.slider.get()))
        self.text_input.activity(inputs)
        self.checkbox.activity(inputs)
        for elem in self.elems:
            if elem.hover() is not None and get_game().actual_menu is not None:
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
        self.checkbox.draw(surface)
        surface.blit(self.im, (50, 50))
