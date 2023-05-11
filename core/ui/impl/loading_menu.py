from __future__ import annotations

import time

import pygame
from pygame import Surface

from core.ui.element.impl.rectangle import Rectangle
from core.ui.element.impl.text import Text
from core.ui.menu import Menu
from util.colors import Colors
from util.instance import get_game
from util.time_util import has_elapsed


class LoadingMenu(Menu):
    def __init__(self, parent: Menu, check_limt: int, base_text: str):
        from util.instance import get_client
        super().__init__("Main Menu", parent)
        self.client = get_client()
        self.checks: list[tuple[int, str, str]] = []
        base_color = Colors.base_color
        text_color = Colors.text_color
        self.check_limt = check_limt
        x = get_client().get_screen().get_width() / 2 - (
                    get_client().get_screen().get_width() - get_client().get_screen().get_width() / 4) / 2
        y = get_client().get_screen().get_height() - get_client().get_screen().get_height() / 4
        width = get_client().get_screen().get_width() - get_client().get_screen().get_width() / 4
        height = get_client().get_screen().get_height() / 20
        self.bar_bg_rectangle = Rectangle(x, y, width, height, base_color)
        self.bar_rectangle = Rectangle(x, y, 0, height, text_color)
        self.check_passed = Text(f"Check 0/{check_limt}", x + width, y, text_color)
        self.check_passed.rectangle.x -= self.check_passed.rectangle.width - 10
        self.check_passed.rectangle.y -= (self.check_passed.rectangle.height + 10)
        self.current_check = Text(base_text, x, y, text_color, 21)
        self.current_check.rectangle.y -= (self.current_check.rectangle.height + 10)
        self.end_time = 0
        self.elems = [self.bar_bg_rectangle, self.bar_rectangle, self.check_passed, self.current_check]

    def activity(self):
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
        self.bar_rectangle.rectangle.width = self.bar_bg_rectangle.width * (len(self.checks)/self.check_limt)
        self.bar_rectangle.width = self.bar_bg_rectangle.width * (len(self.checks)/self.check_limt)
        self.check_passed.change(f"Check {len(self.checks)}/{self.check_limt}")
        if len(self.checks) > 0:
            self.current_check.change(f"{self.checks[-1][1]} ({self.checks[-1][2]})")
        if len(self.checks) == self.check_limt:
            if self.end_time == 0:
                self.end_time = time.time()
            elif has_elapsed(self.end_time, 0.5):
                print("----------------------------------------------------------------")
                get_game().reset_menu()

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface, Colors.base_color,
                         pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        super().draw(surface)

    def end(self):
        get_game().set_menu(self.prev)

    def add_check(self, name: str, source: str):
        self.checks.append((len(self.checks) + 1, name, source))

    def append_check(self, index: int, name: str, source: str):
        self.checks.append((index, name, source))
