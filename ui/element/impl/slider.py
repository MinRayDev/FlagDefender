import pygame

from ui.element.element import Element


class Slider(Element):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int], min_number: int = 0, max_number: int = 100, value: int = 0, selector_color: tuple[int, int, int] = None):
        self.rectangle_line: pygame.Rect = pygame.Rect(x, y, width, height)
        self.color: tuple[int, int, int] = color
        self.min = min_number
        self.max = max_number

        if selector_color is None:
            self.selector_color: tuple[int, int, int] = color
        else:
            self.selector_color = selector_color
        self.rectangle_selector: pygame.Rect = pygame.Rect(x-height+2//2, y-3, height+2, height+6)
        self.is_dragged: bool = False
        super().__init__(x, y, width, height, self.rectangle_selector)
        self.set_value(value)

    def activity(self, _) -> None:
        if self.rectangle_selector.collidepoint(pygame.mouse.get_pos()) or self.is_dragged:
            self.is_hover = True
            if pygame.mouse.get_pressed()[0] == 1:
                self.is_dragged = True
                self.drag()
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            else:
                self.is_dragged = False
        else:
            self.is_hover = False

    def draw(self, surface) -> None:
        if self.is_hover:
            pygame.draw.rect(surface, (114, 137, 218), pygame.Rect(self.x-2, self.y-2, self.width+4, self.height+4))
        pygame.draw.rect(surface, self.color, self.rectangle_line)
        pygame.draw.circle(surface, self.selector_color, (self.rectangle_selector.x + self.rectangle_selector.width//2, self.rectangle_selector.y + self.rectangle_selector.height//2), self.rectangle_selector.height//1.5)

    def drag(self) -> None:
        if self.rectangle_line.x <= pygame.mouse.get_pos()[0] - self.rectangle_selector.width//2 and pygame.mouse.get_pos()[0] + self.rectangle_selector.width//2 <= self.rectangle_line.x+self.rectangle_line.width:
            self.rectangle_selector.x = pygame.mouse.get_pos()[0] - self.rectangle_selector.width//2
        elif pygame.mouse.get_pos()[0] - self.rectangle_selector.width//2 < self.rectangle_line.x:
            self.rectangle_selector.x = self.rectangle_line.x - self.rectangle_selector.width//2
        elif pygame.mouse.get_pos()[0] + self.rectangle_selector.width//2 > self.rectangle_line.x + self.rectangle_line.width:
            self.rectangle_selector.x = self.rectangle_line.x + self.rectangle_line.width - self.rectangle_selector.width // 2

    def get(self) -> float:
        abs_value: int = self.rectangle_selector.x+self.rectangle_selector.width//2 - self.rectangle_line.x
        return self.min + float((abs_value/self.rectangle_line.width)*self.max)

    def set_value(self, value: float) -> None:
        t = ((value - self.min)/self.max)*self.rectangle_line.width
        self.rectangle_selector.x = self.rectangle_line.x + t - self.rectangle_selector.width//2
