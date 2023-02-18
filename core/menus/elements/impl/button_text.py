import pygame

from core.menus.elements.impl.button import Button
from core.menus.elements.impl.text import Text


class ButtonText(Button):
    def __init__(self, x, y, width, height, text, color, text_color=(255, 255, 255)):
        super().__init__(x, y, width, height, pygame.Rect(x, y, width, height))
        self.color = color
        self.text_color = text_color
        self.text = Text(text, 0, 0, (153, 170, 181))
        self.text.rectangle.center = (width // 2 + x, height // 2 + y)

    def draw(self, surface):
        super().draw(surface)
        self.text.draw(surface)

    def activity(self, inputs):
        super().activity(inputs)
        if self.height//2 + self.y != self.text.rectangle.center[1]:
            self.text.rectangle.center = (self.text.rectangle.center[0], self.height//2 + self.y)