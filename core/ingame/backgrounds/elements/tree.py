from __future__ import annotations

import random
from typing import Optional

import pygame
from pygame import Surface

from core.ingame.backgrounds.elements.tree_elements.body import Body
from core.ingame.backgrounds.elements.tree_elements.foot import Foot
from core.ingame.backgrounds.elements.tree_elements.head import Head
from core.world import Facing


class Tree:
    """Class 'Tree'.

        :ivar multiplier: Number with which the sizes will be multiplied to make the tree grow.
        :type multiplier:  Optional[float].

        :ivar is_dead: True if the tree is dead else False.
        :type is_dead: Optional[bool].

        :ivar body: Tree's body part.
        :type body: Optional[Body].

        :ivar foot: Tree's foot part.
        :type foot: Optional[Foot].

        :ivar head: Tree's head part.
        :type head: Optional[Head].

        :ivar surface: Tree's final surface (to draw).
        :type surface: Surface.

    """
    multiplier: Optional[float]
    is_dead: Optional[bool]
    body: Optional[Body]
    foot: Optional[Foot]
    head: Optional[Head]
    surface: Optional[Surface]

    def __init__(self, loading: bool = False):
        """Constructor function for Tree class.

            :param loading: If the level is loaded or not.
            :type loading: bool.

        """
        self.multiplier = None
        self.is_dead = None

        self.body = None
        self.foot = None
        self.head = None

        self.surface = None

        if not loading:
            self.multiplier = random.randint(25, 45) / 10

            self.is_dead = random.randint(0, 100) > 70

            self.body = Body(self.is_dead, self.multiplier)

            self.foot = Foot(self.multiplier)
            self.head = Head(self.is_dead, self.multiplier)

            body_surface: Surface = self.body.get_surface()
            foot_surface: Surface = self.foot.get_surface()
            head_surface: Surface = self.head.get_surface()
            max_offset: int = max(self.body.max_offset, self.foot.offset, self.head.get_offset())
            height: int = self.head.get_surface().get_height() + self.foot.get_surface().get_height() + self.body.real_height
            self.surface = Surface(
                (
                    max(head_surface.get_width(), body_surface.get_width(), foot_surface.get_width()),
                    height
                ),
                pygame.SRCALPHA
            )
            self.surface.blit(
                head_surface,
                (
                    max_offset - self.head.get_offset(),
                    0
                )
            )
            self.surface.blit(
                body_surface,
                (
                    max_offset - self.body.max_offset,
                    self.head.get_surface().get_height()
                )
            )
            self.surface.blit(foot_surface, (max_offset - self.foot.offset, self.head.get_surface().get_height() + self.body.real_height))

    def get_surface(self) -> Surface:
        """Get surface.

            :return: Surface to draw.
            :rtype: Surface.

        """
        return self.surface

    def to_json(self) -> dict[str, dict[str, str] | list[dict[str, dict | list[Facing] | str]] | bool | None | dict[str, str | dict[Facing, str]] | float]:
        """Convert this object to json format.

            :return: Json dictionnary.
            :rtype: dict[str, dict[str, str] | list[dict[str, dict | list[Facing] | str]] | bool | None | dict[str, str | dict[Facing, str]] | float].

        """
        json_dict = {"head": self.head.to_json(), "body": self.body.to_json(), "foot": self.foot.to_json(),
                     "multiplier": self.multiplier, "is_dead": self.is_dead}
        return json_dict

    @staticmethod
    def from_json(json_dict: dict) -> Tree:
        """Load 'Tree' object from json dict.

            :param json_dict: Json dictionnary.
            :type json_dict: dict.

            :return: Tree Object.
            :rtype: Tree.

        """
        tree: Tree = Tree(True)
        tree.is_dead = json_dict["is_dead"]
        tree.multiplier = json_dict["multiplier"]
        tree.head = Head.from_json(json_dict["head"], tree.is_dead, tree.multiplier)
        tree.body = Body.from_json(json_dict["body"], tree.is_dead, tree.multiplier)
        tree.foot = Foot.from_json(json_dict["foot"], tree.multiplier)
        body_surface: Surface = tree.body.get_surface()
        foot_surface: Surface = tree.foot.get_surface()
        head_surface: Surface = tree.head.get_surface()
        max_offset: int = max(tree.body.max_offset, tree.foot.offset, tree.head.get_offset())
        height: int = tree.head.get_surface().get_height() + tree.foot.get_surface().get_height() + tree.body.real_height
        tree.surface = Surface(
            (
                max(head_surface.get_width(), body_surface.get_width(), foot_surface.get_width()),
                height
            ),
            pygame.SRCALPHA
        )
        tree.surface.blit(head_surface, (max_offset - tree.head.get_offset(), 0))
        tree.surface.blit(body_surface, (max_offset - tree.body.max_offset, tree.head.get_surface().get_height()))
        tree.surface.blit(foot_surface, (max_offset - tree.foot.offset, tree.head.get_surface().get_height() + tree.body.real_height))
        return tree
