import time

import pygame

from core.menus.elements.element import Element
from entities.Object import Object
from utils.fonts import Fonts
from utils.inputs.controls import Sources


class TextEntry(Element):
    def __init__(self, placeholder, x, y, width, height, color):

        self.placeholder = placeholder
        self.visual_text = pygame.font.Font(Fonts.chickenic, 30).render(placeholder, True, color)

        super().__init__(x, y, 100, 20, pygame.Rect(x, y, width,  self.visual_text.get_rect().height))
        self.rectangle.x = x
        self.rectangle.y = y
        self.color = color
        self.background_color = (255, 255, 255)
        self.selected_line_color = (255, 0, 0)
        self.selected = False
        self.t = time.time()
        self.text = ""
        self.a = False
        self.init_t = 0
        self.last_t = 0

    def activity(self, inputs):
        if self.rectangle.collidepoint(pygame.mouse.get_pos()):
            self.is_hover = True
            if 1 in inputs.get_codes():
                self.click()
                self.selected = True
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            self.is_hover = False
            if 1 in inputs.get_codes():
                self.selected = False
        if self.selected:
            for elem_ in inputs.raw_inputs:
                if elem_.type == pygame.TEXTINPUT:
                    self.text += elem_.text
                elif elem_.type == pygame.KEYDOWN and elem_.key == pygame.K_BACKSPACE:
                    self.a = True
                    self.init_t = time.time()
                    self.text = self.text[:-1]
                elif elem_.type == pygame.KEYUP and elem_.key == pygame.K_BACKSPACE:
                    self.a = False
                elif elem_.type == pygame.KEYDOWN and (elem_.__dict__["unicode"] == "\x03" or elem_.__dict__["unicode"] == "\x16"):
                    if pygame.scrap.get(pygame.SCRAP_TEXT) is not None:
                        self.text += pygame.scrap.get(pygame.SCRAP_TEXT).decode("utf-8")[:-1]

            if self.a and self.init_t + 0.5 <= time.time() and self.last_t + 0.05 <= time.time():
                self.text = self.text[:-1]
                self.last_t = time.time()
            self.change(self.text)

    def draw(self, surface):
        pygame.draw.rect(surface, self.background_color, self.rectangle)

        if self.visual_text.get_rect().width > self.rectangle.width:
            temp_text = 0
            for i, char in enumerate(self.text):
                if pygame.font.Font(Fonts.chickenic, 30).render(self.text[:i] + char, True, self.color).get_rect().width >= self.rectangle.width:
                    temp_text += 1
                    # if pygame.font.Font(Fonts.chickenic, 30).render(self.text[temp_text:i] + char, True, self.color).get_rect().width >= self.rectangle.width:
                    #     temp_text += 1
            self.visual_text = pygame.font.Font(Fonts.chickenic, 30).render(self.text[temp_text:], True, self.color)
        surface.blit(self.visual_text, self.rectangle)
        if self.selected:
            if self.t+1 >= time.time():
                pygame.draw.rect(surface, self.selected_line_color, pygame.Rect(self.rectangle.x + 2 + self.visual_text.get_rect().width, self.rectangle.y+2, 3, self.rectangle.height - 4))
            elif self.t+2 <= time.time():
                self.t = time.time()

    def click(self):
        pass

    def change(self, text: str):
        self.visual_text = pygame.font.Font(Fonts.chickenic, 30).render(text, True, self.color)

    def hover(self) -> int | None:
        return pygame.SYSTEM_CURSOR_IBEAM if self.rectangle.collidepoint(pygame.mouse.get_pos()) else None
