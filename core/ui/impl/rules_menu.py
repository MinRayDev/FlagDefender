import pygame
from pygame import Surface

from core.ui.element.impl.button_text import ButtonText
from core.ui.element.impl.scrollpane import ScrollPane
from core.ui.element.impl.text import Text
from core.ui.menu import Menu
from util.colors import Colors
from util.instance import get_client
from util.instance import get_game

rules: list[str] = [
    "The goal is to survive as many waves as possible by protecting the flag from the monsters.",
    "b"

]


class RulesMenu(Menu):
    def __init__(self, prev):
        super().__init__("World Menu", prev)
        self.base_color = Colors.base_color
        self.button_base_color = Colors.button_base_color
        self.button_hover_color = Colors.hover_color
        self.text_color = Colors.text_color
        self.sp = ScrollPane(10, 10, get_client().get_screen().get_width() - 20, get_client().get_screen().get_height() - 200,
                             self.base_color)
        x = get_client().get_screen().get_width() // 25
        y = get_client().get_screen().get_height() // 75 + get_client().get_screen().get_height() // 17 + 50
        for rule in rules:
            self.sp.elems.append(Text(rule, x, y, self.text_color))
            y += 40
        self.back_button = ButtonText(get_client().get_screen().get_width() // 30,
                                      get_client().get_screen().get_height() // 75,
                                      get_client().get_screen().get_width() // 10,
                                      get_client().get_screen().get_height() // 17,
                                      "Back", self.base_color, self.text_color,
                                      hover_color=Colors.hover_color)
        self.back_button.click = lambda: get_game().set_menu(prev)
        self.elems += [self.sp, self.back_button]

    def activity(self):
        inputs = self.get_queue()
        for elem in self.elems:
            elem.activity(inputs)

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface, Colors.base_color, pygame.Rect(0, 0, get_client().get_screen().get_width(), get_client().get_screen().get_height()))
        for elem in self.elems:
            elem.draw(surface)
