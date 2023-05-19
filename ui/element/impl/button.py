import pygame
from pygame import Surface

from ui.element.element import Element


class Button(Element):
    """Class 'Button' is a button.

        Extends: 'Element'
        :ivar color: The color of the button.
        :type color: tuple[int, int, int].
        :ivar hover_color: The hover color of the button.
        :type hover_color: tuple[int, int, int].

    """
    color: tuple[int, int, int]
    hover_color: tuple[int, int, int]

    def __init__(self, x: int | str, y: int | str, width: int, height: int, color: tuple[int, int, int]):
        """Constructor of the class 'Button'.

            :param x: The x position of the button.
            :type x: int | str.
            :param y: The y position of the button.
            :type y: int | str.
            :param width: The width of the button.
            :type width: int.
            :param height: The height of the button.
            :type height: int.
            :param color: The color of the button.
            :type color: tuple[int, int, int].

        """
        super().__init__(x, y, width, height)
        self.color = color
        self.hover_color = self.color

    def draw(self, surface: Surface) -> None:
        """Draws the button.

            :param surface: The surface to draw the button on.
            :type surface: pygame.Surface.

        """
        # If the button is hovered, draw the button with the hover color, else draw the button with the color.
        if self.is_hover:
            pygame.draw.rect(surface, self.hover_color, pygame.Rect(self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
