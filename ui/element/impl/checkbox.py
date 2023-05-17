import pygame

from ui.element.element import Element
from util.colors import Colors


class Checkbox(Element):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]):
        super().__init__(x, y, width, height, pygame.Rect(x, y, width, height))
        self.color: tuple[int, int, int] = color
        self.select_rect: pygame.Rect = pygame.Rect(x + 10, y + height // 2 - 10, 20, 20)
        self.selected: bool = False

    def activity(self, inputs) -> None:
        if self.rectangle.collidepoint(pygame.mouse.get_pos()):
            self.is_hover = True
            if 1 in inputs.get_codes():
                self.click()
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            self.is_hover = False

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rectangle)
        if self.is_hover:
            pygame.draw.rect(surface, (114, 137, 218), pygame.Rect(self.x + 8, self.y + self.height // 2 - 12, 24, 24))

        pygame.draw.rect(surface, Colors.white, self.select_rect)
        if self.selected:
            pygame.draw.rect(surface, Colors.red, self.select_rect)

    def click(self) -> None:
        self.selected = not self.selected
