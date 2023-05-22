from datetime import datetime

import pygame
from pygame import Surface

from ui.element.impl.button_text import ButtonText
from ui.element.impl.scrollpane import ScrollPane
from ui.element.impl.text import Text
from ui.menu import Menu
from util.colors import Colors
from util.files import get_datas
from util.instance import get_client
from util.instance import get_game


class ScoreMenu(Menu):
    """Class 'ScoreMenu' is the score menu of the game.

        Extends the class 'Menu'.
        :ivar base_color: The base color of the menu.
        :type base_color: tuple[int, int, int].
        :ivar button_base_color: The base color of the buttons.
        :type button_base_color: tuple[int, int, int].
        :ivar button_hover_color: The hover color of the buttons.
        :type button_hover_color: tuple[int, int, int].
        :ivar text_color: The text color of the menu.
        :type text_color: tuple[int, int, int].
        :ivar back_button: The button to go back to the previous menu.
        :type back_button: ButtonText.
        :ivar sp: The scrollpane of the menu.
        :type sp: ScrollPane.

    """
    base_color: tuple[int, int, int]
    button_base_color: tuple[int, int, int]
    button_hover_color: tuple[int, int, int]
    text_color: tuple[int, int, int]
    back_button: ButtonText
    sp: ScrollPane

    def __init__(self, prev: Menu):
        """Constructor of the class 'ScoreMenu'.

            :param prev: The previous menu.
            :type prev: Menu.

        """
        super().__init__("Score Menu", prev)
        self.base_color = Colors.base_color
        self.button_base_color = Colors.button_base_color
        self.button_hover_color = Colors.hover_color
        self.text_color = Colors.text_color
        self.back_button = ButtonText(get_client().get_screen().get_width() // 30,
                                      get_client().get_screen().get_height() // 75,
                                      get_client().get_screen().get_width() // 10,
                                      get_client().get_screen().get_height() // 17,
                                      "Back", self.base_color, self.text_color,
                                      hover_color=Colors.hover_color)
        self.back_button.click = lambda: get_game().set_menu(prev)
        self.sp = ScrollPane(10, self.back_button.y + self.back_button.height + 5, get_client().get_screen().get_width() - 20, get_client().get_screen().get_height() - 200,
                             self.base_color)

        y: int = int(get_client().get_screen().get_height() // 75 + get_client().get_screen().get_height() // 17 + 50)
        scores = sorted(get_datas()["scores"], key=lambda score_: -score_["score"])
        for i, score in enumerate(scores):
            text: Text = Text(str(i+1) + ". " + str(score["score"]) + " points   (" + datetime.fromtimestamp(score["time"]).strftime("%m/%d/%Y, %Hh %Mmin %Ss") + ")", 0, y, self.text_color)
            text.x = get_client().get_screen().get_width()//2 - text.rectangle.width//2
            self.sp.elems.append(text)
            y += 40
        self.elems += [self.sp, self.back_button]
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def activity(self) -> None:
        """Method 'activity' updates the menu."""
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
        """Method 'draw' draws the menu.

            :param surface: The surface to draw on.
            :type surface: Surface.

        """
        pygame.draw.rect(surface, Colors.base_color, pygame.Rect(0, 0, get_client().get_screen().get_width(), get_client().get_screen().get_height()))
        for elem in self.elems:
            elem.draw(surface)
