import time

import pygame

from core.ui.element.element import Element
from util.colors import Colors
from util.fonts import Fonts
from util.input.controls import Controls, Mouse, Inputs


class KeyInput(Element):
    def __init__(self, base_value: str, x: int | str, y: int | str, width: int, height: int, color: tuple[int, int, int], code, background_color: tuple[int, int, int] = Colors.white):
        super().__init__(x, y, width, height, None)
        self.value: str = base_value
        self.visual_text: pygame.Surface = pygame.font.Font(Fonts.product_sans, self.height).render(base_value, True, color)
        self.color: tuple[int, int, int] = color
        self.background_color: tuple[int, int, int] = background_color
        self.selected_line_color: tuple[int, int, int] = Colors.red
        self.selected: bool = False
        self.cursor_time_switch: float = time.time()
        self.is_deleting: bool = False
        self.del_init_time: float = 0
        self.del_last_time: float = 0
        self.limit: int = -1
        self.unselect: bool = True
        self.has_cursor: bool = True
        self.code = code

    def activity(self, inputs) -> None:
        if self.rectangle.collidepoint(pygame.mouse.get_pos()):
            self.is_hover = True
            if Mouse.left.get_key() in inputs.get_codes():
                self.click()
                self.selected = True
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            self.is_hover = False
            if Mouse.left.get_key() in inputs.get_codes() and self.unselect:
                self.selected = False
        if self.selected:
            self.entry(inputs)
            self.change(self.value)

    def draw(self, surface) -> None:
        if self.background_color is not None:
            pygame.draw.rect(surface, self.background_color, self.rectangle)
        temp_text = 0
        if self.visual_text.get_rect().width > self.rectangle.width:
            self.visual_text = pygame.font.Font(Fonts.product_sans, self.height).render(self.value, True, self.color)
        surface.blit(self.visual_text, (self.rectangle.x + self.rectangle.width // 2 - self.visual_text.get_rect().width//2, self.rectangle.y), (temp_text, 0, self.visual_text.get_rect().width, self.rectangle.height))
        if self.selected and self.has_cursor:
            if self.cursor_time_switch+1 >= time.time():
                t1 = pygame.font.Font(Fonts.product_sans, self.height).render(">", True, self.color)
                t2 = pygame.font.Font(Fonts.product_sans, self.height).render("<", True, self.color)
                surface.blit(t1, (self.rectangle.x + 3, self.rectangle.y), t1.get_rect())
                surface.blit(t2, (self.rectangle.x + self.rectangle.width - 3 - t2.get_rect().width, self.rectangle.y), t2.get_rect())
            elif self.cursor_time_switch+2 <= time.time():
                self.cursor_time_switch = time.time()

    def change(self, text: str) -> None:
        self.visual_text = pygame.font.Font(Fonts.product_sans, self.height).render(text, True, self.color)

    def hover(self) -> int | None:
        return pygame.SYSTEM_CURSOR_IBEAM if self.rectangle.collidepoint(pygame.mouse.get_pos()) else None

    def get_text(self) -> str:
        return self.value

    def entry(self, inputs: Inputs) -> None:
        t = False
        for elem_ in inputs.raw_inputs:
            if elem_.type == pygame.KEYDOWN:
                self.value = pygame.key.name(elem_.key)
                if Controls.code_exists(self.code) and elem_.key != Controls.from_code(self.code).get_key():
                    Controls.change_key(elem_.key, self.code)
                    t = True
        if t:
            self.selected = False
