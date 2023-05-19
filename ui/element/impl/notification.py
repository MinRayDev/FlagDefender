import time

import pygame
from pygame import Surface

from ui.animation.animation import Animation
from ui.element.impl.button import Button
from ui.element.impl.text import Text
from ui.menu import Menu
from util.input.controls import Inputs
from util.instance import get_client


class Notification(Button):
    """Class 'Notification' is a notification.

        Extends: 'Button'
        :ivar text: The text of the notification.
        :type text: Text.
        :ivar gen_time: The time when the notification has been generated.
        :type gen_time: float.
        :ivar parent: The parent of the notification.
        :type parent: Menu.
        :ivar has_been_clicked: If the notification has been clicked.
        :type has_been_clicked: bool.
        :ivar close_started: If the notification has started to close.
        :type close_started: bool.
        :ivar animation: The animation of the notification.
        :type animation: Animation.

    """
    text_color: tuple[int, int, int]
    text: Text
    gen_time: float
    parent: Menu
    has_been_clicked: bool
    close_started: bool
    animation: Animation

    def __init__(self, text: str, color: tuple[int, int, int], text_color: tuple[int, int, int], menu: Menu):
        """Constructor of the class 'Notification'.

            :param text: The text of the notification.
            :type text: str.
            :param color: The color of the notification.
            :type color: tuple[int, int, int].
            :param text_color: The text color of the notification.
            :type text_color: tuple[int, int, int].
            :param menu: The parent of the notification.
            :type menu: Menu.

        """
        super().__init__(0, -get_client().get_screen().get_height() // 18, get_client().get_screen().get_width(), get_client().get_screen().get_height() // 18, color)
        self.text_color = text_color
        self.text = Text(text, 0, 0, self.text_color)
        self.text.rectangle.center = (self.width // 2 + self.x, self.height // 2 + self.y)
        self.gen_time = time.time()
        self.parent = menu
        self.has_been_clicked = False
        self.close_started = True
        self.animation = Animation(self, 10)
        self.animation.add_key(10, (self.x, 0))

    def draw(self, surface: Surface) -> None:
        """Draws the notification.

            :param surface: The surface to draw the notification on.
            :type surface: pygame.Surface.

        """
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
        self.text.draw(surface)

    def activity(self, inputs: Inputs) -> None:
        """Activities the notification.

            :param inputs: The inputs.
            :type inputs: Inputs.

        """
        # Activity of the button.
        super().activity(inputs)

        # Animation of the notification.
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
        """Kills the notification."""
        if self.animation.is_ended():
            if self in self.parent.elems:
                self.parent.elems.remove(self)
            del self

    def click(self) -> None:
        """Method 'click' is called when the notification is clicked."""
        self.has_been_clicked = True


def notify(menu: Menu, text: str, color: tuple[int, int, int], text_color: tuple[int, int, int]) -> None:
    """Method 'notify' notifies the user.

        :param menu: The menu.
        :type menu: Menu.
        :param text: The text of the notification.
        :type text: str.
        :param color: The color of the notification.
        :type color: tuple[int, int, int].
        :param text_color: The color of the text of the notification.
        :type text_color: tuple[int, int, int].

    """
    menu.elems.append(Notification(text, color, text_color, menu))


def warn(menu: Menu, text: str) -> None:
    """Method 'warn' warns the user.

        :param menu: The menu.
        :type menu: Menu.
        :param text: The text of the notification.
        :type text: str.

    """
    notify(menu, text, (244, 144, 12), (240, 240, 240))


def alert(menu: Menu, text: str) -> None:
    """Method 'alert' alerts the user.

        :param menu: The menu.
        :type menu: Menu.
        :param text: The text of the notification.
        :type text: str.

    """
    notify(menu, text, (221, 46, 68), (240, 240, 240))


def info(menu: Menu, text: str) -> None:
    """Method 'info' informs the user.

        :param menu: The menu.
        :type menu: Menu.
        :param text: The text of the notification.
        :type text: str.

    """
    notify(menu, text, (120, 177, 89), (240, 240, 240))
