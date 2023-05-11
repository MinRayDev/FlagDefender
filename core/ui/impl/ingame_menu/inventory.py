from __future__ import annotations

import time

import pygame
from pygame import Surface

from core.ui.element.element import Element
from core.ui.game_menu import GameMenu
from core.world import Facing
from util.fonts import Fonts
from util.input.controls import Controls
from util.instance import get_game, get_client
from util.world_util import drop


class InventoryMenu(GameMenu):
    def __init__(self):
        super().__init__("Inventory Menu")
        screen_width = get_client().get_screen().get_width()
        screen_height = get_client().get_screen().get_height()
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
        super().activity()
        inputs = self.get_queue()
        for elem in self.elems:
            elem.activity(inputs)
            pass

        for elem in self.elems:
            if elem.hover() is not None and get_game().current_menu is not None:
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
        if Controls.drop.get_code() in inputs.get_codes():
            if len(get_game().current_level.main_player.get_inventory()) > self.selected-1:
                item = get_game().current_level.main_player.get_inventory().get_index(self.selected-1)
                p_entity = get_game().current_level.main_player.entity
                get_game().current_level.main_player.get_inventory().remove_item(item, 1)
                match p_entity.facing:
                    case Facing.EAST:
                        drop(item, p_entity.x + p_entity.width + 10, p_entity.world)
                    case Facing.WEST:
                        drop(item, p_entity.x - 48 - 10, p_entity.world)
        if Controls.use.get_code() in inputs.get_codes():
            if len(get_game().current_level.main_player.get_inventory()) > self.selected - 1:
                item = get_game().current_level.main_player.get_inventory().get_index(self.selected - 1)
                if item.has_usage():
                    exec(item.get_usage() + "()")
                    get_game().current_level.main_player.get_inventory().remove_item(item, 1)

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface, (200, 200, 200), self.rectangle)
        for i, rect in enumerate(self.rectangles):
            if i + 1 == self.selected:
                pygame.draw.rect(surface, (0, 180, 180), pygame.Rect(rect.x - 3, rect.y - 3, rect.width + 6, rect.height + 6))
            pygame.draw.rect(surface, (180, 180, 180), rect)
            if len(get_game().current_level.main_player.get_inventory()) > i:
                item = get_game().current_level.main_player.get_inventory().get_index(i)
                img = pygame.transform.scale(item.get_sprite(), (rect.width, rect.height))
                surface.blit(img, rect)
                count_text = pygame.font.Font(Fonts.product_sans, 20).render(str(get_game().current_level.main_player.get_inventory().get_item_count(item)), True, (100, 100, 0))
                surface.blit(count_text, pygame.Rect(rect.x + rect.width - count_text.get_rect().width - 2, rect.y + rect.height - count_text.get_rect().height, count_text.get_rect().width, count_text.get_rect().height))

        for elem in self.elems:
            elem.draw(surface)
