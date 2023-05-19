import random

import pygame
from pygame import Surface

from core.ingame.backgrounds.elements.tree_elements.branch import Branch
from core.ingame.backgrounds.elements.tree_elements.tree_element import TreeElement
from core.world import Facing
from util.sprites import load


class Trunk(TreeElement):
    """Class 'Trunk'.

        :ivar body_sprites: Dict of body sprites associated with their names.
        :type body_sprites: dict[str, Surface].

        :ivar branches: Dict of facing associated with their branches.
        :type branches: dict[Facing, Branch].

        :ivar facings: List of facings.
        :type facings: list[Facing].

        :ivar multiplier: Number with which the sizes will be multiplied to make the tree grow.
        :type multiplier: float.

        :ivar index: Currant sprite's name.
        :type index: str.

        :ivar final_surface: Trunk's final surface (to draw).
        :type final_surface: Surface.

    """
    body_sprites: dict[str, Surface]
    branches: dict[Facing, Branch]
    facings: list[Facing]
    multiplier: float
    index: str
    final_surface: Surface

    def __init__(self, facings: list[Facing], is_dead: bool, multiplier: float):
        """Constructor function for Trunk class.

            :param facings: List of facings.
            :type facings: list[Facing].
            :param is_dead: True if the tree is dead else False.
            :type is_dead: bool.
            :param multiplier: Number with which the sizes will be multiplied to make the tree grow.
            :type multiplier: float.

        """
        super().__init__()
        self.body_sprites = load(r"./resources/sprites/world/tree/body")
        self.branches = {}
        self.facings = facings
        self.multiplier = multiplier
        if len(facings) == 0:
            self.index = str(random.randint(1, 3))
        elif Facing.EAST in facings and Facing.WEST in facings:
            # Both
            self.index = "branch_" + str(random.randint(13, 18))
            self.branches[Facing.WEST] = Branch(Facing.WEST, is_dead, multiplier)
            self.branches[Facing.EAST] = Branch(Facing.EAST, is_dead, multiplier)
        elif Facing.EAST in facings:
            # Right
            self.index = "branch_" + str(random.randint(1, 6))
            self.branches[Facing.EAST] = Branch(Facing.EAST, is_dead, multiplier)
        elif Facing.WEST in facings:
            # Left
            self.index = "branch_" + str(random.randint(7, 12))
            self.branches[Facing.WEST] = Branch(Facing.WEST, is_dead, multiplier)
        self.final_surface = self.generate_surface()

    def generate_surface(self) -> Surface:
        """Generate the surface to draw.

           :return: Surface to draw.
           :rtype: Surface.

       """
        trunk_sprite: Surface = self.resize(self.body_sprites[self.index].copy(), self.multiplier)
        width: int = trunk_sprite.get_width()
        height: int = trunk_sprite.get_height()
        for facing in self.branches:
            branch_surface: Surface = self.branches[facing].get_surface()
            width += branch_surface.get_width()
            if height < branch_surface.get_height():
                height = branch_surface.get_height()
        surface: Surface = Surface((width + 20 * self.multiplier, height), pygame.SRCALPHA)
        x = 0
        if Facing.WEST in self.branches:
            branch_surface: Surface = self.branches[Facing.WEST].get_surface()
            surface.blit(branch_surface, (x, height - branch_surface.get_height()))
            x += branch_surface.get_width()
        surface.blit(trunk_sprite, (x, 0))
        x += trunk_sprite.get_width()
        if Facing.EAST in self.branches:
            branch_surface: Surface = self.branches[Facing.EAST].get_surface()
            surface.blit(branch_surface, (x, 0))
        return surface

    def get_surface(self) -> Surface:
        """Get 'final_surface'.

            :return: Surface to draw.
            :rtype: Surface.

        """
        return self.final_surface

    def get_height(self) -> int:
        """Get trunk body sprite's height.

            :return: The height.
            :rtype: int.

        """
        return self.resize(self.body_sprites[self.index].copy(), self.multiplier).get_height()

    def get_offset(self) -> int:
        """Get current sprite's offset.

            :return: The offset.
            :rtype: float.

        """
        for facing in self.branches:
            if facing == Facing.WEST:
                return self.branches[facing].get_surface().get_width()
        return 0
