from __future__ import annotations

import pygame
from catppuccin import Flavour

from core.ui.element.impl.button_text import ButtonText
from core.ui.element.impl.slider import Slider
from core.ui.element.impl.text import Text
from core.ui.impl.settings.settings_base import SettingsBaseMenu
from core.ui.impl.world_menu import WorldMenu
from util.instance import get_game


class ControlSettingsMenu(SettingsBaseMenu):
    def __init__(self, parent):
        from util.instance import get_client
        super().__init__(parent)
        self.client = get_client()
        sw = self.client.get_screen().get_width()
        sh = self.client.get_screen().get_height()
        width = self.client.get_screen().get_width()//5
        height = self.client.get_screen().get_height()//130

    def activity(self):
        super().activity()

    def draw(self, surface):
        pygame.draw.rect(surface, Flavour.frappe().base.rgb, pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        super().draw(surface)
