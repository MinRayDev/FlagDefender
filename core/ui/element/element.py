from typing import List

import pygame

from util.input.controls import Inputs



class Element:
    def __init__(self, x: int | str, y: int | str, width: int, height: int, rectangle: pygame.Rect = None):
        from util.instance import get_client
        if isinstance(x, str):
            if x == "CENTER":
                self.x = get_client().get_screen().get_width()//2 - width//2
            else:
                raise ValueError(f"Invalid x position: {x}")
        else:
            self.x: int = x
        if isinstance(y, str):
            if y == "CENTER":
                self.y = get_client().get_screen().get_height() // 2 - height // 2
            else:
                raise ValueError(f"Invalid x position: {x}")
        else:
            self.y: int = y
        self.width: int = width
        self.height: int = height
        self.is_hover: bool = False
        if rectangle is not None:
            self.rectangle: pygame.Rect = rectangle
        else:
            self.rectangle: pygame.Rect = pygame.Rect(self.x, self.y, width, height)

    def activity(self, inputs: Inputs) -> None:
        if self.rectangle.collidepoint(pygame.mouse.get_pos()):
            self.is_hover = True
            if 1 in inputs.get_codes():
                self.click()
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            self.is_hover = False

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def click(self) -> None:
        pass

    def hover(self) -> int | None:
        return pygame.SYSTEM_CURSOR_HAND if self.rectangle.collidepoint(pygame.mouse.get_pos()) else None
