from __future__ import annotations

import pygame
from pygame import Surface

from util.instance import get_client
from ui.element.impl.slider import Slider
from ui.element.impl.text import Text
from ui.impl.settings.settings_base import SettingsBaseMenu
from util.colors import Colors
from util.files import write_datas, get_datas
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.client import Client




class GeneralSettingsMenu(SettingsBaseMenu):
    """Class 'GeneralSettingsMenu' is the general settings menu of the game.

        Extends the class 'SettingsBaseMenu'.
        :cvar game_credits: The credits of the game.
        :type game_credits: list[str].
        :ivar client: The client of the game.
        :type client: Client.
        :ivar slider_text: The text of the slider.
        :type slider_text: Text.
        :ivar master_volume_text: The text of the master volume.
        :type master_volume_text: Text.
        :ivar slider_volume: The slider of the volume.
        :type slider_volume: Slider.
        :ivar credit_text: The text of the credits.
        :type credit_text: Text.

    """
    game_credits: list[str] = [
        "Textures from Terraria",
        "Libraries: pygame",
        "Libraries: catppuccin",
        "Libraries: Pillow"
    ]
    client: 'Client'
    slider_text: Text
    master_volume_text: Text
    slider_volume: Slider
    credit_text: Text

    def __init__(self, parent):

        super().__init__(parent)
        self.client = get_client()
        sw: int = self.client.get_screen().get_width()
        sh: int = self.client.get_screen().get_height()
        width: int = self.client.get_screen().get_width()//5
        height: int = self.client.get_screen().get_height()//130
        self.slider_text = Text("0", sw//2 + width//2, 0, Colors.text)
        self.slider_text.rectangle.x += sw//150
        self.slider_text.rectangle.y = sh // 10 - self.slider_text.rectangle.height // 2 + self.slider_text.rectangle.height // 6
        self.master_volume_text = Text("Master volume", sw//2 - width//2, 0, Colors.text)
        self.master_volume_text.rectangle.x -= self.master_volume_text.rectangle.width*1.2
        self.master_volume_text.rectangle.y = sh//10 - self.master_volume_text.rectangle.height//2 + self.master_volume_text.rectangle.height//6
        self.slider_volume = Slider(sw//2 - width//2, sh//10, width, height, Colors.hover_color, selector_color=Colors.text_color)
        self.slider_volume.set_value(get_client().volume)
        self.credit_text = Text("Credits", sw//2 - width//2, sh//3, Colors.text)
        self.credit_text.rectangle.x -= self.master_volume_text.rectangle.width * 1.2
        y = self.credit_text.rectangle.y + self.credit_text.height + 10
        self.elems += [self.slider_volume, self.slider_text, self.master_volume_text, self.credit_text]
        for credit in GeneralSettingsMenu.game_credits:
            self.elems.append(Text(credit, self.credit_text.rectangle.x, y, Colors.text_color))
            y += 40

    def activity(self) -> None:
        """Method 'activity' updates the volume of the game."""
        super().activity()
        self.slider_text.change(str(int(self.slider_volume.get())))
        if self.client.volume != int(self.slider_volume.get()):
            self.client.volume = self.slider_volume.get()
            datas = get_datas()
            datas["volume"] = self.slider_volume.get()
            write_datas(datas)

    def draw(self, surface: Surface) -> None:
        """Method 'draw' draws the general settings menu.

            :param surface: The surface of the game.
            :type surface: Surface.

        """
        pygame.draw.rect(surface, Colors.base_color, pygame.Rect(0, 0, surface.get_width(), self.client.get_screen().get_height()))
        super().draw(surface)
