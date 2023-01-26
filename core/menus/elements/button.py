import pygame

from entities.Object import Object


class Button(Object):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, None, width, height)
        self.rectangle = pygame.Rect(x, y, width, height)
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
        if self.is_hover:
            pygame.draw.rect(surface, (114, 137, 218),
                             pygame.Rect(self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(surface, self.color, self.rectangle)

    def click(self):
        pass

    def hover(self) -> int | None:
        return pygame.SYSTEM_CURSOR_HAND if self.rectangle.collidepoint(pygame.mouse.get_pos()) else None
