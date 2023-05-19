from typing import Optional, TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import EventType

from util.input.controls import Inputs, Event
from util.instance import get_game

if TYPE_CHECKING:
    from ui.element.element import Element


class Menu:
    """Class 'Menu' is a base class for all menus.

        :ivar name: Name of the menu.
        :type name: str.
        :ivar inputs_queue: Queue of inputs.
        :type inputs_queue: Inputs.
        :ivar prev: Previous menu.
        :type prev: Optional[Menu].
        :ivar elems: List of elements.
        :type elems: list[Element].

    """
    name: str
    inputs_queue: Inputs
    prev: Optional['Menu']
    elems: list['Element']

    def __init__(self, name: str, prev: Optional['Menu'] = None):
        """Constructor of the class 'Menu'.

            :param name: Name of the menu.
            :type name: str.
            :param prev: Previous menu.
            :type prev: Optional[Menu].

        """
        self.name = name
        self.inputs_queue = Inputs()
        self.prev = prev
        self.elems = []

    def activity(self) -> None:
        """Object's activity function."""
        inputs: Inputs = self.get_queue(False)
        if pygame.K_ESCAPE in inputs.get_codes():
            if self.prev is not None:
                get_game().set_menu(self.prev)
            else:
                get_game().reset_menu()

    def draw(self, surface: Surface) -> None:
        """Object's draw function.

            :param surface: Surface to draw on.
            :type surface: Surface.

        """
        for elem in self.elems:
            elem.draw(surface)

    def add_queue(self, element: Event) -> None:
        """Add an input to the queue of inputs.

            :param element: The input to add.
            :type element: Event.

        """
        if element not in self.inputs_queue:
            self.inputs_queue.add(element)

    def add_raw_queue(self, element: EventType) -> None:
        """Add an input to the queue of raw inputs.

            :param element: The input to add.
            :type element: EventType.

        """
        if element not in self.inputs_queue.raw_inputs:
            self.inputs_queue.raw_add(element)

    def get_queue(self, reset: bool = True) -> Inputs:
        """Get the queue of inputs.

            :param reset: Reset the queue of inputs or not.
            :type reset: bool.

            :return: The queue of inputs.
            :rtype: Inputs.

        """
        temp = self.inputs_queue.copy()
        if reset:
            self.inputs_queue = Inputs()
        return temp
