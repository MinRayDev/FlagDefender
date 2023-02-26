from __future__ import annotations

import enum
import uuid
from typing import Optional
from core.world import Facing, World
from entities.Object import Object
from util import sprites
from util.instance import get_game
from util.instance import get_client


# TODO: passer les collisions sur les objets et en fonction d'une taille et pas du sprite (recalc au changement de sprite)
class Entity(Object):
    def __init__(self, x: int, y: int, sprites_path: str, world: World, facing: Optional[Facing] = None,
                 health=float("inf"), gravity=True):
        self.has_gravity = gravity
        self.world = world
        self.health = health
        self.max_health = self.health
        self.facing = facing
        self.sprites_files = []
        self.sprites = sprites.load(sprites_path)
        self.sprite_selected = list(self.sprites.values())[0]
        self.max_height = 0
        self.max_width = 0
        self.gravity_value = 3
        self.uuid: uuid.UUID = uuid.uuid4()
        self.source = 0
        self.type = EntityType.DEFAULT
        world.entities.append(self)
        for sprite in self.sprites:
            if self.max_height < self.sprites[sprite].get_height():
                self.max_height = self.sprites[sprite].get_height()
            if self.max_width < self.sprites[sprite].get_width():
                self.max_width = self.sprites[sprite].get_width()
        super().__init__(x, y, world=world, width=list(self.sprites.values())[0].get_width(),
                         height=list(self.sprites.values())[0].get_height())

    def activity(self, **kwargs):
        super().activity()
        if self.health <= 0:
            self.death()
        self.gravity()

    def death(self):
        if self in self.world.entities:
            del self.world.entities[self.world.entities.index(self)]

    def sprite_set(self, sprite):
        self.sprite_selected = sprite

    def draw(self, surface):
        surface.blit(self.sprite_selected, (
            self.x + get_client().get_screen().get_width() // 2 + get_game().scroll - get_game().main_player.entity.width // 2,
            self.y))

    def change_sprite(self):
        pass

    def is_flying(self):
        return self.y + self.height < get_client().get_screen().get_height() - self.world.floor

    def damage(self, amount: float, damage_type: DamageType):
        self.health -= amount
        if self.health <= 0:
            self.death()

    def gravity(self):
        if self.has_gravity:
            if self.is_flying():
                if self.y + self.height + self.gravity_value < get_client().get_screen().get_height() - self.world.floor:
                    self.y += self.gravity_value
                else:
                    # print(Game.instance.screen.get_height() - self.world.floor - self.y + self.height)
                    pass
                # prin
            # else:
            #     self.y +=get_game().screen.get_height() - self.world.floor and self.has_gravity - self.y + self.height

    @staticmethod
    def get_entity_by_uuid(entity_uuid: str | uuid.UUID) -> Entity:
        if isinstance(entity_uuid, str):
            entity_uuid = uuid.UUID(entity_uuid)
        for world in get_game().worlds:
            for entity_ in world.entities:
                if entity_.uuid == uuid:
                    return entity_


class DamageType(enum.IntEnum):
    WORLD = 0
    GAME = 1
    PROJECTILE = 2
    PHYSICAL = 3
    EXPLOSION = 4


class EntityType(enum.IntEnum):
    DEFAULT = 1  # pas visé
    ALLY = 2
    ENEMY = 3
