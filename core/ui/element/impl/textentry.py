import time

import pygame

from core.ui.element.element import Element
from util.colors import Colors
from util.fonts import Fonts
from util.input.controls import Controls, Mouse, Inputs


#TODO opti code
class TextEntry(Element):
    def __init__(self, placeholder: str, x: int | str, y: int | str, width: int, height: int, color: tuple[int, int, int], background_color: tuple[int, int, int] = Colors.white):
        super().__init__(x, y, width, height, None)
        self.placeholder: str = placeholder
        self.visual_text: pygame.Surface = pygame.font.Font(Fonts.product_sans, self.height).render(placeholder, True, color)
        self.color: tuple[int, int, int] = color
        self.background_color: tuple[int, int, int] = background_color
        self.selected_line_color: tuple[int, int, int] = Colors.red
        self.selected: bool = False
        self.cursor_time_switch: float = time.time()
        self.text: str = ""
        self.is_deleting: bool = False
        self.del_init_time: float = 0
        self.del_last_time: float = 0
        self.limit: int = -1
        self.unselect: bool = True
        self.has_cursor: bool = True

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
            self.change(self.text)

    def draw(self, surface) -> None:
        if self.background_color is not None:
            pygame.draw.rect(surface, self.background_color, self.rectangle)
        temp_text = 0
        if self.visual_text.get_rect().width > self.rectangle.width:

            for i, char in enumerate(self.text):
                if pygame.font.Font(Fonts.product_sans, self.height).render(self.text[:i] + char, True, self.color).get_rect().width >= self.rectangle.width:
                    temp_text += pygame.font.Font(Fonts.product_sans, self.height).render(char, True, self.color).get_rect().width
            self.visual_text = pygame.font.Font(Fonts.product_sans, self.height).render(self.text, True, self.color)
        surface.blit(self.visual_text, (self.rectangle.x, self.rectangle.y), (temp_text, 0, self.visual_text.get_rect().width, self.rectangle.height))
        if self.selected and self.has_cursor:
            if self.cursor_time_switch+1 >= time.time():
                pygame.draw.rect(surface, self.selected_line_color, pygame.Rect(self.rectangle.x + self.visual_text.get_rect().width - temp_text, self.rectangle.y+2, 3, self.rectangle.height - 4))
            elif self.cursor_time_switch+2 <= time.time():
                self.cursor_time_switch = time.time()

    def change(self, text: str) -> None:
        self.visual_text = pygame.font.Font(Fonts.product_sans, self.height).render(text, True, self.color)

    def hover(self) -> int | None:
        return pygame.SYSTEM_CURSOR_IBEAM if self.rectangle.collidepoint(pygame.mouse.get_pos()) else None

    def get_text(self) -> str:
        return self.text

    def entry(self, inputs: Inputs) -> None:
        for elem_ in inputs.raw_inputs:
            if elem_.type == pygame.TEXTINPUT and (len(self.text) < self.limit or self.limit == -1):
                self.text += elem_.text
            elif elem_.type == pygame.KEYDOWN and elem_.key == pygame.K_BACKSPACE:
                self.is_deleting = True
                self.del_init_time = time.time()
                self.text = self.text[:-1]
            elif elem_.type == pygame.KEYUP and elem_.key == pygame.K_BACKSPACE:
                self.is_deleting = False
            elif elem_.type == pygame.KEYDOWN and (
                    elem_.__dict__["unicode"] == "\x03" or elem_.__dict__["unicode"] == "\x16"):
                if pygame.scrap.get(pygame.SCRAP_TEXT) is not None:
                    clipboard = pygame.scrap.get(pygame.SCRAP_TEXT).decode("utf-8")[:-1]
                    if len(self.text + clipboard) <= self.limit or self.limit == -1:
                        self.text += clipboard
            # if elem_.type == pygame.KEYDOWN:
            #     print(elem_)
            # self.text = " ".join(self.get_text().split(" ")[:-1])
        if self.is_deleting and self.del_init_time + 0.5 <= time.time() and self.del_last_time + 0.05 <= time.time():
            self.text = self.text[:-1]
            self.del_last_time = time.time()
