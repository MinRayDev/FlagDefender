from __future__ import annotations

import pygame
from pygame import Surface


from ui.element.impl.key_input import KeyInput
from ui.element.impl.rectangle import Rectangle
from ui.element.impl.scrollpane import ScrollPane
from ui.element.impl.text import Text
from ui.impl.settings.settings_base import SettingsBaseMenu
from ui.menu import Menu
from util.colors import Colors
from util.input.controls import Controls
from util.instance import get_client
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.client import Client


class ControlSettingsMenu(SettingsBaseMenu):
    """Class 'ControlSettingsMenu' is the control settings menu of the game.

        Extends the class 'SettingsBaseMenu'.
        :ivar client: The client of the game.
        :type client: Client.
        :ivar sp: The scrollpane of the menu.
        :type sp: ScrollPane.

    """
    client: 'Client'
    sp: ScrollPane

    def __init__(self, parent: Menu):
        """Constructor of the class 'ControlSettingsMenu'.

            :param parent: The parent of the menu.
            :type parent: Menu.

        """
        super().__init__(parent)
        self.client = get_client()
        sw: int = self.client.get_screen().get_width()
        sh: int = self.client.get_screen().get_height()
        width: int = self.client.get_screen().get_width()//5
        height: int= self.client.get_screen().get_height()//13
        y: int = get_client().get_screen().get_height() // 75 + get_client().get_screen().get_height() // 17 + 7
        self.sp = ScrollPane(10, y, sw - 20, sh - y*2, Colors.base_color)
        for i, control in enumerate(Controls):
            if "register" in control.value and control.value["register"] is True:
                continue
            self.sp.elems.append(Text(str(control).split(".")[1], sw//2 - width*2, y + i * (height+7) + 15, Colors.text, height))
            self.sp.elems.append(KeyInput(pygame.key.name(control.value["keyboard"]["key"]), sw//2 - width//2, y + i * (height+7) + 15, width, height, Colors.text, control.value["keyboard"]["code"], Colors.surface1))
        self.elems.insert(0, self.sp)
        self.elems.insert(1, Rectangle(0, 0, get_client().get_screen().get_width(), self.rect_split.y, Colors.base_color))
        self.elems.insert(2, Rectangle(0, self.rect_split_2.y + self.rect_split_2.height, get_client().get_screen().get_width(), get_client().get_screen().get_height()-(self.rect_split_2.y + self.rect_split_2.height), Colors.base_color))

    def activity(self) -> None:
        """Activity of the menu."""
        super().activity()

    def draw(self, surface: Surface) -> None:
        """Draws the menu."""
        pygame.draw.rect(surface, Colors.base_color, pygame.Rect(0, 0, surface.get_width(), surface.get_height()))

        for elem in self.elems:
            elem.draw(surface)
