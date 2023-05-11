from __future__ import annotations

import random

import pygame
from pygame import Surface

from core.ui.impl.ingame_menu.backgrounds.elements.tree_elements.body import Body
from core.ui.impl.ingame_menu.backgrounds.elements.tree_elements.foot import Foot
from core.ui.impl.ingame_menu.backgrounds.elements.tree_elements.head import Head


class Tree:
    def __init__(self, loading: bool = False):
        self.multiplier: float

        self.is_dead: bool

        self.body: Body

        self.foot: Foot
        self.head: Head

        self.body_surface: Surface
        self.foot_surface: Surface
        self.head_surface: Surface
        self.surface: Surface
        if not loading:
            self.multiplier = random.randint(25, 45) / 10

            self.is_dead = random.randint(0, 100) > 70

            self.body = Body(self.is_dead, self.multiplier)

            self.foot = Foot(self.multiplier)
            self.head = Head(self.is_dead, self.multiplier)

            body_surface = self.body.get_surface()
            foot_surface = self.foot.get_surface()
            head_surface = self.head.get_surface()
            max_offset = max(self.body.max_offset, self.foot.offset, self.head.get_offset())
            height = self.head.get_surface().get_height() + self.foot.get_surface().get_height() + self.body.get_surface().get_height()
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
                    height - foot_surface.get_height() - self.body.get_height() - head_surface.get_height()
                )
            )
            self.surface.blit(
                body_surface,
                (
                    max_offset - self.body.max_offset,
                    height - foot_surface.get_height() - self.body.get_height()
                )
            )
            self.surface.blit(foot_surface, (max_offset - self.foot.offset, height - foot_surface.get_height()))

    def get_surface(self) -> Surface:
        return self.surface

    def resize(self, to_resize: Surface) -> Surface:
        ratio = self.multiplier
        return pygame.transform.scale(to_resize, (to_resize.get_width() * ratio, to_resize.get_height() * ratio))

    def to_json(self) -> dict:
        json_dict = {"head": self.head.to_json(), "body": self.body.to_json(), "foot": self.foot.to_json(),
                     "multiplier": self.multiplier, "is_dead": self.is_dead}
        return json_dict

    @staticmethod
    def from_json(json_dict: dict) -> Tree:
        print(
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(json_dict)
        tree: Tree = Tree(True)
        tree.is_dead = json_dict["is_dead"]
        tree.multiplier = json_dict["multiplier"]
        tree.head = Head.from_json(json_dict["head"], tree.is_dead, tree.multiplier)
        tree.body = Body.from_json(json_dict["body"], tree.is_dead, tree.multiplier)
        tree.foot = Foot.from_json(json_dict["foot"], tree.multiplier)
        body_surface = tree.body.get_surface()
        foot_surface = tree.foot.get_surface()
        head_surface = tree.head.get_surface()
        max_offset = max(tree.body.max_offset, tree.foot.offset, tree.head.get_offset())
        height = tree.head.get_surface().get_height() + tree.foot.get_surface().get_height() + tree.body.get_surface().get_height()
        tree.surface = Surface(
            (
                max(head_surface.get_width(), body_surface.get_width(), foot_surface.get_width()),
                height
            ),
            pygame.SRCALPHA
        )
        tree.surface.blit(head_surface, (max_offset - tree.head.get_offset(),
                                         height - foot_surface.get_height() - tree.body.get_height() - head_surface.get_height()))
        tree.surface.blit(body_surface, (
            max_offset - tree.body.max_offset, height - foot_surface.get_height() - tree.body.get_height()))
        tree.surface.blit(foot_surface, (max_offset - tree.foot.offset, height - foot_surface.get_height()))
        return tree
