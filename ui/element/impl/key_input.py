import time

import pygame
from pygame import Surface

from ui.element.element import Element
from util.colors import Colors
from util.fonts import Fonts
from util.input.controls import Controls, Mouse, Inputs


class KeyInput(Element):
    """Class 'KeyInput' is a key input.

        A key input is an element that allows the user to input keybinds to edit the controls.

        Extends: 'Element'
        :ivar value: The value of the key input.
        :type value: str.
        :ivar visual_text: The visual text of the key input.
        :type visual_text: pygame.Surface.
        :ivar color: The color of the key input.
        :type color: tuple[int, int, int].
        :ivar background_color: The background color of the key input.
        :type background_color: tuple[int, int, int].
        :ivar selected_line_color: The selected line color of the key input.
        :type selected_line_color: tuple[int, int, int].
        :ivar selected: If the key input is selected.
        :type selected: bool.
        :ivar cursor_time_switch: The cursor time switch of the key input.
        :type cursor_time_switch: float.
        :ivar is_deleting: If the key input is deleting.
        :type is_deleting: bool.
        :ivar del_init_time: The delete init time of the key input.
        :type del_init_time: float.
        :ivar del_last_time: The delete last time of the key input.
        :type del_last_time: float.
        :ivar limit: The limit of the key input.
        :type limit: int.
        :ivar unselect: If the key input is unselected.
        :type unselect: bool.
        :ivar has_cursor: If the key input has a cursor.
        :type has_cursor: bool.

    """
    value: str
    visual_text: pygame.Surface
    color: tuple[int, int, int]
    background_color: tuple[int, int, int]
    selected_line_color: tuple[int, int, int]
    selected: bool
    cursor_time_switch: float
    is_deleting: bool
    del_init_time: float
    del_last_time: float
    limit: int
    unselect: bool
    has_cursor: bool

    def __init__(self, base_value: str, x: int | str, y: int | str, width: int, height: int, color: tuple[int, int, int], code: int, background_color: tuple[int, int, int] = Colors.white):
        """Constructor of the class 'KeyInput'.

            :param base_value: The base value of the key input.
            :type base_value: str.
            :param x: The x position of the key input.
            :type x: int | str.
            :param y: The y position of the key input.
            :type y: int | str.
            :param width: The width of the key input.
            :type width: int.
            :param height: The height of the key input.
            :type height: int.
            :param color: The color of the key input.
            :type color: tuple[int, int, int].
            :param background_color: The background color of the key input.
            :type background_color: tuple[int, int, int].
            :param code: The code of the key input.
            :type code: str.

        """
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

    def activity(self, inputs: Inputs) -> None:
        """Activity of the key input.

            :param inputs: The inputs of the key input.
            :type inputs: Inputs.

        """
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
                text_border_1: Surface = pygame.font.Font(Fonts.product_sans, self.height).render(">", True, self.color)
                text_border_2: Surface = pygame.font.Font(Fonts.product_sans, self.height).render("<", True, self.color)
                surface.blit(text_border_1, (self.rectangle.x + 3, self.rectangle.y), text_border_1.get_rect())
                surface.blit(text_border_2, (self.rectangle.x + self.rectangle.width - 3 - text_border_2.get_rect().width, self.rectangle.y), text_border_2.get_rect())
            elif self.cursor_time_switch+2 <= time.time():
                self.cursor_time_switch = time.time()

    def change(self, text: str) -> None:
        """Change the text of the key input."""
        self.visual_text = pygame.font.Font(Fonts.product_sans, self.height).render(text, True, self.color)

    def hover(self) -> int | None:
        """Return the cursor type of the key input."""
        return pygame.SYSTEM_CURSOR_IBEAM if self.rectangle.collidepoint(pygame.mouse.get_pos()) else None

    def get_text(self) -> str:
        """Return the text of the key input."""
        return self.value

    def entry(self, inputs: Inputs) -> None:
        """Entry of the key input.

            :param inputs: The inputs of the key input.
            :type inputs: Inputs.

        """
        can_unselect: bool = False
        # Change the value of the key input.
        for input_ in inputs.raw_inputs:
            if input_.type == pygame.KEYDOWN:
                self.value = pygame.key.name(input_.key)
                if Controls.code_exists(self.code) and input_.key != Controls.from_code(self.code).get_key():
                    Controls.change_key(input_.key, self.code)
                    can_unselect = True
        if can_unselect:
            self.selected = False
