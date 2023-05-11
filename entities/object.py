from typing import Optional

from core.world import World, Facing
from util.instance import get_client


class Object:
    """Class 'Object', un objet.

    Dans ce jeu un objet est la base de tout. Un objet doit répondre à ces conditions (hors exceptions):
    - Immobile.
    - Ne pas disposer de vie.
    - Avoir des collisions.


    """

    def __init__(self, x: int, y: int, world: Optional[World], width: int, height: int):
        self.x = x
        self.y = y
        self.world = world
        self.width = width
        self.height = height
        self.has_collisions = True

    def get_collisions(self):
        col = {Facing.NORTH: True, Facing.EAST: True, Facing.SOUTH: True, Facing.WEST: True}
        if self.has_collisions:
            for entity in self.world.entities:
                if self != entity and entity.has_collisions:
                    if entity.x < self.x <= entity.x + entity.width and (
                            (entity.y <= self.y <= entity.y + entity.height) or (
                            entity.y <= self.y + self.height <= entity.y + entity.height)):
                        col[Facing.WEST] = False
                    if entity.x <= self.x + self.width < entity.x + entity.width and (
                            (entity.y <= self.y <= entity.y + entity.height) or (
                            entity.y <= self.y + self.height <= entity.y + entity.height)):
                        col[Facing.EAST] = False
                    if entity.y <= self.y <= entity.y + entity.height and (
                            (entity.x <= self.x <= entity.x + entity.width) or (
                            entity.x <= self.x + self.width <= entity.x + entity.width)):
                        col[Facing.NORTH] = False
                    if entity.y <= self.y + self.height <= entity.y + entity.height and (
                            (entity.x <= self.x <= entity.x + entity.width) or (
                            entity.x <= self.x + self.width <= entity.x + entity.width)):
                        col[Facing.SOUTH] = False
        return col

    def activity(self):
        pass

    def contact(self, entity):
        return ((entity.x <= self.x <= entity.x + entity.width) or (
                entity.x <= self.x + self.width <= entity.x + entity.width)) and (
                (entity.y <= self.y <= entity.y + entity.height) or (
                entity.y <= self.y + self.height <= entity.y + entity.height))

    def to_floor(self):
        self.y = get_client().get_screen().get_height() - self.world.floor - self.height
