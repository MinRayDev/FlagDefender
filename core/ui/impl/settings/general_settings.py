from __future__ import annotations

import pygame
from catppuccin import Flavour

from core.ui.element.impl.button_text import ButtonText
from core.ui.element.impl.slider import Slider
from core.ui.element.impl.text import Text
from core.ui.impl.settings.settings_base import SettingsBaseMenu
from core.ui.impl.world_menu import WorldMenu
from util.instance import get_game


class GeneralSettingsMenu(SettingsBaseMenu):
    def __init__(self, parent):
        from util.instance import get_client
        super().__init__(parent)
        self.client = get_client()
        sw = self.client.get_screen().get_width()
        sh = self.client.get_screen().get_height()
        width = self.client.get_screen().get_width()//5
        height = self.client.get_screen().get_height()//130
        self.slider_text = Text("0", sw//2 + width//2, 0, Flavour.frappe().text.rgb)
        self.slider_text.rectangle.x += self.slider_text.rectangle.width
        self.slider_text.rectangle.y = sh // 10 - self.slider_text.rectangle.height // 2 + self.slider_text.rectangle.height // 6
        self.master_volume_text = Text("Master volume", sw//2 - width//2, 0, Flavour.frappe().text.rgb)
        self.master_volume_text.rectangle.x -= self.master_volume_text.rectangle.width*1.2
        self.master_volume_text.rectangle.y = sh//10 - self.master_volume_text.rectangle.height//2 + self.master_volume_text.rectangle.height//6
        self.slider_volume = Slider(sw//2 - width//2, sh//10, width, height, Flavour.frappe().overlay0.rgb, Flavour.frappe().pink.rgb)
        self.elems += [self.slider_volume, self.slider_text, self.master_volume_text]

    def activity(self):
        super().activity()
        self.slider_text.change(str(int(self.slider_volume.get())))

    def draw(self, surface):
        pygame.draw.rect(surface, Flavour.frappe().base.rgb, pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        super().draw(surface)
