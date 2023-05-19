import pygame
from pygame import Surface

from ui.element.element import Element
from util.input.controls import Inputs
from util.instance import get_game


class ScrollPane(Element):
    """ScrollPane is a scroll pane.

        A scroll pane is a pane that can scroll and contains elements.

        Extends: 'Element'
        :ivar color: The color of the scroll pane.
        :type color: tuple[int, int, int].
        :ivar elems: The elements of the scroll pane.
        :type elems: list[Element].
        :ivar scroll: The scroll of the scroll pane.
        :type scroll: int.
        :ivar can_scroll_down: Whether the scroll pane can scroll down.
        :type can_scroll_down: bool.
        :ivar can_scroll_up: Whether the scroll pane can scroll up.
        :type can_scroll_up: bool.

    """
    color: tuple[int, int, int]
    elems: list[Element]
    scroll: int
    can_scroll_down: bool
    can_scroll_up: bool

    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]):
        """Constructor of the class 'ScrollPane'.

            :param x: The x position of the scroll pane.
            :type x: int.
            :param y: The y position of the scroll pane.
            :type y: int.
            :param width: The width of the scroll pane.
            :type width: int.
            :param height: The height of the scroll pane.
            :type height: int.
            :param color: The color of the scroll pane.
            :type color: tuple[int, int, int].

        """
        super().__init__(x, y, width, height, pygame.Rect(x, y, width, height))
        self.color = color
        self.elems = []
        self.scroll = 0
        self.can_scroll_down = False
        self.can_scroll_up = False

    def activity(self, inputs: Inputs) -> None:
        """Method 'activity' is called every tick.

            :param inputs: The inputs of the user.
            :type inputs: Inputs.

        """
        super().activity(inputs)
        # If the scroll pane is hovered, check if the scroll pane can scroll down or up and scroll if possible.
        if self.is_hover:
            self.scroll = 0
            self.can_scroll_down = False
            self.can_scroll_up = False
            for elem in self.elems:
                if elem.y + elem.height + 10 >= self.height + self.y:
                    self.can_scroll_down = True
                elif elem.y - 10 < self.y:
                    self.can_scroll_up = True
            # Check if the user scrolled and scroll if possible.
            for input_ in inputs.raw_inputs:
                if input_.type == pygame.MOUSEWHEEL:
                    if input_.y == -1 and self.can_scroll_down:
                        self.scroll += input_.y * 20
                    elif input_.y == 1 and self.can_scroll_up:
                        self.scroll += input_.y * 20
            # Do element activity and scroll the elements.
            for elem in self.elems:
                elem.y += self.scroll
                elem.rectangle = pygame.Rect(elem.x, elem.y, elem.width, elem.height)
                if elem.y <= self.height + self.y and elem.y + elem.height >= self.y:
                    elem.activity(inputs)

    def draw(self, surface: Surface) -> None:
        """Draws the scroll pane.

            Draws the scroll pane and its elements.

            :param surface: The surface to draw the scroll pane on.
            :type surface: Surface.

        """
        pygame.draw.rect(surface, self.color, self.rectangle)
        for elem in self.elems:
            if elem.y <= self.height + self.y and elem.y + elem.height >= self.y:
                elem.draw(surface)

    def hover(self) -> int | None:
        """Returns the cursor of the element that is hovered."""
        for elem in self.elems:
            if elem.y <= self.height + self.y and elem.y + elem.height >= self.y:
                if elem.hover() is not None and get_game().current_menu is not None:
                    if pygame.mouse.get_cursor() != elem.hover():
                        return elem.hover()
        return None
