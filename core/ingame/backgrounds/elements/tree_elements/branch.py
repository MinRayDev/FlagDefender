import random

from pygame import Surface

from core.ingame.backgrounds.elements.tree_elements.tree_element import TreeElement
from core.world import Facing
from util.sprites import load


class Branch(TreeElement):
    def __init__(self, facing: Facing, is_dead: bool, multiplier: float):
        super().__init__()
        self.facing = facing
        self.is_dead = is_dead
        self.sprites: dict[str, Surface] = load(r"./resources/sprites/world/tree/branch")
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
        return self.final_surface

    def generate_surface(self) -> Surface:
        return self.resize(self.sprites[self.index], self.multiplier)