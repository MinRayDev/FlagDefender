
import pygame
from catppuccin import Flavour

from core.client import Client
from core.ui.element.element import Element
from core.ui.element.impl.button_text import ButtonText
from core.ui.element.impl.scrollpane import ScrollPane
from core.ui.impl.multiplayer_host_menu import MPHostMenu
from core.ui.menu import Menu
from util import files
from util.instance import get_game, get_client


class MPWorldMenu(Menu):
    def __init__(self, prev):
        super().__init__("World Menu", prev)
        self.client = get_client()
        self.sp = ScrollPane(10, 10, Client.get_screen().get_width()-20, Client.get_screen().get_height()-200, (43, 45, 49))
        for i, save in enumerate(files.get_saves()):
            bt = ButtonText(200, 30+(80+10)*i, Client.get_screen().get_width()-400, 80, save.split("\\")[-1][:-5], (44, 47, 51))
            bt.click = lambda: print(i)
            self.sp.elems.append(bt)
        # 43, 45, 49

        # 35, 39, 42
        self.elems = [self.sp]
        elem0 = Element(0, Client.get_screen().get_height()-190, Client.get_screen().get_width(), 190, pygame.Rect(0, Client.get_screen().get_height()-190, Client.get_screen().get_width(), 190))
        elem0.draw = lambda surface: pygame.draw.rect(surface, (35, 39, 42), pygame.Rect(elem0.x, elem0.y, elem0.width, elem0.height))
        elem1 = Element(0, 0, Client.get_screen().get_width(), 10, pygame.Rect(0, Client.get_screen().get_height()-190, Client.get_screen().get_width(), 190))
        elem1.draw = lambda surface: pygame.draw.rect(surface, (35, 39, 42), pygame.Rect(elem1.x, elem1.y, elem1.width, elem1.height))
        elem2 = Element(0, 0, 10, self.sp.height+self.sp.y, pygame.Rect(0, Client.get_screen().get_height()-190, Client.get_screen().get_width(), 190))
        elem2.draw = lambda surface: pygame.draw.rect(surface, (35, 39, 42), pygame.Rect(elem2.x, elem2.y, elem2.width, elem2.height))
        elem3 = Element(self.sp.width+self.sp.x, 0, 10, self.sp.height+self.sp.y, pygame.Rect(0, Client.get_screen().get_height()-190, Client.get_screen().get_width(), 190))
        elem3.draw = lambda surface: pygame.draw.rect(surface, (35, 39, 42), pygame.Rect(elem3.x, elem3.y, elem3.width, elem3.height))
        self.t_elems = [elem0, elem1, elem2, elem3]
        for elem_ in self.t_elems:
            self.elems.append(elem_)
        self.load_button = ButtonText(Client.get_screen().get_width()/16, Client.get_screen().get_height() - 180, Client.get_screen().get_width()/4, 70, "Load", (44, 47, 51))
        self.dup_button = ButtonText(Client.get_screen().get_width()/16 * 2 + Client.get_screen().get_width()/4, Client.get_screen().get_height() - 180, Client.get_screen().get_width()/4, 70, "Duplicate", (44, 47, 51))
        self.del_button = ButtonText(Client.get_screen().get_width()/16 * 3 + Client.get_screen().get_width()/4 * 2, Client.get_screen().get_height() - 180, Client.get_screen().get_width()/4, 70, "Delete", (44, 47, 51))
        self.new_button = ButtonText(Client.get_screen().get_width()/9, Client.get_screen().get_height() - 100, Client.get_screen().get_width()/3, 70, "New", (44, 47, 51))
        self.new_button.click = lambda: get_game().set_menu(MPHostMenu(self))
        self.back_button = ButtonText(Client.get_screen().get_width()/9 * 2 + Client.get_screen().get_width()/3, Client.get_screen().get_height() - 100, Client.get_screen().get_width()/3, 70, "Back", (44, 47, 51))
        self.back_button.click = lambda: get_game().set_menu(prev)
        self.elems += [self.load_button, self.del_button, self.dup_button, self.new_button, self.back_button]
        # self.sp.elems = [self.solo_button, self.coop_button, self.multi_button, self._button]

    def activity(self):
        inputs = self.get_queue()

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

    def draw(self, surface):
        pygame.draw.rect(surface, Flavour.frappe().base.rgb, pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        for elem in self.elems:
            elem.draw(surface)
