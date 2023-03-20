from __future__ import annotations

import pygame
from catppuccin import Flavour

from core.client import Client
from core.ui.element.impl.button_text import ButtonText
from core.ui.element.impl.key_input import KeyInput
from core.ui.element.impl.rectangle import Rectangle
from core.ui.element.impl.scrollpane import ScrollPane
from core.ui.element.impl.slider import Slider
from core.ui.element.impl.text import Text
from core.ui.impl.settings.settings_base import SettingsBaseMenu
from core.ui.impl.world_menu import WorldMenu
from util.colors import Colors
from util.input.controls import Controls
from util.instance import get_game


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
        self.sp = ScrollPane(10, y, sw - 20, sh - y*2, Flavour.frappe().base.rgb)
        for i, control in enumerate(Controls):
            self.sp.elems.append(KeyInput(pygame.key.name(control.value["keyboard"]["key"]), sw//2 - width//2, y + i * (height+7) + 15, width, height, Flavour.frappe().text.rgb, control.value["keyboard"]["code"], Flavour.frappe().surface1.rgb))
        # t = KeyInput("a", sw//2, sh//2, width, height, Flavour.frappe().text.rgb)
        self.elems.insert(0, self.sp)
        # self.elems.append(Rectangle(0, 0, sw, y, Flavour.frappe().pink.rgb))

    def activity(self):
        super().activity()

    def draw(self, surface):
        pygame.draw.rect(surface, Flavour.frappe().base.rgb, pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        for elem in self.elems:
            elem.draw(surface)
