import random

from pygame import Surface

from core.ingame.backgrounds.elements.tree_elements.tree_element import TreeElement
from core.world import Facing
from util.sprites import load


class Branch(TreeElement):
    """Class 'Branch'.

        :ivar is_dead: True if the tree is dead else False.
        :type is_dead: bool.
        :ivar multiplier: Number with which the sizes will be multiplied to make the tree grow.
        :type multiplier: float.
        :ivar sprites: Dict of sprites associated with their names.
        :type sprites: dict[str, Surface].
        :ivar index: Currant sprite's name.
        :type index: str.

        :ivar final_surface: Branch's final surface (to draw).
        :type final_surface: Surface.

    """
    facing: Facing
    is_dead: bool
    sprites: dict[str, Surface]
    index: str
    multiplier: float
    final_surface: Surface

    def __init__(self, facing: Facing, is_dead: bool, multiplier: float):
        """Constructor function for Branch class.

            :param facing: West if the branch is left else East if the branch is right.
            :type facing: Facing.
            :param is_dead: True if the tree is dead else False.
            :type is_dead: bool.
            :param multiplier: Number with which the sizes will be multiplied to make the tree grow.
            :type multiplier: float.

        """
        super().__init__()
        self.facing = facing
        self.is_dead = is_dead
        self.sprites = load(r"./resources/sprites/world/tree/branch")
        self.index = ""
        self.multiplier = multiplier
        if facing == Facing.EAST:
            # Right
            self.index = str(random.randint(4, 6))
            if self.is_dead:
                self.index = "dead_" + self.index
        elif facing == Facing.WEST:
            # Left
            self.index = str(random.randint(1, 3))
            if self.is_dead:
                self.index = "dead_" + self.index
        else:
            raise ValueError("Invalid direction")
        self.final_surface = self.generate_surface()

    def get_surface(self) -> Surface:
        """Get 'final_surface'.

            :return: Surface to draw.
            :rtype: Surface.

        """
        return self.final_surface

    def generate_surface(self) -> Surface:
        """Generate the surface to draw.

            :return: Surface to draw.
            :rtype: Surface.

        """
        return self.resize(self.sprites[self.index], self.multiplier)
