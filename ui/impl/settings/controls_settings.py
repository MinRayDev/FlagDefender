from __future__ import annotations

import pygame
from pygame import Surface

from ui.element.impl.key_input import KeyInput
from ui.element.impl.rectangle import Rectangle
from ui.element.impl.scrollpane import ScrollPane
from ui.element.impl.text import Text
from ui.impl.settings.settings_base import SettingsBaseMenu
from util.colors import Colors
from util.input.controls import Controls


class ControlSettingsMenu(SettingsBaseMenu):
    def __init__(self, parent):
        from util.instance import get_client
        super().__init__(parent)
        self.client = get_client()
        sw = self.client.get_screen().get_width()
        sh = self.client.get_screen().get_height()
        width = self.client.get_screen().get_width()//5
        height = self.client.get_screen().get_height()//13
        y = get_client().get_screen().get_height() // 75 + get_client().get_screen().get_height() // 17 + 7
        self.sp = ScrollPane(10, y, sw - 20, sh - y*2, Colors.base_color)
        for i, control in enumerate(Controls):
            if "register" in control.value and control.value["register"] is True:
                continue
            self.sp.elems.append(Text(str(control).split(".")[1], sw//2 - width*2, y + i * (height+7) + 15, Colors.text, height))
            self.sp.elems.append(KeyInput(pygame.key.name(control.value["keyboard"]["key"]), sw//2 - width//2, y + i * (height+7) + 15, width, height, Colors.text, control.value["keyboard"]["code"], Colors.surface1))
        self.elems.insert(0, self.sp)
        self.elems.insert(1, Rectangle(0, 0, get_client().get_screen().get_width(), self.rect_split.y, Colors.base_color))
        self.elems.insert(2, Rectangle(0, self.rect_split_2.y + self.rect_split_2.height, get_client().get_screen().get_width(), get_client().get_screen().get_height()-(self.rect_split_2.y + self.rect_split_2.height), Colors.base_color))

    def activity(self):
        super().activity()

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface, Colors.base_color, pygame.Rect(0, 0, surface.get_width(), surface.get_height()))

        for elem in self.elems:
            elem.draw(surface)
