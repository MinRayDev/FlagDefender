from __future__ import annotations

import random
from typing import Generator, Any

import pygame
from pygame import Surface

from core.ingame.backgrounds.elements.tree_elements.branch import Branch
from core.ingame.backgrounds.elements.tree_elements.tree_element import TreeElement
from core.ingame.backgrounds.elements.tree_elements.trunk import Trunk
from core.world import Facing


class Body(TreeElement):
    """Class 'Body'.

        :ivar is_dead: True if the tree is dead else False.
        :type is_dead: bool.

        :ivar components: List of trunks.
        :type components: list[Trunk].

        :ivar multiplier: Number with which the sizes will be multiplied to make the tree grow.
        :type multiplier: float.

        :ivar real_height: Height of the body without branches (not to be confused with surface size).
        :type real_height: int.

        :ivar size: Number of trunk (component).
        :type size: int.

        :ivar branch_prop: Proportion of branches on the body.
        :type branch_prop: int.

        :ivar max_offset: Biggest offset of all branches.
        :type max_offset: int.

        :ivar final_surface: Body's final surface (to draw).
        :type final_surface: Surface.

    """
    is_dead: bool
    components: list[Trunk]
    multiplier: float
    real_height: int
    size: int
    branch_prop: int
    max_offset: int
    final_surface: Surface

    def __init__(self, is_dead: bool, multiplier: float):
        """Constructor function for Trunk class.

            :param is_dead: True if the tree is dead else False.
            :type is_dead: bool.
            :param multiplier: Number with which the sizes will be multiplied to make the tree grow.
            :type multiplier: float.

        """
        super().__init__()
        self.is_dead = is_dead
        self.components = []
        self.multiplier = multiplier
        self.real_height = 0
        max_height: int = 27
        if self.is_dead:
            max_height = 13
        self.size = random.randint(7, max_height)
        self.branch_prop = 20
        if self.size > 20:
            self.branch_prop = 30
        branch_prop_check: bool = False
        ultimate_tree: int = random.randint(0, 1000)
        for i in range(self.size):
            if (random.randint(0, 40) > self.branch_prop or i < 2 or i >= self.size - 1 or (branch_prop_check and random.randint(0, 100) > 33)) and ultimate_tree != 0:
                self.components.append(Trunk([], self.is_dead, multiplier))
                branch_prop_check = False
            else:
                branch_prop_check = True
                random_int: int = random.randint(1, 18)
                if random_int in range(1, 7):
                    self.components.append(Trunk([Facing.EAST], self.is_dead, multiplier))
                elif random_int in range(7, 12):
                    self.components.append(Trunk([Facing.WEST], self.is_dead, multiplier))
                elif random_int in range(12, 18):
                    self.components.append(Trunk([Facing.WEST, Facing.EAST], self.is_dead, multiplier))
        self.max_offset = max(self.get_offsets())
        self.final_surface: Surface = self.generate_surface()

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
        self.real_height = 0
        width: int = max(self.get_widths())
        height: int = int(sum(self.get_heights())*1)
        surface: Surface = Surface((width, height), pygame.SRCALPHA)
        y = 0
        for i, component in enumerate(self.components):
            component_surface: Surface = component.get_surface()
            surface.blit(component_surface, (self.max_offset - component.get_offset(), y))
            y += component.get_height()
            self.real_height += component.get_height()
        return surface

    def get_widths(self) -> Generator[int, Any, None]:
        """Get all trunks' width.

           :return: All trunks' width.
           :rtype: Generator[int, Any, None].

       """
        for component in self.components:
            yield component.get_surface().get_width()

    def get_heights(self) -> Generator[int, Any, None]:
        """Get all trunks' height.

           :return: All trunks' height.
           :rtype: Generator[int, Any, None].

       """
        for component in self.components:
            yield component.get_surface().get_height()

    def get_offsets(self) -> Generator[int, Any, None]:
        """Get all trunks' offset.

           :return: All trunks' offset.
           :rtype: Generator[int, Any, None].

       """
        for component in self.components:
            yield component.get_offset()

    def to_json(self) -> list[dict[str, dict | list[Facing] | str]]:
        """Convert this object to json format.

            :return: Json dictionnary.
            :rtype: list[dict[str, dict | list[Facing] | str]].

        """
        json_list: list[dict[str, dict | list[Facing] | str]] = []
        for component in self.components:
            json_dict: dict[str, dict | list[Facing] | str] = {"branches": {}}
            if Facing.WEST in component.branches:
                json_dict["branches"][Facing.WEST] = component.branches[Facing.WEST].index
            if Facing.EAST in component.branches:
                json_dict["branches"][Facing.EAST] = component.branches[Facing.EAST].index
            json_dict["facings"] = component.facings
            json_dict["index"] = component.index
            json_list.append(json_dict)
        return json_list

    @staticmethod
    def from_json(json_dict: dict, is_dead: bool, multiplier: float) -> Body:
        """Load 'Body' object from json dict.

            :param json_dict: Json dictionnary.
            :type json_dict: dict.
            :param is_dead: True if the tree is dead else False.
            :type is_dead: bool.
            :param multiplier: Number with which the sizes will be multiplied to make the tree grow.
            :type multiplier: float.

            :return: Body Object.
            :rtype: Body.

        """
        body: Body = Body(is_dead, multiplier)
        body.components.clear()

        for comp in json_dict:
            facings: list[Facing] = comp["facings"]
            trunk: Trunk = Trunk(facings, is_dead, multiplier)
            trunk.index = comp["index"]
            trunk.branches = {}
            for facing_str in comp["branches"]:
                facing: int = int(facing_str)
                branch: Branch = Branch(Facing(facing), is_dead, multiplier)
                branch.index = comp["branches"][facing_str]
                branch.final_surface = branch.generate_surface()
                trunk.branches[Facing(facing)] = branch
            trunk.final_surface = trunk.generate_surface()
            body.components.append(trunk)
        body.max_offset = max(body.get_offsets())
        body.final_surface = body.generate_surface()
        return body
