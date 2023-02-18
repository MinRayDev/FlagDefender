from typing import Optional

from core.world import World, Facing
from core.game import Game

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
        self.collisions = True

    def get_collisions(self):
        col = {Facing.NORTH: True, Facing.EAST: True, Facing.SOUTH: True, Facing.WEST: True}
        if self.collisions:
            for entity in Game.instance.actual_world.entities:
                if self != entity and entity.collisions:
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
