from typing import List

import pygame

from utils.inputs.controls import Inputs


class Element:
    def __init__(self, x, y, width, height, rectangle):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_hover = False
        self.rectangle = rectangle

    def activity(self, inputs: Inputs):
        if self.rectangle.collidepoint(pygame.mouse.get_pos()):
            self.is_hover = True
            if 1 in inputs.get_codes():
                self.click()
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            self.is_hover = False

    def draw(self, surface):
        pass

    def click(self):
        pass

    def hover(self) -> int | None:
        return pygame.SYSTEM_CURSOR_HAND if self.rectangle.collidepoint(pygame.mouse.get_pos()) else None
