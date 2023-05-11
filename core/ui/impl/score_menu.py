from datetime import datetime

import pygame
from pygame import Surface

from core.ui.element.impl.button_text import ButtonText
from core.ui.element.impl.scrollpane import ScrollPane
from core.ui.element.impl.text import Text
from core.ui.menu import Menu
from util.colors import Colors
from util.files import get_datas
from util.instance import get_client
from util.instance import get_game


class ScoreMenu(Menu):
    def __init__(self, prev):
        super().__init__("Score Menu", prev)
        self.base_color = Colors.base_color
        self.button_base_color = Colors.button_base_color
        self.button_hover_color = Colors.hover_color
        self.text_color = Colors.text_color
        self.sp = ScrollPane(10, 10, get_client().get_screen().get_width() - 20, get_client().get_screen().get_height() - 200,
                             self.base_color)
        x = get_client().get_screen().get_width() // 25
        y = get_client().get_screen().get_height() // 75 + get_client().get_screen().get_height() // 17 + 50
        scores = sorted(get_datas()["scores"], key=lambda score_: score_["score"])
        for score in scores:
            text: Text = Text("1. " + str(score["score"]) + " (" + datetime.fromtimestamp(score["time"]).strftime("%m/%d/%Y, %Hh %Mmin %Ss") + ")", x, y, self.text_color)
            text.rectangle.x = get_client().get_screen().get_width()//2 - text.rectangle.width//2
            self.sp.elems.append(text)
            y += 40
        self.back_button = ButtonText(get_client().get_screen().get_width() // 30,
                                      get_client().get_screen().get_height() // 75,
                                      get_client().get_screen().get_width() // 10,
                                      get_client().get_screen().get_height() // 17,
                                      "Back", self.base_color, self.text_color,
                                      hover_color=Colors.hover_color)
        self.back_button.click = lambda: get_game().set_menu(prev)
        self.elems += [self.sp, self.back_button]
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def activity(self):
        super().activity()
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
        pygame.draw.rect(surface, Colors.base_color, pygame.Rect(0, 0, get_client().get_screen().get_width(), get_client().get_screen().get_height()))
        for elem in self.elems:
            elem.draw(surface)
