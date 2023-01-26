from entities.Object import Object
from core.game import Game
from utils import sprites
from core.world import Facing, World
from typing import Optional


class Entity(Object):
    def __init__(self, x: int, y: int, sprites_path: str, world: World, facing: Optional[Facing] = None, health=float("inf")):
        self.world = world
        self.health = health
        self.facing = facing
        self.sprites_files = []
        self.sprites = sprites.load(sprites_path)
        self.sprite_selected = list(self.sprites.values())[0]
        super().__init__(x, y, world=world, width=list(self.sprites.values())[0].get_width(),
                         height=list(self.sprites.values())[0].get_height())

    def activity(self, **kwargs):
        if self.health <= 0:
            self.death()

    def death(self):
        del Game.instance.actual_world.entities[Game.instance.actual_world.entities.index(self)]

    def collisions(self):
        col = {Facing.NORTH: True, Facing.EAST: True, Facing.SOUTH: True, Facing.WEST: True}
        for entity in Game.instance.actual_world.entities:
            if self != entity:
                if entity.x <= self.x <= entity.x + entity.width and (
                        (entity.y <= self.y <= entity.y + entity.height) or (
                        entity.y <= self.y + self.height <= entity.y + entity.height)):
                    col[Facing.WEST] = False
                if entity.x <= self.x + self.width <= entity.x + entity.width and (
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

    def sprite_set(self, sprite):
        self.sprite_selected = sprite

    def draw(self, surface):
        surface.blit(self.sprite_selected, (self.x, self.y))

    def change_sprite(self):
        pass
