from __future__ import annotations

import random
import time

import pygame
from catppuccin import Flavour

from core.client import Client
from core.ingame.item.item_type import ItemType
from core.ui.element.element import Element
from core.ui.element.impl.key_input import KeyInput
from core.ui.element.impl.rectangle import Rectangle
from core.ui.game_menu import GameMenu
from core.world import Facing
from entities.Item import ItemEntity
from util.fonts import Fonts
from util.input.controls import Controls, Inputs, test
from util.instance import get_game
from core.ingame.spell.impl.wall import Wall
from core.ingame.spell.impl.turret import Turret


def entry(self, inputs: Inputs) -> None:
    t = False
    for elem_ in inputs.raw_inputs:
        if elem_.type == pygame.KEYDOWN:
            print(elem_)
            self.value = pygame.key.name(elem_.key)
            print(self.code)
            if Controls.code_exists(self.code) and elem_.key != Controls.from_code(self.code).get_key():
                print('aaa')
                test[self.code] = self.item
                self.parent.new_creation = False
                del self.parent.elems[self.parent.elems.index(self)]
                t = True
    if t:
        self.selected = False


class Bind(Element):
    def __init__(self, parent: InventoryMenu, item: ItemType):
        self.parent = parent
        self.s_width, self.s_height = Client.instance.get_screen().get_width(), Client.instance.get_screen().get_height()
        super().__init__("CENTER", "CENTER", self.s_width // 3, self.s_height // 6)
        # self.rect_ = Rectangle("CENTER", "CENTER", self.s_width // 3, self.s_height // 6, Flavour.frappe().surface0.rgb, Flavour.frappe().surface1.rgb)
        self.rect = Rectangle("CENTER", "CENTER", self.s_width // 3, self.s_height // 6, Flavour.frappe().surface1.rgb, Flavour.frappe().surface1.rgb)
        self.text_entry = KeyInput("Input", "CENTER", self.s_height//2 - (self.s_height // 16)//2 - 7, self.s_width // 4, self.s_height // 16, Flavour.frappe().text.rgb, random.randint(500, 1500), Flavour.frappe().surface1.rgb)
        self.text_entry.entry = entry.__get__(self.text_entry, KeyInput)
        self.text_entry.item = item
        self.intern_elems: list[Element] = [self.rect, self.text_entry]

    def activity(self, inputs: Inputs) -> None:
        if pygame.K_ESCAPE in inputs.get_codes():
            if self in self.parent.elems:
                self.parent.new_creation = False
                del self.parent.elems[self.parent.elems.index(self)]
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


class InventoryMenu(GameMenu):
    def __init__(self):
        super().__init__("Inventory Menu")
        screen_width = Client.get_screen().get_width()
        screen_height = Client.get_screen().get_height()
        self.x: int = screen_width//20
        self.y: int = screen_width//15
        self.width: int = screen_width - self.x*2
        self.height: int = screen_height - self.y*2
        self.init_time: float = time.time()
        self.rectangle: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rectangles: list[pygame.Rect] = []
        self.elems: list[Element] = []
        line_max: int = 4
        column_max: int = 9
        x_base: int = self.x + screen_width//75
        y_base: int = self.y + screen_width//75
        base: int = ((self.width - screen_width*2//75)//column_max) - screen_width//150
        self.selected: int = 18
        for i in range(column_max):
            for j in range(line_max):
                self.rectangles.append(pygame.Rect(x_base + i * (base + screen_width//150), y_base + j * (base + screen_height//100), base, base))

    def activity(self):
        inputs = self.get_queue()
        if pygame.K_ESCAPE in inputs.get_codes():
            get_game().reset_menu()
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

        if pygame.K_LEFT in inputs.get_codes() and self.selected - 4 > 0:
            self.selected -= 4
        if pygame.K_RIGHT in inputs.get_codes() and self.selected + 4 <= 36:
            self.selected += 4
        if pygame.K_DOWN in inputs.get_codes() and self.selected + 1 <= 36:
            self.selected += 1
        if pygame.K_UP in inputs.get_codes() and self.selected - 1 > 0:
            self.selected -= 1
        if pygame.K_w in inputs.get_codes():
            if len(get_game().main_player.get_inventory()) > self.selected-1:
                item = get_game().main_player.get_inventory().get_index(self.selected-1)
                p_entity = get_game().main_player.entity
                get_game().main_player.get_inventory().remove_item(item, 1)
                match p_entity.facing:
                    case Facing.EAST:
                        ItemEntity(p_entity.x + p_entity.width + 10, item.get_sprite_path(), p_entity.world, item)
                    case Facing.WEST:
                        ItemEntity(p_entity.x - 48 - 10, item.get_sprite_path(), p_entity.world, item)
        if Controls.a.get_code() in inputs.get_codes():
            print('a1')
            if len(get_game().main_player.get_inventory()) > self.selected - 1:
                print('2')
                item = get_game().main_player.get_inventory().get_index(self.selected - 1)
                print("a", item)
                if item.has_usage():
                    print('3')
                    exec(item.get_usage() + "(get_game().main_player)")
                    get_game().main_player.get_inventory().remove_item(item, 1)
        if pygame.K_x in inputs.get_codes():
            print("bind")
            if len(get_game().main_player.get_inventory()) > self.selected - 1:
                print('2')
                item = get_game().main_player.get_inventory().get_index(self.selected - 1)
                self.elems.append(Bind(self, item))

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rectangle)
        for i, rect in enumerate(self.rectangles):
            if i + 1 == self.selected:
                pygame.draw.rect(surface, (0, 180, 180), pygame.Rect(rect.x - 3, rect.y - 3, rect.width + 6, rect.height + 6))
            pygame.draw.rect(surface, (180, 180, 180), rect)
            if len(get_game().main_player.get_inventory()) > i:
                item = get_game().main_player.get_inventory().get_index(i)
                img = pygame.transform.scale(item.get_sprite(), (rect.width, rect.height))
                surface.blit(img, rect)
                count_text = pygame.font.Font(Fonts.product_sans, 20).render(str(get_game().main_player.get_inventory().get_item_count(item)), True, (100, 100, 0))
                surface.blit(count_text, pygame.Rect(rect.x + rect.width - count_text.get_rect().width - 2, rect.y + rect.height - count_text.get_rect().height, count_text.get_rect().width, count_text.get_rect().height))

        for elem in self.elems:
            elem.draw(surface)
