import pygame

from entities.Object import Object
from utils.fonts import Fonts


class Text(Object):
    def __init__(self, text, x, y, color):
        super().__init__(x, y, None, -1, -1)
        self.text = pygame.font.Font(Fonts.chickenic, 30).render(text, True, color)
        self.rectangle = self.text.get_rect()
        self.rectangle.x = x
        self.rectangle.y = y
        self.color = color
        self.is_hover = False

    def activity(self, kwargs):
        pass

    def draw(self, surface):
        surface.blit(self.text, self.rectangle)

    def click(self):
        pass

    def change(self, text: str):
        self.text = pygame.font.Font(Fonts.chickenic, 30).render(text, True, self.color)