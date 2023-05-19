import time

import pygame

from ui.element.element import Element
from util.colors import Colors
from util.fonts import Fonts
from util.input.controls import Mouse, Inputs


class TextEntry(Element):
    """Class 'TextEntry' is a text entry.

        Extends: 'Element'
        :ivar placeholder: The placeholder of the text entry.
        :type placeholder: str.
        :ivar visual_text: The visual text of the text entry.
        :type visual_text: pygame.Surface.
        :ivar color: The color of the text entry.
        :type color: tuple[int, int, int].
        :ivar background_color: The background color of the text entry.
        :type background_color: tuple[int, int, int].
        :ivar selected_line_color: The selected line color of the text entry.
        :type selected_line_color: tuple[int, int, int].
        :ivar selected: If the text entry is selected.
        :type selected: bool.
        :ivar cursor_time_switch: The cursor time switch of the text entry.
        :type cursor_time_switch: float.
        :ivar text: The text of the text entry.
        :type text: str.
        :ivar is_deleting: If the text entry is deleting.
        :type is_deleting: bool.
        :ivar del_init_time: The delete init time of the text entry.
        :type del_init_time: float.
        :ivar del_last_time: The delete last time of the text entry.
        :type del_last_time: float.
        :ivar limit: The limit of the text entry.
        :type limit: int.
        :ivar unselect: If the text entry is unselected.
        :type unselect: bool.
        :ivar has_cursor: If the text entry has a cursor.
        :type has_cursor: bool.

    """
    placeholder: str
    visual_text: pygame.Surface
    color: tuple[int, int, int]
    background_color: tuple[int, int, int]
    selected_line_color: tuple[int, int, int]
    selected: bool
    cursor_time_switch: float
    text: str
    is_deleting: bool
    del_init_time: float
    del_last_time: float
    limit: int
    unselect: bool
    has_cursor: bool

    def __init__(self, placeholder: str, x: int | str, y: int | str, width: int, height: int, color: tuple[int, int, int], background_color: tuple[int, int, int] = Colors.white):
        """Constructor of the class 'TextEntry'.

            :param placeholder: The placeholder of the text entry.
            :type placeholder: str.
            :param x: The x position of the text entry.
            :type x: int | str.
            :param y: The y position of the text entry.
            :type y: int | str.
            :param width: The width of the text entry.
            :type width: int.
            :param height: The height of the text entry.
            :type height: int.
            :param color: The color of the text entry.
            :type color: tuple[int, int, int].

        """
        super().__init__(x, y, width, height, None)
        self.placeholder = placeholder
        self.visual_text = pygame.font.Font(Fonts.product_sans, self.height).render(placeholder, True, color)
        self.color = color
        self.background_color = background_color
        self.selected_line_color = Colors.red
        self.selected = False
        self.cursor_time_switch = time.time()
        self.text = ""
        self.is_deleting = False
        self.del_init_time = 0
        self.del_last_time = 0
        self.limit = -1
        self.unselect = True
        self.has_cursor = True

    def activity(self, inputs: Inputs) -> None:
        """Activity of the text entry.

            :param inputs: The inputs of the text entry.
            :type inputs: Inputs.

        """
        # Code to select the text entry or unselect it.
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
            # Entry of the text entry and change the text.
            self.entry(inputs)
            self.change(self.text)

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the text entry.

            :param surface: The surface of the text entry.
            :type surface: pygame.Surface.

        """
        # Draw the background of the text entry.
        if self.background_color is not None:
            pygame.draw.rect(surface, self.background_color, self.rectangle)
        temp_text = 0

        # Draw the text of the text entry.
        # Compute the text to draw (if the text is too long or not).
        if self.visual_text.get_rect().width > self.rectangle.width:
            for i, char in enumerate(self.text):
                if pygame.font.Font(Fonts.product_sans, self.height).render(self.text[:i] + char, True, self.color).get_rect().width >= self.rectangle.width:
                    temp_text += pygame.font.Font(Fonts.product_sans, self.height).render(char, True, self.color).get_rect().width
            self.visual_text = pygame.font.Font(Fonts.product_sans, self.height).render(self.text, True, self.color)
        # Use surface.blit() to draw the text to cut the text.
        surface.blit(self.visual_text, (self.rectangle.x, self.rectangle.y), (temp_text, 0, self.visual_text.get_rect().width, self.rectangle.height))
        # Cursor of the text entry.
        if self.selected and self.has_cursor:
            if self.cursor_time_switch+1 >= time.time():
                pygame.draw.rect(surface, self.selected_line_color, pygame.Rect(self.rectangle.x + self.visual_text.get_rect().width - temp_text, self.rectangle.y+2, 3, self.rectangle.height - 4))
            elif self.cursor_time_switch+2 <= time.time():
                self.cursor_time_switch = time.time()

    def change(self, text: str) -> None:
        """Changes the text of the text entry.

            :param text: The text of the text entry.
            :type text: str.

        """
        self.visual_text = pygame.font.Font(Fonts.product_sans, self.height).render(text, True, self.color)

    def hover(self) -> int | None:
        return pygame.SYSTEM_CURSOR_IBEAM if self.rectangle.collidepoint(pygame.mouse.get_pos()) else None

    def get_text(self) -> str:
        """Returns the text of the text entry."""
        return self.text

    def entry(self, inputs: Inputs) -> None:
        """Entry of the text entry.

            :param inputs: The inputs of the text entry.
            :type inputs: Inputs.

        """
        # For each input, if the input is a text input (or K_BACKSPACE) and the text entry is not full, add the text to the text entry.
        for elem_ in inputs.raw_inputs:
            if elem_.type == pygame.TEXTINPUT and (len(self.text) < self.limit or self.limit == -1):
                self.text += elem_.text
            elif elem_.type == pygame.KEYDOWN and elem_.key == pygame.K_BACKSPACE:
                self.is_deleting = True
                self.del_init_time = time.time()
                self.text = self.text[:-1]
            elif elem_.type == pygame.KEYUP and elem_.key == pygame.K_BACKSPACE:
                self.is_deleting = False
            elif elem_.type == pygame.KEYDOWN and (elem_.__dict__["unicode"] == "\x03" or elem_.__dict__["unicode"] == "\x16"):
                # Copy and paste.
                if pygame.scrap.get(pygame.SCRAP_TEXT) is not None:
                    clipboard = pygame.scrap.get(pygame.SCRAP_TEXT).decode("utf-8")[:-1]
                    if len(self.text + clipboard) <= self.limit or self.limit == -1:
                        self.text += clipboard
        if self.is_deleting and self.del_init_time + 0.5 <= time.time() and self.del_last_time + 0.05 <= time.time():
            self.text = self.text[:-1]
            self.del_last_time = time.time()
