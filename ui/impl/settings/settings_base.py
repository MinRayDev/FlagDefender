from __future__ import annotations

import pygame
from catppuccin import Flavour
from pygame import Surface

from ui.element.impl.button_text import ButtonText
from ui.element.impl.rectangle import Rectangle
from ui.element.impl.text import Text

from ui.menu import Menu
from util.colors import Colors
from util.instance import get_game


class SettingsBaseMenu(Menu):
    def __init__(self, parent):
        from ui.impl.settings.controls_settings import ControlSettingsMenu
        from ui.impl.settings.general_settings import GeneralSettingsMenu
        from util.instance import get_client
        super().__init__("Main Menu", parent)
        self.client = get_client()

        width_base = get_client().get_screen().get_width() // 10
        height_base = get_client().get_screen().get_height() // 17
        self.rect_split = Rectangle(get_client().get_screen().get_width() // 40,
                                    get_client().get_screen().get_height() // 75 + height_base,
                                    get_client().get_screen().get_width() - 2 * (
                                            get_client().get_screen().get_width() // 40),
                                    3,
                                    Colors.crust)
        self.general_button = ButtonText(get_client().get_screen().get_width() // 2 - width_base - 10,
                                         get_client().get_screen().get_height() // 75,
                                         width_base,
                                         height_base,
                                         "General", Colors.base_color, Colors.text)
        self.general_button.hover_text_color = Colors.subtext0
        self.general_button.click = lambda: get_game().set_menu(GeneralSettingsMenu(parent))
        self.control_button = ButtonText(get_client().get_screen().get_width() // 2 + 10,
                                         get_client().get_screen().get_height() // 75,
                                         width_base,
                                         height_base,
                                         "Controls", Colors.base_color, Colors.text)
        self.control_button.hover_text_color = Colors.subtext0
        self.control_button.click = lambda: get_game().set_menu(ControlSettingsMenu(parent))
        self.back_button = ButtonText(get_client().get_screen().get_width() // 30,
                                      get_client().get_screen().get_height() // 75,
                                      width_base,
                                      height_base,
                                      "Back", Colors.base_color, Colors.text_color, hover_color=Colors.hover_color)
        self.back_button.click = lambda: get_game().set_menu(parent)
        if isinstance(self, GeneralSettingsMenu):
            self.selected = self.general_button
        else:
            self.selected = self.control_button

        self.rect_split_2 = Rectangle(get_client().get_screen().get_width() // 40,
                                      get_client().get_screen().get_height() - (get_client().get_screen().get_height() // 75 + height_base),
                                      get_client().get_screen().get_width() - 2 * (
                                              get_client().get_screen().get_width() // 40),
                                      3,
                                      Colors.subtext0)
        self.client_id_text = Text("Client id: " + str(get_client().id), get_client().get_screen().get_width() // 30, get_client().get_screen().get_height() - height_base + get_client().get_screen().get_height()//80, Colors.text, 20)
        self.game_version_text = Text("Game version: " + str(get_game().version), 0, get_client().get_screen().get_height() - height_base + get_client().get_screen().get_height()//80, Colors.text, 20)
        self.game_version_text.rectangle.x = get_client().get_screen().get_width() - get_client().get_screen().get_width() // 30 - self.game_version_text.rectangle.width
        self.elems = [self.general_button, self.control_button, self.back_button, self.rect_split, self.rect_split_2, self.client_id_text, self.game_version_text]

    def activity(self):
        super().activity()
        inputs = self.get_queue()
        for elem in self.elems:
            elem.activity(inputs)
            if ((isinstance(elem, ButtonText) and elem.has_been_clicked) or self.selected == elem) and elem.text_content in ["General", "Controls"]:
                self.selected = elem
                elem.text_color = Flavour.frappe().green.rgb
                elem.hover_text_color = Flavour.frappe().green.rgb
            elif isinstance(elem, ButtonText):
                elem.text_color = Colors.text
                elem.hover_text_color = Colors.subtext0
        for elem in self.elems:
            if elem.hover() is not None and get_game().current_menu is not None:
                if pygame.mouse.get_cursor() != elem.hover():
                    pygame.mouse.set_cursor(elem.hover())
                    break
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface, Colors.base_color,
                         pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        super().draw(surface)
