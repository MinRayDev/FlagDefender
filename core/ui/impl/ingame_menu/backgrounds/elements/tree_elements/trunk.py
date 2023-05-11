import random

import pygame
from pygame import Surface

from core.ui.impl.ingame_menu.backgrounds.elements.tree_elements.branch import Branch
from core.ui.impl.ingame_menu.backgrounds.elements.tree_elements.tree_element import TreeElement
from core.world import Facing
from util.sprites import load


class Trunk(TreeElement):
    def __init__(self, facings: list[Facing], is_dead: bool, multiplier: float):
        super().__init__()
        self.body_sprites: dict[str, Surface] = load(
            r"./resources/sprites/world/tree/body")
        self.simple_bodys: list[str] = [x for x in self.body_sprites if "branch" not in x and "bottom" not in x]
        self.branch_bodys: list[str] = [x for x in self.body_sprites if "branch" in x]
        self.branches: dict[Facing, Branch] = {}
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
        self.trunk_sprite: Surface = self.resize(self.body_sprites[self.index].copy(), self.multiplier)
        self.final_surface = self.generate_surface()

    def generate_surface(self) -> Surface:
        self.trunk_sprite: Surface = self.resize(self.body_sprites[self.index].copy(), self.multiplier)
        width: int = self.trunk_sprite.get_width()
        height: int = self.trunk_sprite.get_height()
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
        surface.blit(self.trunk_sprite, (x, height - self.trunk_sprite.get_height()))
        x += self.trunk_sprite.get_width()
        if Facing.EAST in self.branches:
            branch_surface: Surface = self.branches[Facing.EAST].get_surface()
            surface.blit(branch_surface, (x, height - branch_surface.get_height()))
        return surface

    def get_surface(self) -> Surface:
        return self.final_surface

    def get_height(self) -> int:
        return self.trunk_sprite.get_height()

    def get_offset(self) -> int:
        for facing in self.branches:
            if facing == Facing.WEST:
                return self.branches[facing].get_surface().get_width()
        else:
            return 0

    def get_vertical_offset(self) -> int:
        temp_branches_height: list[int] = [x.get_surface().get_height() for x in self.branches.values()]
        if len(temp_branches_height) != 0:
            return max(temp_branches_height)
        else:
            return 0
