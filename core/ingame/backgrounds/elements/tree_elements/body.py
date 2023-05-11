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
    def __init__(self, is_dead: bool, multiplier: float):
        super().__init__()
        self.is_dead = is_dead
        self.components: list[Trunk] = []
        self.multiplier = multiplier
        max_height = 27
        if self.is_dead:
            max_height = 13
        self.size = random.randint(7, max_height)
        self.branch_prop = 20
        if self.size > 20:
            self.branch_prop = 30
        for i in range(self.size):
            if random.randint(0, 70) > self.branch_prop or i <= 3:
                self.components.append(Trunk([], self.is_dead, multiplier))
            else:
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
        return self.final_surface

    def generate_surface(self) -> Surface:
        width: int = max(self.get_widths())
        height: int = sum(self.get_heights())
        surface: Surface = Surface((width, height), pygame.SRCALPHA)
        y = 0
        for component in self.components:
            component_surface: Surface = component.get_surface()
            surface.blit(component_surface, (self.max_offset - component.get_offset(), y - component.get_vertical_offset()))
            y += component.get_height() - component.get_vertical_offset()
        return surface

    def get_widths(self) -> Generator[int, Any, None]:
        for component in self.components:
            yield component.get_surface().get_width()

    def get_heights(self) -> Generator[int, Any, None]:
        for component in self.components:
            yield component.get_surface().get_height()

    def get_offsets(self) -> Generator[int, Any, None]:
        for component in self.components:
            yield component.get_offset()

    def get_height(self) -> int:
        height: int = 0
        for component in self.components:
            height += component.get_height() - component.get_vertical_offset()
        return height

    def to_json(self) -> list[dict[str, dict | list[Facing] | str]]:
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
        body: Body = Body(is_dead, multiplier)
        body.components.clear()
        for comp in json_dict:
            facings: list[Facing] = comp["facings"]
            trunk: Trunk = Trunk(facings, is_dead, multiplier)
            trunk.index = comp["index"]
            trunk.branches = {}
            for facing in comp["branches"]:
                facing: int = int(facing)
                branch: Branch = Branch(Facing(facing), is_dead, multiplier)
                branch.index = comp["branches"][str(facing)]
                branch.final_surface = branch.generate_surface()
                trunk.branches[Facing(facing)] = branch
            trunk.final_surface = trunk.get_surface()
            trunk.generate_surface()
            body.components.append(trunk)
        body.final_surface = body.generate_surface()
        return body
