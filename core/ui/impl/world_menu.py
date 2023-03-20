from __future__ import annotations

import os
from typing import Optional
import pygame
from catppuccin import Flavour
import shutil
from core.client import Client
from core.ui.element.element import Element
from core.ui.element.impl.button_text import ButtonText
from core.ui.element.impl.notification import alert
from core.ui.element.impl.rectangle import Rectangle
from core.ui.element.impl.scrollpane import ScrollPane
from core.ui.element.impl.textentry import TextEntry
from core.ui.menu import Menu
from util import files
from util.input.controls import Inputs
from util.instance import get_game


class CreateNewWorld(Element):
    def __init__(self, parent: WorldMenu):
        self.parent = parent
        self.s_width, self.s_height = Client.instance.get_screen().get_width(), Client.instance.get_screen().get_height()
        super().__init__("CENTER", "CENTER", self.s_width // 3, self.s_height // 6)
        # self.rect_ = Rectangle("CENTER", "CENTER", self.s_width // 3, self.s_height // 6, Flavour.frappe().surface0.rgb, Flavour.frappe().surface1.rgb)
        self.rect = Rectangle("CENTER", "CENTER", self.s_width // 3, self.s_height // 6, Flavour.frappe().surface1.rgb, Flavour.frappe().surface1.rgb)
        self.text_entry = TextEntry("World Name", "CENTER", self.s_height//2 - (self.s_height // 16)//2 - 7, self.s_width // 4, self.s_height // 16, Flavour.frappe().text.rgb, Flavour.frappe().surface1.rgb)
        self.intern_elems: list[Element] = [self.rect, self.text_entry]

    def activity(self, inputs: Inputs) -> None:
        if pygame.K_ESCAPE in inputs.get_codes():
            if self in self.parent.elems:
                self.parent.new_creation = False
                del self.parent.elems[self.parent.elems.index(self)]
                return
        elif pygame.K_RETURN in inputs.get_codes():
            try:
                f = open(os.path.join(files.get_save_path(), self.text_entry.text + ".json"), "x")
                f.close()
                self.parent.new_creation = False
                del self.parent.elems[self.parent.elems.index(self)]
                self.parent.reload()
                return
            except:
                alert(self.parent, f"Error: {self.text_entry.text} is invalid")
                self.parent.new_creation = False
                del self.parent.elems[self.parent.elems.index(self)]
                self.parent.reload()
                return
        for elem in self.intern_elems:
            elem.activity(inputs)

    def draw(self, surface: pygame.Surface) -> None:
        for elem in self.intern_elems:
            elem.draw(surface)

    def hover(self) -> None:
        for elem in self.intern_elems:
            if elem.hover() is not None and get_game().actual_menu is not None and not isinstance(elem, Rectangle):
                if pygame.mouse.get_cursor() != elem.hover():
                    pygame.mouse.set_cursor(elem.hover())
                    break
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


class WorldMenu(Menu):
    def __init__(self, prev):
        super().__init__("World Menu", prev)
        self.base_color = Flavour.frappe().base.rgb
        self.button_base_color = Flavour.frappe().surface0.rgb
        self.button_hover_color = Flavour.frappe().overlay0.rgb
        self.text_color = Flavour.frappe().pink.rgb
        self.selected_button: Optional[ButtonText] = None
        self.sp = ScrollPane(10, 10, Client.get_screen().get_width() - 20, Client.get_screen().get_height() - 200,
                             self.base_color)
        for i, save in enumerate(files.get_saves()):
            if save.endswith(".json"):
                bt = ButtonText(Client.get_screen().get_width() // 7, 30 + (80 + 15) * i,
                                Client.get_screen().get_width() - (Client.get_screen().get_width() // 7) * 2, 80,
                                save.split("\\")[-1][:-5], self.button_base_color, self.text_color, self.button_hover_color)
                # bt.click = lambda: print(i)
                self.sp.elems.append(bt)
        elem0 = Rectangle(0, Client.get_screen().get_height() - 190, Client.get_screen().get_width(), 190,
                          Flavour.frappe().mantle.rgb)
        elem1 = Rectangle(0, 0, Client.get_screen().get_width(), 10, self.base_color)
        elem2 = Rectangle(0, 0, 10, self.sp.height + self.sp.y, self.base_color)
        elem3 = Rectangle(self.sp.width + self.sp.x, 0, 10, self.sp.height + self.sp.y,
                          self.base_color)  # TODO, double click pour load
        # self.load_button = ButtonText(Client.get_screen().get_width()/16, Client.get_screen().get_height() - 180, Client.get_screen().get_width()/4, 70, "Load", button_base_color, text_color, button_hover_color)
        base_x = Client.get_screen().get_width() // 7
        base_y = Client.get_screen().get_height() - Client.get_screen().get_height() // 6
        width = ((Client.get_screen().get_width() - (Client.get_screen().get_width() // 7) * 2) // 2) - 10
        height = Client.get_screen().get_height() // 15
        self.new_button = ButtonText(base_x, base_y, width, height, "New", self.button_base_color, self.text_color,
                                     self.button_hover_color)
        self.new_button.click = self.new
        self.dup_button = ButtonText(base_x, base_y + height + 20, width, height, "Duplicate", self.button_base_color,
                                     self.text_color, self.button_hover_color)
        self.dup_button.click = self.duplicate
        self.del_button = ButtonText(base_x + width + 20, base_y, width, height, "Delete", self.button_base_color,
                                     self.text_color, self.button_hover_color)
        self.del_button.click = self.delete
        self.back_button = ButtonText(base_x + width + 20, base_y + height + 20, width, height, "Back",
                                      self.button_base_color, self.text_color, self.button_hover_color)
        self.back_button.click = lambda: get_game().set_menu(prev)
        self.elems += [self.sp, elem0, elem1, elem2, elem3, self.del_button, self.dup_button, self.new_button, self.back_button]
        # self.sp.elems = [self.solo_button, self.coop_button, self.multi_button, self._button]
        self.new_creation: bool = False

    def activity(self):
        inputs = self.get_queue()
        if not self.new_creation:
            for elem in self.elems:
                elem.activity(inputs)
                pass

            for elem in self.elems:
                if elem.hover() is not None and get_game().actual_menu is not None:
                    if pygame.mouse.get_cursor() != elem.hover():
                        pygame.mouse.set_cursor(elem.hover())
                        break
            else:
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            for elem in self.sp.elems:
                if isinstance(elem, ButtonText):
                    if elem.has_been_clicked and self.selected_button != elem:
                        self.selected_button = elem
                        print(elem.text_content)
                    elif elem.has_been_clicked and self.selected_button == elem:
                        print("aaaa", elem.text_content)
        else:
            if pygame.mouse.get_cursor().data[0] != pygame.SYSTEM_CURSOR_ARROW and pygame.mouse.get_cursor().data[0] != pygame.SYSTEM_CURSOR_IBEAM:
                print("ooo")
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            for elem in self.elems:
                if isinstance(elem, CreateNewWorld):
                    elem.activity(inputs)
                    elem.hover()

    def draw(self, surface):
        for elem in self.elems:
            if self.new_creation:
                elem.is_hover = False
            elem.draw(surface)
            if isinstance(elem, ScrollPane):
                for child in elem.elems:
                    if self.new_creation:
                        child.is_hover = False
                    if self.selected_button == child and isinstance(child, ButtonText) and self.new_creation is False:
                        pygame.draw.rect(surface, Flavour.frappe().surface1.rgb,
                                         pygame.Rect(child.x - 4, child.y - 4, child.width + 8, child.height + 8))
                        child.draw(surface)

    def delete(self):
        if self.selected_button is not None:
            os.remove(os.path.join(files.get_save_path(), self.selected_button.text_content + ".json"))
        self.reload()

    def duplicate(self):
        if self.selected_button is not None:
            shutil.copyfile(os.path.join(files.get_save_path(), self.selected_button.text_content + ".json"), os.path.join(files.get_save_path(), self.selected_button.text_content + " - Copy.json"))
        self.reload()

    def reload(self):
        self.sp.elems.clear()
        for i, save in enumerate(files.get_saves()):
            if save.endswith(".json"):
                bt = ButtonText(Client.get_screen().get_width() // 7, 30 + (80 + 15) * i,
                                Client.get_screen().get_width() - (Client.get_screen().get_width() // 7) * 2, 80,
                                save.split("\\")[-1][:-5], self.button_base_color, self.text_color,
                                self.button_hover_color)
                self.sp.elems.append(bt)

    def new(self):
        self.new_creation = True
        self.elems.append(CreateNewWorld(self))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
