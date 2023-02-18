import pygame

from core.game import Game
from core.menus.elements.element import Element


class ScrollPane(Element):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, pygame.Rect(x, y, width, height))
        self.color = color
        self.elems: list[Element] = []
        self.scroll = 0
        self.can_scroll_d = False
        self.can_scroll_u = False

    def activity(self, inputs):
        super().activity(inputs)
        if self.is_hover:
            self.scroll = 0
            self.can_scroll_d = False
            self.can_scroll_u = False
            for elem in self.elems:
                if elem.y + elem.height + 10 >= self.height + self.y:
                    self.can_scroll_d = True
                elif elem.y - 10 < self.y:
                    self.can_scroll_u = True
            for input_ in inputs.raw_inputs:
                if input_.type == pygame.MOUSEWHEEL:
                    if input_.y == -1 and self.can_scroll_d:
                        self.scroll += input_.y * 10
                    elif input_.y == 1 and self.can_scroll_u:
                        self.scroll += input_.y * 10
            for elem in self.elems:
                elem.y += self.scroll
                elem.rectangle = pygame.Rect(elem.x, elem.y, elem.width, elem.height)
                if elem.y <= self.height + self.y and elem.y + elem.height >= self.y:
                    elem.activity(inputs)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rectangle)
        for elem in self.elems:
            if elem.y <= self.height + self.y and elem.y + elem.height >= self.y:
                elem.draw(surface)

    def hover(self) -> int | None:
        for elem in self.elems:
            if elem.y <= self.height + self.y and elem.y + elem.height >= self.y:
                if elem.hover() is not None and Game.instance.actual_menu is not None:
                    if pygame.mouse.get_cursor() != elem.hover():
                        return elem.hover()
        return None
