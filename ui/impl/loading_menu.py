from __future__ import annotations

import math
import time
from typing import Callable, TYPE_CHECKING

import pygame
from pygame import Surface, SurfaceType


from ui.element.impl.rectangle import Rectangle
from ui.element.impl.text import Text
from ui.menu import Menu
from util.colors import Colors
from util.input.controls import Inputs
from util.instance import get_game, get_client
from util.time_util import has_elapsed
if TYPE_CHECKING:
    from core.client import Client


class LoadingMenu(Menu):
    """Class 'LoadingMenu' is the loading menu of the game.

        Extends the class 'Menu'.
        :ivar client: The client of the game.
        :type client: Client.
        :ivar after: The function to call after the loading is done.
        :type after: Callable.
        :ivar checks: The checks to do.
        :type checks: list[tuple[int, str, str]].
        :ivar check_limt: The limit of checks.
        :type check_limt: int.
        :ivar bar_bg_rectangle: The background rectangle of the loading bar.
        :type bar_bg_rectangle: Rectangle.
        :ivar bar_rectangle: The rectangle of the loading bar.
        :type bar_rectangle: Rectangle.
        :ivar anim_holder: The animation holder of the loading bar.
        :type anim_holder: AnimationHolder.
        :ivar check_passed: The text of the checks passed.
        :type check_passed: Text.
        :ivar current_check: The text of the current check.
        :type current_check: Text.
        :ivar end_time: The end time of the loading.
        :type end_time: int.

    """
    client: 'Client'
    after: Callable
    checks: list[tuple[int, str, str]]
    check_limt: int
    bar_bg_rectangle: Rectangle
    bar_rectangle: Rectangle
    anim_holder: AnimationHolder
    check_passed: Text
    current_check: Text
    end_time: float

    def __init__(self, parent: Menu, check_limt: int, base_text: str, after: Callable = None):
        """Constructor of the class 'LoadingMenu'.

            :param parent: The parent of the menu.
            :type parent: Menu.
            :param check_limt: The limit of checks.
            :type check_limt: int.
            :param base_text: The base text of the checks.
            :type base_text: str.
            :param after: The function to call after the loading is done.
            :type after: Callable.

        """
        super().__init__("Main Menu", parent)
        self.client = get_client()
        self.after = get_game().reset_menu
        if after is not None:
            self.after = after
        self.checks = []
        text_color: tuple[int, int, int] = Colors.text_color
        self.check_limt = check_limt

        screen: SurfaceType = get_client().get_screen()
        s_width: int = screen.get_width()
        s_height: int = screen.get_height()

        x: int = int(s_width / 2 - (s_width - s_width / 4) / 2)
        y: int = int(s_height - s_height / 4)
        width: int = int(s_width - s_width / 4)
        height: int = int(s_height / 20)
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

    def activity(self) -> None:
        """Method 'activity' updates the menu."""
        inputs: Inputs = self.get_queue()
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

        target_bar_width: float = self.bar_bg_rectangle.width * (len(self.checks) / self.check_limt)
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
        """Method 'draw' draws the menu.

            :param surface: The surface to draw on.
            :type surface: Surface.

        """
        pygame.draw.rect(surface, Colors.base_color,
                         pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        super().draw(surface)
        self.anim_holder.update()

    def end(self) -> None:
        """Method 'end' ends the menu."""
        get_game().set_menu(self.prev)

    def add_check(self, name: str, source: str) -> None:
        """Method 'add_check' adds a check to the loading."""
        self.checks.append((len(self.checks) + 1, name, source))


class AnimationHolder:
    """Class 'AnimationHolder' holds the animation of the loading bar.

        :param func: The function to use for the animation.
        :type func: Callable[[float], float].
        :param target: The target value of the animation.
        :type target: int.

    """
    def __init__(self, func: Callable[[float], float], target: int = 100):
        """Constructor of the class 'AnimationHolder'.

            :param func: The function to use for the animation.
            :type func: Callable[[float], float].
            :param target: The target value of the animation.
            :type target: int.

        """
        self.__func = func
        self.__value = 0
        self.__target = target

    def update(self) -> None:
        """Method 'update' updates the animation."""
        if self.__value >= self.__target:
            return
        self.__value += 5
        if self.__value > self.__target:
            self.__value = self.__target

    @property
    def percentage(self) -> float:
        """Property 'percentage' returns the percentage of the animation."""
        if self.__target == 0:
            return 0
        return self.__value / self.__target

    @property
    def translated_percentage(self) -> float:
        """Property 'translated_percentage' returns the translated percentage of the animation."""
        return self.__func(self.percentage) * self.__target

    @property
    def value(self) -> int:
        """Property 'value' returns the value of the animation."""
        return self.__value

    @property
    def target(self) -> int:
        """Property 'target' returns the target of the animation."""
        return self.__target

    @target.setter
    def target(self, value: int) -> None:
        """Property 'target' sets the target of the animation.

            :param value: The new target.
            :type value: int.

        """
        self.__target = value

    def reset(self) -> None:
        """Method 'reset' resets the animation."""
        self.__value = 0


def ease_out_quint(percentage: float) -> float:
    """Function 'ease_out_quint' returns the percentage of the animation.

        :param percentage: The percentage of the animation.
        :type percentage: float.

        :return: The percentage of the animation.
        :rtype: float.

    """
    return 1 - (1. - percentage) ** 5


def ease_out_circ(percentage: float) -> float:
    """Function 'ease_out_circ' returns the percentage of the animation.

        :param percentage: The percentage of the animation.
        :type percentage: float.

    """
    return math.sqrt(1 - (percentage - 1) ** 2)
