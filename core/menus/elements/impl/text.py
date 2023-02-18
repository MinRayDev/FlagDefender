import pygame

from core.menus.elements.element import Element
from entities.Object import Object
from utils.fonts import Fonts


class Text(Element):
    def __init__(self, text, x, y, color):
        self.content = text
        self.text = pygame.font.Font(Fonts.chickenic, 30).render(text, True, color)
        super().__init__(x, y, -1, -1, self.text.get_rect())
        self.rectangle.x, self.rectangle.y = x, y
        self.color = color

    def activity(self, kwargs):
        pass

    def draw(self, surface):
        surface.blit(self.text, self.rectangle)

    def click(self):
        pass

    def change(self, text: str):
        self.text = pygame.font.Font(Fonts.chickenic, 30).render(text, True, self.color)

    def hover(self) -> int | None:
        pass
