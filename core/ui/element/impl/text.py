import pygame

from core.ui.element.element import Element
from util.fonts import Fonts


class Text(Element):
    def __init__(self, text: str, x: int, y: int, color: tuple[int, int, int], height: int = 30):
        self.content: str = text
        self.height = height
        self.text: pygame.Surface = pygame.font.Font(Fonts.product_sans, self.height).render(text, True, color)
        super().__init__(x, y, -1, self.height, self.text.get_rect())
        self.rectangle.x, self.rectangle.y = x, y
        self.color: tuple[int, int, int] = color

    def draw(self, surface) -> None:
        surface.blit(self.text, self.rectangle)

    def change(self, text: str) -> None:
        self.text = pygame.font.Font(Fonts.product_sans, self.height).render(text, True, self.color)

    def hover(self) -> int | None:
        pass
