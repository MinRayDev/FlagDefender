import pygame

from entities.Object import Object


class Slider(Object):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, None, width, height)
        self.rectangle_line = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_hover = False
        self.rectangle_selector = pygame.Rect(x-height+2//2, y-3, height+2, height+6)
        self.test = False

    def activity(self, kwargs):
        if self.rectangle_selector.collidepoint(pygame.mouse.get_pos()) or self.test:
            self.is_hover = True
            if pygame.mouse.get_pressed()[0] == 1:
                self.test = True
                self.drag()
                self.get()
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            else:
                self.test = False
        else:
            self.is_hover = False

    def draw(self, surface):
        if self.is_hover:
            pygame.draw.rect(surface, (114, 137, 218), pygame.Rect(self.x-2, self.y-2, self.width+4, self.height+4))
        pygame.draw.rect(surface, self.color, self.rectangle_selector)
        pygame.draw.rect(surface, self.color, self.rectangle_line)

    def drag(self):
        if self.rectangle_line.x <= pygame.mouse.get_pos()[0] - self.rectangle_selector.width//2 and pygame.mouse.get_pos()[0] + self.rectangle_selector.width//2 <= self.rectangle_line.x+self.rectangle_line.width:
            self.rectangle_selector.x = pygame.mouse.get_pos()[0] - self.rectangle_selector.width//2
        elif pygame.mouse.get_pos()[0] - self.rectangle_selector.width//2 < self.rectangle_line.x:
            self.rectangle_selector.x = self.rectangle_line.x - self.rectangle_selector.width//2
        elif pygame.mouse.get_pos()[0] + self.rectangle_selector.width//2 > self.rectangle_line.x + self.rectangle_line.width:
            self.rectangle_selector.x = self.rectangle_line.x + self.rectangle_line.width - self.rectangle_selector.width // 2

    def get(self) -> float:
        abs_value: int = self.rectangle_selector.x+self.rectangle_selector.width//2 - self.rectangle_line.x
        return float((abs_value/self.rectangle_line.width)*100)

    def hover(self) -> int | None:
        return pygame.SYSTEM_CURSOR_HAND if self.rectangle_selector.collidepoint(pygame.mouse.get_pos()) else None
