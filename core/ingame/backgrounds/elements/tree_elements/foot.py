from __future__ import annotations

import random

import pygame
from pygame import Surface
from core.ingame.backgrounds.elements.tree_elements.tree_element import TreeElement
from core.world import Facing
from util.sprites import load


class Foot(TreeElement):
    def __init__(self, multiplier: float):
        super().__init__()
        self.multiplier = multiplier
        self.body_sprites: dict[str, Surface] = load(
            r"./resources/sprites/world/tree/body")
        self.foot_sprites: dict[str, Surface] = load(
            r"./resources/sprites/world/tree/foot")
        self.bottom_bodys: list[str] = [x for x in self.body_sprites if "bottom" in x]
        self.mid_index = str(random.choice(self.bottom_bodys))
        self.sides_indexes: dict[Facing, str] = {}
        self.offset = 0
        match self.mid_index.lstrip("bottom_"):
            case "1" | "2" | "3":
                # Right
                self.sides_indexes[Facing.EAST] = str(random.randint(1, 3))
            case "4" | "5" | "6":
                # Left
                self.sides_indexes[Facing.WEST] = str(random.randint(4, 6))
            case "7" | "8" | "9":
                # Both
                self.sides_indexes[Facing.EAST] = str(random.randint(1, 3))
                self.sides_indexes[Facing.WEST] = str(random.randint(4, 6))
        self.final_surface = self.generate_surface()

    def generate_surface(self) -> Surface:

        mid_surface: Surface = self.resize(self.body_sprites[self.mid_index], self.multiplier)
        width: int = mid_surface.get_width()
        roots_surfaces: list[Surface] = []
        if Facing.WEST in self.sides_indexes:
            foot_surface: Surface = self.resize(self.foot_sprites[self.sides_indexes[Facing.WEST]], self.multiplier)
            roots_surfaces.append(foot_surface)
            width += foot_surface.get_width()
            self.offset = foot_surface.get_width()
            print("Offset:", self.offset)
        if Facing.EAST in self.sides_indexes:
            foot_surface: Surface = self.resize(self.foot_sprites[self.sides_indexes[Facing.EAST]], self.multiplier)
            roots_surfaces.append(foot_surface)
            width += foot_surface.get_width()
        surface: Surface = Surface((width, mid_surface.get_height()), pygame.SRCALPHA)
        x: int = 0
        index: int = 0
        if Facing.WEST in self.sides_indexes:
            surface.blit(roots_surfaces[index],
                                    (x, surface.get_height() - roots_surfaces[index].get_height()))
            x += roots_surfaces[0].get_width()
            index += 1
        surface.blit(mid_surface, (x, 0))
        x += mid_surface.get_width()
        if Facing.EAST in self.sides_indexes:
            surface.blit(roots_surfaces[index], (x, surface.get_height() - roots_surfaces[index].get_height()))
        return surface

    def get_surface(self) -> Surface:
        return self.final_surface

    def to_json(self) -> dict:
        return {"roots": self.sides_indexes, "index": self.mid_index}

    @staticmethod
    def from_json(json_dict: dict, multiplier: float) -> Foot:
        foot: Foot = Foot(multiplier)
        foot.mid_index = json_dict["index"]
        foot.sides_indexes.clear()
        foot.offset = 0
        for root in json_dict["roots"]:
            foot.sides_indexes[Facing(int(root))] = json_dict["roots"][root]
        print("Side indexes", foot.sides_indexes)
        foot.final_surface = foot.generate_surface()
        return foot
