import pygame

from util.input.controls import Inputs
from util.instance import get_client


class Element:
    """Class 'Element' is the base class for all elements.

        :ivar x: The x position of the element.
        :type x: int.
        :ivar y: The y position of the element.
        :type y: int.
        :ivar __width: The width of the element.
        :type __width: int.
        :ivar __height: The height of the element.
        :type __height: int.
        :ivar rectangle: The rectangle of the element.
        :type rectangle: pygame.Rect.
        :ivar is_hover: Whether the element is hovered or not.
        :type is_hover: bool.

    """
    x: int
    y: int
    __width: int
    __height: int
    rectangle: pygame.Rect
    is_hover: bool

    def __init__(self, x: int | str, y: int | str, width: int, height: int, rectangle: pygame.Rect = None):
        """Constructor of the class 'Element'.

            :param x: The x position of the element.
            :type x: int | str.
            :param y: The y position of the element.
            :type y: int | str.
            :param width: The width of the element.
            :type width: int.
            :param height: The height of the element.
            :type height: int.
            :param rectangle: The rectangle of the element.
            :type rectangle: pygame.Rect.

        """
        if isinstance(x, str):
            if x == "CENTER":
                self.x = get_client().get_screen().get_width() // 2 - width // 2
            else:
                raise ValueError(f"Invalid x position: {x}")
        else:
            self.x: int = x
        if isinstance(y, str):
            if y == "CENTER":
                self.y = get_client().get_screen().get_height() // 2 - height // 2
            else:
                raise ValueError(f"Invalid x position: {x}")
        else:
            self.y: int = y
        self.__width: int = width
        self.__height: int = height
        self.is_hover: bool = False
        if rectangle is not None:
            self.rectangle: pygame.Rect = rectangle
        else:
            self.rectangle: pygame.Rect = pygame.Rect(self.x, self.y, width, height)

    @property
    def width(self) -> int:
        """Getter for the width of the element."""
        return self.__width

    @property
    def height(self) -> int:
        """Getter for the height of the element."""
        return self.__height

    @width.setter
    def width(self, value: int):
        """Setter for the width of the element."""
        self.__width = value

    @height.setter
    def height(self, value: int):
        """Setter for the height of the element."""
        self.__height = value

    def activity(self, inputs: Inputs) -> None:
        """Method 'activity' is called every tick to update the element.

            :param inputs: The inputs of the game.
            :type inputs: Inputs.

        """
        # If mouse is hovering over the element (mouse is inside the rectangle of the element)
        if self.rectangle.collidepoint(pygame.mouse.get_pos()):
            self.is_hover = True
            # If the mouse is clicked (left click)
            if 1 in inputs.get_codes():
                # Do the click method
                self.click()
                # If the cursor is not an arrow, set it to an arrow
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            self.is_hover = False

    def draw(self, surface: pygame.Surface) -> None:
        """Method 'draw' is called every frame to draw the element.

            :param surface: The surface to draw the element on.
            :type surface: pygame.Surface.

        """
        pass

    def click(self) -> None:
        """Method 'click' is called when the element is clicked."""
        pass

    def hover(self) -> int | None:
        """Method 'hover' is called when the element is hovered.

            :return: The cursor to set.
            :rtype: int | None.

        """
        return pygame.SYSTEM_CURSOR_HAND if self.rectangle.collidepoint(pygame.mouse.get_pos()) else None
