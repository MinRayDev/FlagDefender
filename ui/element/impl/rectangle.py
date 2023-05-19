import pygame
from pygame import Surface

from ui.element.element import Element
from util.input.controls import Inputs


class Rectangle(Element):
    """Class 'Rectangle' is a rectangle.

        Extends: 'Element'
        :ivar color: The color of the rectangle.
        :type color: tuple[int, int, int].
        :ivar hover_color: The hover color of the rectangle.
        :type hover_color: tuple[int, int, int].

    """
    color: tuple[int, int, int]
    hover_color: tuple[int, int, int]

    def __init__(self, x: int | str, y: int | str, width: int, height: int, color: tuple[int, int, int], hover_color: tuple[int, int, int] = None):
        """Constructor of the class 'Rectangle'.

            :param x: The x position of the rectangle.
            :type x: int | str.
            :param y: The y position of the rectangle.
            :type y: int | str.
            :param width: The width of the rectangle.
            :type width: int.
            :param height: The height of the rectangle.
            :type height: int.
            :param color: The color of the rectangle.
            :type color: tuple[int, int, int].
            :param hover_color: The hover color of the rectangle.
            :type hover_color: tuple[int, int, int].

        """
        super().__init__(x, y, width, height)
        self.color = color
        if hover_color is not None:
            self.hover_color = hover_color
        else:
            self.hover_color = self.color

    def activity(self, inputs: Inputs) -> None:
        """Method 'activity' is called every tick.

            :param inputs: The inputs of the user.
            :type inputs: Inputs.

        """
        super().activity(inputs)

    def draw(self, surface: Surface) -> None:
        """Draws the rectangle.

            :param surface: The surface to draw the rectangle on.
            :type surface: Surface.

        """
        # If the rectangle is hovered, draw the rectangle with the hover color, else draw the rectangle with the color.
        if self.is_hover:
            pygame.draw.rect(surface, self.hover_color, pygame.Rect(self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def hover(self) -> None:
        """Called when the element is hovered."""
        pass
