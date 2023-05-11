from __future__ import annotations

import random

from pygame import Surface

from core.ui.impl.ingame_menu.backgrounds.elements.tree_elements.tree_element import TreeElement
from util.sprites import load


class Head(TreeElement):
    def __init__(self, is_dead: bool, multiplier: float):
        super().__init__()
        self.is_dead = is_dead
        self.multiplier = multiplier
        self.sprites: dict[str, Surface] = load(r"./resources/sprites/world/tree/head")
        self.index = str(random.randint(1, 3))
        if self.is_dead:
            self.index = "dead_" + self.index
        self.final_surface = self.generate_surface()

    def get_surface(self) -> Surface:
        return self.final_surface

    def get_offset(self) -> float:
        match self.index:
            case "1":
                return 16 * self.multiplier
            case "2":
                return 13 * self.multiplier
            case "3":
                return 15 * self.multiplier
            case _:
                return 0

    def to_json(self) -> dict:
        return {"index": self.index}

    def generate_surface(self) -> Surface:
        return self.resize(self.sprites[self.index], self.multiplier)

    @staticmethod
    def from_json(json_dict: dict, is_dead: bool, multiplier: float) -> Head:
        head: Head = Head(is_dead, multiplier)
        head.index = json_dict["index"]
        head.final_surface = head.generate_surface()
        return head
