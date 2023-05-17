from __future__ import annotations

import random

import pygame
from pygame import Surface
from core.ingame.backgrounds.elements.tree_elements.tree_element import TreeElement
from core.world import Facing
from util.sprites import load


class Foot(TreeElement):
    """Class 'Foot'.

        :ivar multiplier: Number with which the sizes will be multiplied to make the tree grow.
        :type multiplier: float.
        :ivar body_sprites: Dict of body sprites associated with their names.
        :type body_sprites: dict[str, Surface].
        :ivar foot_sprites: Dict of foot sprites associated with their names.
        :type foot_sprites: dict[str, Surface].
        :ivar bottom_bodys: Dict of foot sprites associated with their names.
        :type bottom_bodys: list[str].
        :ivar mid_index: Currant mid sprite's name.
        :type mid_index: str.
        :ivar sides_indexes: Currant sides sprite's name.
        :type sides_indexes: dict[Facing, str].

        :ivar offset: Currant offset.
        :type offset: int.

        :ivar final_surface: Head's final surface (to draw).
        :type final_surface: Surface.

    """
    multiplier: float
    body_sprites: dict[str, Surface]
    foot_sprites: dict[str, Surface]
    bottom_bodys: list[str]
    mid_index: str
    sides_indexes: dict[Facing, str]
    offset: int
    final_surface: Surface

    def __init__(self, multiplier: float):
        """Constructor function for Foot class.

            :param multiplier: Number with which the sizes will be multiplied to make the tree grow.
            :type multiplier: float.

        """
        super().__init__()
        self.multiplier = multiplier
        self.body_sprites = load(
            r"./resources/sprites/world/tree/body")
        self.foot_sprites = load(
            r"./resources/sprites/world/tree/foot")
        self.bottom_bodys = [x for x in self.body_sprites if "bottom" in x]
        self.mid_index = str(random.choice(self.bottom_bodys))
        self.sides_indexes = {}
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
        """Generate the surface to draw.

            :return: Surface to draw.
            :rtype: Surface.

        """
        mid_surface: Surface = self.resize(self.body_sprites[self.mid_index], self.multiplier)
        width: int = mid_surface.get_width()
        roots_surfaces: list[Surface] = []
        if Facing.WEST in self.sides_indexes:
            foot_surface: Surface = self.resize(self.foot_sprites[self.sides_indexes[Facing.WEST]], self.multiplier)
            roots_surfaces.append(foot_surface)
            width += foot_surface.get_width()
            self.offset = foot_surface.get_width()
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
        """Get 'final_surface'.

            :return: Surface to draw.
            :rtype: Surface.

        """
        return self.final_surface

    def to_json(self) -> dict[str, str | dict[Facing, str]]:
        """Convert this object to json format.

            :return: Json dictionnary.
            :rtype: dict[str, str].

        """
        return {"roots": self.sides_indexes, "index": self.mid_index}

    @staticmethod
    def from_json(json_dict: dict, multiplier: float) -> Foot:
        """Load 'Foot' object from json dict.

            :param json_dict: Json dictionnary.
            :type json_dict: dict.
            :param multiplier: Number with which the sizes will be multiplied to make the tree grow.
            :type multiplier: float.

            :return: Foot object.
            :rtype: Foot.

        """
        foot: Foot = Foot(multiplier)
        foot.mid_index = json_dict["index"]
        foot.sides_indexes.clear()
        foot.offset = 0
        for root in json_dict["roots"]:
            foot.sides_indexes[Facing(int(root))] = json_dict["roots"][root]
        foot.final_surface = foot.generate_surface()
        return foot
