import pygame

from ui.element.element import Element
from util.instance import get_game


class ScrollPane(Element):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]):
        super().__init__(x, y, width, height, pygame.Rect(x, y, width, height))
        self.color: tuple[int, int, int] = color
        self.elems: list[Element] = []
        self.scroll: int = 0
        self.can_scroll_down: bool = False
        self.can_scroll_up: bool = False

    def activity(self, inputs) -> None:
        super().activity(inputs)
        if self.is_hover:
            self.scroll = 0
            self.can_scroll_down = False
            self.can_scroll_up = False
            for elem in self.elems:
                if elem.y + elem.height + 10 >= self.height + self.y:
                    self.can_scroll_down = True
                elif elem.y - 10 < self.y:
                    self.can_scroll_up = True
            for input_ in inputs.raw_inputs:
                if input_.type == pygame.MOUSEWHEEL:
                    if input_.y == -1 and self.can_scroll_down:
                        self.scroll += input_.y * 20
                    elif input_.y == 1 and self.can_scroll_up:
                        self.scroll += input_.y * 20
            for elem in self.elems:
                elem.y += self.scroll
                elem.rectangle = pygame.Rect(elem.x, elem.y, elem.width, elem.height)
                if elem.y <= self.height + self.y and elem.y + elem.height >= self.y:
                    elem.activity(inputs)

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rectangle)
        for elem in self.elems:
            if elem.y <= self.height + self.y and elem.y + elem.height >= self.y:
                elem.draw(surface)

    def hover(self) -> int | None:
        for elem in self.elems:
            if elem.y <= self.height + self.y and elem.y + elem.height >= self.y:
                if elem.hover() is not None and get_game().current_menu is not None:
                    if pygame.mouse.get_cursor() != elem.hover():
                        return elem.hover()
        return None
