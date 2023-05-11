import time

import pygame

from core.ui.animation.animation import Animation
from core.ui.element.impl.button import Button
from core.ui.element.impl.text import Text
from core.ui.menu import Menu
from util.instance import get_client


class Notification(Button):
    def __init__(self, text: str, color: tuple[int, int, int], text_color: tuple[int, int, int], menu: Menu):
        super().__init__(0, -get_client().get_screen().get_height() // 18, get_client().get_screen().get_width(), get_client().get_screen().get_height() // 18, color)
        self.color: tuple[int, int, int] = color
        self.text_color: tuple[int, int, int] = text_color
        self.text: Text = Text(text, 0, 0, self.text_color)
        self.text.rectangle.center = (self.width // 2 + self.x, self.height // 2 + self.y)
        self.gen_time: float = time.time()
        self.parent: Menu = menu
        self.has_been_clicked: bool = False
        self.close_started: bool = True
        self.animation: Animation = Animation(self, 10)
        self.animation.add_key(10, (self.x, 0))

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
        self.text.draw(surface)

    def activity(self, inputs) -> None:
        super().activity(inputs)
        if not self.animation.is_started():
            self.animation.start()
        self.animation.activity()
        if self.height // 2 + self.y != self.text.rectangle.center[1]:
            self.text.rectangle.center = (self.text.rectangle.center[0], self.height // 2 + self.y)
        if time.time() > self.gen_time + 3 or self.has_been_clicked:
            if self.close_started:
                self.animation = Animation(self, 10)
                self.animation.add_key(10, (self.x, 0-self.height))
                self.close_started = False
                self.animation.start()
            self.kill()

    def kill(self) -> None:
        if self.animation.is_ended():
            if self in self.parent.elems:
                self.parent.elems.remove(self)
            del self

    def click(self) -> None:
        self.has_been_clicked = True


def notify(menu: Menu, text: str, color: tuple[int, int, int], text_color: tuple[int, int, int]) -> None:
    menu.elems.append(Notification(text, color, text_color, menu))


def warn(menu: Menu, text: str) -> None:
    notify(menu, text, (244, 144, 12), (240, 240, 240))


def alert(menu: Menu, text: str) -> None:
    notify(menu, text, (221, 46, 68), (240, 240, 240))


def info(menu: Menu, text: str) -> None:
    notify(menu, text, (120, 177, 89), (240, 240, 240))
