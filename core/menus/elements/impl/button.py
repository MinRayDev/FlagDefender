import pygame

from core.menus.elements.element import Element


class Button(Element):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, pygame.Rect(x, y, width, height))
        self.color = color

    def activity(self, inputs):
        super().activity(inputs)

    def draw(self, surface):
        if self.is_hover:
            pygame.draw.rect(surface, (114, 137, 218), pygame.Rect(self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
