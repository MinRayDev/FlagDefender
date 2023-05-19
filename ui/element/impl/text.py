import pygame
from pygame import Surface

from ui.element.element import Element
from util.fonts import Fonts


class Text(Element):
    """Class 'Text' is a text element.

        Extends: 'Element'
        :ivar content: The text content of the text element.
        :type content: str.
        :ivar text: The text of the text element.
        :type text: pygame.Surface.
        :ivar color: The color of the text element.
        :type color: tuple[int, int, int].

    """
    content: str
    text: Surface
    color: tuple[int, int, int]

    def __init__(self, text: str, x: int, y: int, color: tuple[int, int, int], height: int = 30):
        """Constructor of the class 'Text'.

            :param text: The text content of the text element.
            :type text: str.
            :param x: The x position of the text element.
            :type x: int.
            :param y: The y position of the text element.
            :type y: int.
            :param color: The color of the text element.
            :type color: tuple[int, int, int].
            :param height: The height of the text element.
            :type height: int.

        """
        self.content = text
        self.text = pygame.font.Font(Fonts.product_sans, height).render(text, True, color)
        super().__init__(x, y, -1, height, self.text.get_rect())
        self.rectangle.x, self.rectangle.y = x, y
        self.color = color

    def draw(self, surface: Surface) -> None:
        """Draws the text element.

            :param surface: The surface to draw the text element on.
            :type surface: Surface.

        """
        surface.blit(self.text, self.rectangle)

    def change(self, text: str) -> None:
        """Changes the text of the text element.

            :param text: The new text of the text element.
            :type text: str.

        """
        self.text = pygame.font.Font(Fonts.product_sans, self.height).render(text, True, self.color)

    def hover(self) -> None:
        """Returns the index of the hovered character."""
        pass
