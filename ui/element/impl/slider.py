import pygame
from pygame import Surface

from ui.element.element import Element
from util.input.controls import Inputs


class Slider(Element):
    """Class 'Slider' is a slider.

        Extends: 'Element'
        :ivar rectangle_line: The rectangle of the line of the slider.
        :type rectangle_line: pygame.Rect.
        :ivar color: The color of the slider.
        :type color: tuple[int, int, int].
        :ivar min: The minimum value of the slider.
        :type min: int.
        :ivar max: The maximum value of the slider.
        :type max: int.
        :ivar rectangle_selector: The rectangle of the selector of the slider.
        :type rectangle_selector: pygame.Rect.
        :ivar is_dragged: If the slider is dragged.
        :type is_dragged: bool.
        :ivar selector_color: The color of the selector of the slider.
        :type selector_color: tuple[int, int, int].

    """
    rectangle_line: pygame.Rect
    color: tuple[int, int, int]
    min: int
    max: int
    rectangle_selector: pygame.Rect
    is_dragged: bool
    selector_color: tuple[int, int, int]

    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int], min_number: int = 0, max_number: int = 100, value: int = 0, selector_color: tuple[int, int, int] = None):
        """Constructor of the class 'Slider'.

            :param x: The x position of the slider.
            :type x: int.
            :param y: The y position of the slider.
            :type y: int.
            :param width: The width of the slider.
            :type width: int.
            :param height: The height of the slider.
            :type height: int.
            :param color: The color of the slider.
            :type color: tuple[int, int, int].
            :param min_number: The minimum value of the slider.
            :type min_number: int.
            :param max_number: The maximum value of the slider.
            :type max_number: int.
            :param value: The value of the slider.
            :type value: int.
            :param selector_color: The color of the selector of the slider.
            :type selector_color: tuple[int, int, int].

        """
        self.rectangle_line = pygame.Rect(x, y, width, height)
        self.color = color
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

    def activity(self, _: Inputs) -> None:
        """The activity of the slider.

            :param _: The inputs of the game (_ because it's not used).
            :type _: Inputs.

        """
        # If the mouse is on the slider or if the slider is dragged.
        if self.rectangle_selector.collidepoint(pygame.mouse.get_pos()) or self.is_dragged:
            self.is_hover = True
            # If the mouse is pressed.
            if pygame.mouse.get_pressed()[0] == 1:
                self.is_dragged = True
                # Drag the slider.
                self.drag()
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            else:
                self.is_dragged = False
        else:
            self.is_hover = False

    def draw(self, surface: Surface) -> None:
        """Draw the slider.

            :param surface: The surface of the game.
            :type surface: Surface.

        """
        if self.is_hover:
            pygame.draw.rect(surface, (114, 137, 218), pygame.Rect(self.x-2, self.y-2, self.width+4, self.height+4))
        pygame.draw.rect(surface, self.color, self.rectangle_line)
        pygame.draw.circle(surface, self.selector_color, (self.rectangle_selector.x + self.rectangle_selector.width//2, self.rectangle_selector.y + self.rectangle_selector.height//2), self.rectangle_selector.height//1.5)

    def drag(self) -> None:
        """Drag the slider.

            Make the selector follow the mouse. And if the mouse is out of the line, the selector is at the end of the line.

        """
        if self.rectangle_line.x <= pygame.mouse.get_pos()[0] - self.rectangle_selector.width//2 and pygame.mouse.get_pos()[0] + self.rectangle_selector.width//2 <= self.rectangle_line.x+self.rectangle_line.width:
            self.rectangle_selector.x = pygame.mouse.get_pos()[0] - self.rectangle_selector.width//2
        elif pygame.mouse.get_pos()[0] - self.rectangle_selector.width//2 < self.rectangle_line.x:
            self.rectangle_selector.x = self.rectangle_line.x - self.rectangle_selector.width//2
        elif pygame.mouse.get_pos()[0] + self.rectangle_selector.width//2 > self.rectangle_line.x + self.rectangle_line.width:
            self.rectangle_selector.x = self.rectangle_line.x + self.rectangle_line.width - self.rectangle_selector.width // 2

    def get(self) -> float:
        """Get the value of the slider.

            :return: The value of the slider.
            :rtype: float.

        """
        abs_value: int = self.rectangle_selector.x+self.rectangle_selector.width//2 - self.rectangle_line.x
        return self.min + float((abs_value/self.rectangle_line.width)*self.max)

    def set_value(self, value: float) -> None:
        """Set the value of the slider.

            :param value: The value of the slider.
            :type value: float.

        """
        selector_pos: float = ((value - self.min)/self.max)*self.rectangle_line.width
        self.rectangle_selector.x = self.rectangle_line.x + selector_pos - self.rectangle_selector.width//2
