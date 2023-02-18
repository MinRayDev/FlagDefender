import time

import pygame

from core.game import Game
from core.menus.animations.Test import Animation
from core.menus.elements.element import Element
from core.menus.elements.impl.button import Button
from core.menus.elements.impl.text import Text
from core.menus.menu import Menu


class Notification(Button):
    def __init__(self, text, color, text_color, menu: Menu):
        super().__init__(0, -Game.instance.screen.get_height() // 18, Game.instance.screen.get_width(),
                         Game.instance.screen.get_height() // 18,
                         pygame.Rect(0, 0, Game.instance.screen.get_width(), Game.instance.screen.get_height()))
        self.color = color
        self.text_color = text_color
        self.text = Text(text, 0, 0, self.text_color)
        self.text.rectangle.center = (self.width // 2 + self.x, self.height // 2 + self.y)
        self.gen_time = time.time()
        self.parent = menu
        self.deploying = True
        self.closing = True
        self.iterations = 10
        self.test = 0
        self.has_been_clicked = False
        self.close_started = True
        self.animation = Animation(self, 10)
        self.animation.add_key(3, (self.x, self.y+self.height))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
        self.text.draw(surface)

    def activity(self, inputs):
        super().activity(inputs)
        if self.deploy() and self.animation.last + 0.01 < time.time() and self.animation.test < self.animation.iterations:
            self.animation.aa()
        elif self.deploying:
            self.deploying = False
        if self.height // 2 + self.y != self.text.rectangle.center[1]:
            self.text.rectangle.center = (self.text.rectangle.center[0], self.height // 2 + self.y)
        if time.time() > self.gen_time + 3 or self.has_been_clicked:
            if self.close_started:
                self.close_started = False
                self.last = time.time()
                self.test = 0
            self.kill()

    def kill(self):

        if self.y >= -self.height and self.closing and self.last + 0.01 < time.time() and self.test < self.iterations:
            self.last = time.time()
            self.test += 1
            self.y -= self.height // self.iterations
            self.rectangle.y = self.y
        elif self.test >= self.iterations:
            if self in self.parent.elems:
                self.parent.elems.remove(self)
            del self

    def click(self):
        self.has_been_clicked = True

    def deploy(self):
        # v=d/t
        return self.y <= 0 and self.deploying


def notify(menu: Menu, text: str, color: tuple[int, int, int], text_color: tuple[int, int, int]):
    menu.elems.append(Notification(text, color, text_color, menu))


def warn(menu: Menu, text: str):
    notify(menu, text, (244, 144, 12), (220, 220, 220))


def alert(menu: Menu, text: str):
    notify(menu, text, (221, 46, 68), (220, 220, 220))


def info(menu: Menu, text: str):
    notify(menu, text, (120, 177, 89), (220, 220, 220))
