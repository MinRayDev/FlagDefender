import pygame

from core.ui.element.element import Element


class Button(Element):
    def __init__(self, x: int | str, y: int | str, width: int, height: int, color: tuple[int, int, int]):
        super().__init__(x, y, width, height)
        self.color: tuple[int, int, int] = color
        self.hover_color = self.color

    def activity(self, inputs) -> None:
        super().activity(inputs)

    def draw(self, surface) -> None:
        if self.is_hover:
            pygame.draw.rect(surface, self.hover_color, pygame.Rect(self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
