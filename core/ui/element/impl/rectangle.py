import pygame

from core.ui.element.element import Element


class Rectangle(Element):
    def __init__(self, x: int | str, y: int | str, width: int, height: int, color: tuple[int, int, int], hover_color: tuple[int, int, int] = None):
        super().__init__(x, y, width, height)
        self.color: tuple[int, int, int] = color
        if hover_color is not None:
            self.hover_color = hover_color
        else:
            self.hover_color = self.color

    def activity(self, inputs) -> None:
        super().activity(inputs)

    def draw(self, surface) -> None:
        if self.is_hover:
            pygame.draw.rect(surface, self.hover_color, pygame.Rect(self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
