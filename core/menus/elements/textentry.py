import pygame

from entities.Object import Object
from utils.fonts import Fonts


class TextEntry(Object):
    def __init__(self, placeholder, x, y, color):
        super().__init__(x, y, None, -1, -1)
        self.placeholder = placeholder
        self.visual_text = pygame.font.Font(Fonts.chickenic, 30).render(placeholder, True, color)
        self.rectangle = self.visual_text.get_rect()
        self.rectangle.x = x
        self.rectangle.y = y
        self.color = color
        self.is_hover = False

    def activity(self, kwargs):
        if self.rectangle.collidepoint(pygame.mouse.get_pos()):
            self.is_hover = True
            if 1 in kwargs["m_events"]:
                self.click()
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            self.is_hover = False

    def draw(self, surface):
        surface.blit(self.visual_text, self.rectangle)

    def click(self):
        pass

    def change(self, text: str):
        self.visual_text = pygame.font.Font(Fonts.chickenic, 30).render(text, True, self.color)

    def hover(self) -> int | None:
        return pygame.SYSTEM_CURSOR_IBEAM if self.rectangle.collidepoint(pygame.mouse.get_pos()) else None
