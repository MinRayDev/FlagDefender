from __future__ import annotations

import pygame
from catppuccin import Flavour

from core.ui.element.impl.button_text import ButtonText
from core.ui.element.impl.rectangle import Rectangle
from core.ui.element.impl.text import Text

from core.ui.menu import Menu
from util.instance import get_game


class SettingsBaseMenu(Menu):
    def __init__(self, parent):
        from core.ui.impl.settings.controls_settings import ControlSettingsMenu
        from core.ui.impl.settings.general_settings import GeneralSettingsMenu
        from util.instance import get_client
        super().__init__("Main Menu", parent)
        self.client = get_client()
        base_color = Flavour.frappe().base.rgb
        hover_color = Flavour.frappe().overlay0.rgb
        text_color = Flavour.frappe().pink.rgb

        width_base = get_client().get_screen().get_width() // 10
        height_base = get_client().get_screen().get_height() // 17
        self.rect_split = Rectangle(get_client().get_screen().get_width() // 40,
                                    get_client().get_screen().get_height() // 75 + height_base,
                                    get_client().get_screen().get_width() - 2 * (
                                            get_client().get_screen().get_width() // 40),
                                    3,
                                    Flavour.frappe().crust.rgb)
        self.general_button = ButtonText(get_client().get_screen().get_width() // 2 - width_base - 10,
                                         get_client().get_screen().get_height() // 75,
                                         width_base,
                                         height_base,
                                         "General", base_color, Flavour.frappe().text.rgb)
        self.general_button.hover_text_color = Flavour.frappe().subtext0.rgb
        self.general_button.click = lambda: get_game().set_menu(GeneralSettingsMenu(parent))
        self.control_button = ButtonText(get_client().get_screen().get_width() // 2 + 10,
                                         get_client().get_screen().get_height() // 75,
                                         width_base,
                                         height_base,
                                         "Controls", base_color, Flavour.frappe().text.rgb)
        self.control_button.hover_text_color = Flavour.frappe().subtext0.rgb
        self.control_button.click = lambda: get_game().set_menu(ControlSettingsMenu(parent))
        self.back_button = ButtonText(get_client().get_screen().get_width() // 30,
                                      get_client().get_screen().get_height() // 75,
                                      width_base,
                                      height_base,
                                      "Back", base_color, text_color, hover_color=hover_color)
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
                                      Flavour.frappe().crust.rgb)
        self.client_id_text = Text("Client id: " + str(get_client().id), get_client().get_screen().get_width() // 30, get_client().get_screen().get_height() - height_base + get_client().get_screen().get_height()//80, Flavour.frappe().text.rgb, 20)
        self.game_version_text = Text("Game version: " + str(get_game().version), 0, get_client().get_screen().get_height() - height_base + get_client().get_screen().get_height()//80, Flavour.frappe().text.rgb, 20)
        self.game_version_text.rectangle.x = get_client().get_screen().get_width() - get_client().get_screen().get_width() // 30 - self.game_version_text.rectangle.width
        self.elems = [self.general_button, self.control_button, self.back_button, self.rect_split, self.rect_split_2, self.client_id_text, self.game_version_text]

    def activity(self):
        inputs = self.get_queue()
        for elem in self.elems:
            elem.activity(inputs)
            if ((isinstance(elem, ButtonText) and elem.has_been_clicked) or self.selected == elem) and elem.text_content in ["General", "Controls"]:
                self.selected = elem
                elem.text_color = Flavour.frappe().green.rgb
                elem.hover_text_color = Flavour.frappe().green.rgb
            elif isinstance(elem, ButtonText):
                elem.text_color = Flavour.frappe().text.rgb
                elem.hover_text_color = Flavour.frappe().subtext0.rgb
        for elem in self.elems:
            if elem.hover() is not None and get_game().actual_menu is not None:
                if pygame.mouse.get_cursor() != elem.hover():
                    pygame.mouse.set_cursor(elem.hover())
                    break
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, surface):
        pygame.draw.rect(surface, Flavour.frappe().base.rgb,
                         pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        super().draw(surface)
