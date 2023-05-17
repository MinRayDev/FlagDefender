from __future__ import annotations

import math
import time
from typing import Callable

import pygame
from pygame import Surface

from ui.element.impl.rectangle import Rectangle
from ui.element.impl.text import Text
from ui.menu import Menu
from util.colors import Colors
from util.instance import get_game
from util.time_util import has_elapsed


class LoadingMenu(Menu):
    def __init__(self, parent: Menu, check_limt: int, base_text: str, after: Callable = None):
        from util.instance import get_client
        super().__init__("Main Menu", parent)
        self.client = get_client()
        self.after = get_game().reset_menu
        if after is not None:
            self.after = after
        self.checks: list[tuple[int, str, str]] = []
        base_color = Colors.base_color
        text_color = Colors.text_color
        self.check_limt = check_limt
        x =  int(get_client().get_screen().get_width() / 2 - (
                get_client().get_screen().get_width() - get_client().get_screen().get_width() / 4) / 2)
        y = int(get_client().get_screen().get_height() - get_client().get_screen().get_height() / 4)
        width =  int(get_client().get_screen().get_width() - get_client().get_screen().get_width() / 4)
        height =  int(get_client().get_screen().get_height() / 20)
        self.bar_bg_rectangle = Rectangle(x, y, width, height, Colors.crust)
        self.bar_rectangle = Rectangle(x, y, 0, height, text_color)

        self.anim_holder = AnimationHolder(ease_out_circ, 0)

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

        for elem in self.elems:
            if elem.hover() is not None and get_game().current_menu is not None:
                if pygame.mouse.get_cursor() != elem.hover():
                    pygame.mouse.set_cursor(elem.hover())
                    break
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        target_bar_width = self.bar_bg_rectangle.width * (len(self.checks) / self.check_limt)
        self.anim_holder.target = target_bar_width * (len(self.checks) / self.check_limt)

        self.bar_rectangle.rectangle.width = self.anim_holder.translated_percentage
        self.bar_rectangle.width = self.anim_holder.translated_percentage

        self.check_passed.change(f"Check {len(self.checks)}/{self.check_limt}")
        if len(self.checks) > 0:
            self.current_check.change(f"{self.checks[-1][1]} ({self.checks[-1][2]})")
        if len(self.checks) == self.check_limt:
            if self.end_time == 0:
                self.end_time = time.time()
            elif has_elapsed(self.end_time, 3):
                self.after()

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface, Colors.base_color,
                         pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        super().draw(surface)
        self.anim_holder.update()

    def end(self):
        get_game().set_menu(self.prev)

    def add_check(self, name: str, source: str):
        self.checks.append((len(self.checks) + 1, name, source))

    def append_check(self, index: int, name: str, source: str):
        self.checks.append((index, name, source))


class AnimationHolder:
    def __init__(self, func: Callable[[float], float], target: int = 100):
        self.__func = func
        self.__value = 0
        self.__target = target

    def update(self):
        if self.__value >= self.__target:
            return
        self.__value += 5
        if self.__value > self.__target:
            self.__value = self.__target

    @property
    def percentage(self):
        if self.__target == 0:
            return 0
        return self.__value / self.__target

    @property
    def translated_percentage(self):
        return self.__func(self.percentage) * self.__target

    @property
    def value(self) -> int:
        return self.__value

    @property
    def target(self) -> int:
        return self.__target

    @target.setter
    def target(self, value: int):
        self.__target = value

    def reset(self):
        self.__value = 0


def ease_out_quint(percentage: float) -> float:
    return 1 - (1. - percentage) ** 5


def ease_out_circ(percentage: float) -> float:
    return math.sqrt(1 - (percentage - 1) ** 2)
