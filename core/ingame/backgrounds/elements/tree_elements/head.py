from __future__ import annotations

import random

from pygame import Surface

from core.ingame.backgrounds.elements.tree_elements.tree_element import TreeElement
from util.sprites import load


class Head(TreeElement):
    """Class 'Head'.

        :ivar is_dead: True if the tree is dead else False.
        :type is_dead: bool.
        :ivar multiplier: Number with which the sizes will be multiplied to make the tree grow.
        :type multiplier: float.
        :ivar sprites: Dict of sprites associated with their names.
        :type sprites: dict[str, Surface].
        :ivar index: Currant sprite's name.
        :type index: str.

        :ivar final_surface: Head's final surface (to draw).
        :type final_surface: Surface.

    """
    is_dead: bool
    multiplier: float
    sprites: dict[str, Surface]
    index: str
    final_surface: Surface

    def __init__(self, is_dead: bool, multiplier: float):
        """Constructor function for Head class.

            :param is_dead: True if the tree is dead else False.
            :type is_dead: bool.
            :param multiplier: Number with which the sizes will be multiplied to make the tree grow.
            :type multiplier: float.

        """
        super().__init__()
        self.is_dead = is_dead
        self.multiplier = multiplier
        self.sprites = load(r"./resources/sprites/world/tree/head")
        self.index = str(random.randint(1, 3))
        if self.is_dead:
            self.index = "dead_" + self.index
        self.final_surface = self.generate_surface()

    def get_surface(self) -> Surface:
        """Get 'final_surface'.

            :return: Surface to draw.
            :rtype: Surface.

        """
        return self.final_surface

    def get_offset(self) -> int:
        """Get current sprite's offset.

            :return: The offset.
            :rtype: float.

        """
        match self.index:
            case "1":
                return int(16 * self.multiplier)
            case "2":
                return int(13 * self.multiplier)
            case "3":
                return int(15 * self.multiplier)
            case _:
                return 0

    def to_json(self) -> dict[str, str]:
        """Convert this object to json format.

            :return: Json dictionnary.
            :rtype: dict[str, str].

        """
        return {"index": self.index}

    def generate_surface(self) -> Surface:
        """Generate the surface to draw.

            :return: Surface to draw.
            :rtype: Surface.

        """
        return self.resize(self.sprites[self.index], self.multiplier)

    @staticmethod
    def from_json(json_dict: dict, is_dead: bool, multiplier: float) -> Head:
        """Load 'Head' object from json dict.

            :param json_dict: Json dictionnary.
            :type json_dict: dict.
            :param is_dead: True if the tree is dead else False.
            :type is_dead: bool.
            :param multiplier: Number with which the sizes will be multiplied to make the tree grow.
            :type multiplier: float.

            :return: The head.
            :rtype: Head.

        """
        head: Head = Head(is_dead, multiplier)
        head.index = json_dict["index"]
        head.final_surface = head.generate_surface()
        return head
