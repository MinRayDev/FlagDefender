import pygame

from core.menus.elements.element import Element


class Checkbox(Element):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, pygame.Rect(x, y, width, height))
        self.color = color
        self.select_rect = pygame.Rect(x + 10, y + height // 2 - 10, 20, 20)
        self.selected = False

    def activity(self, inputs):
        if self.rectangle.collidepoint(pygame.mouse.get_pos()):
            self.is_hover = True
            if 1 in inputs.get_codes():
                self.click()
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            self.is_hover = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rectangle)
        if self.is_hover:
            pygame.draw.rect(surface, (114, 137, 218), pygame.Rect(self.x + 8, self.y + self.height // 2 - 12, 24, 24))

        pygame.draw.rect(surface, (255, 255, 255), self.select_rect)
        if self.selected:
            pygame.draw.rect(surface, (255, 0, 0), self.select_rect)

    def click(self):
        self.selected = not self.selected
