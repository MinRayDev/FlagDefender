from __future__ import annotations

import enum
import uuid
from typing import Optional

import pygame
from pygame import Surface

from core.world import Facing, World
from entities.object import Object
from util import sprites
from util.colors import Colors
from util.draw_util import draw_with_scroll
from util.instance import get_client
from util.instance import get_game


class Entity(Object):
    sprite_selected: Surface

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

    def activity(self):
        super().activity()
        if self.health <= 0:
            self.death()
        self.gravity()

    def death(self):
        if self in self.world.entities:
            del self.world.entities[self.world.entities.index(self)]

    def sprite_set(self, sprite):
        self.sprite_selected = sprite

    def draw(self, surface: Surface) -> None:
        draw_with_scroll(surface, self.sprite_selected, self.x, self.y)

    def is_flying(self) -> bool:
        return self.y + self.height < get_client().get_screen().get_height() - self.world.floor

    def get_floor_dist(self) -> int:
        return get_client().get_screen().get_height() - self.world.floor - self.y - self.height

    def damage(self, amount: float, damage_type: DamageType, author: Entity = None) -> None:
        from entities.livingentities.entity_player import PlayerEntity
        from core.player import Player
        if (
                damage_type == DamageType.PROJECTILE or damage_type == DamageType.PHYSICAL or damage_type == DamageType.EXPLOSION) and author is None:
            raise ValueError("Author must be specified")
        self.health -= amount
        if self.health <= 0:
            self.death()
            if isinstance(author, PlayerEntity):
                Player.get_by_entity(author).kills += 1

    def gravity(self) -> None:
        if self.has_gravity:
            if self.is_flying():
                if self.y + self.height + self.gravity_value < get_client().get_screen().get_height() - self.world.floor:
                    self.y += self.gravity_value
                else:
                    self.to_floor()

    @staticmethod
    def get_entity_by_uuid(entity_uuid: str | uuid.UUID) -> Entity:
        if isinstance(entity_uuid, str):
            entity_uuid = uuid.UUID(entity_uuid)
        for world in get_game().current_level.worlds:
            for entity_ in world.entities:
                if entity_.uuid == entity_uuid:
                    return entity_

    def to_json(self) -> dict[str, int | float | Facing | None | str]:
        return {"entity_type": str(self.__class__).split("'")[1], "x": self.x, "y": self.y, "health": self.health,
                "facing": self.facing, "uuid": str(self.uuid)}

    def draw_health_bar(self, surface: Surface, offset: int = 0) -> None:
        x: int = self.x - 4 + surface.get_width() // 2 + get_game().current_level.scroll - get_game().current_level.main_player.entity.width // 2 + offset
        y: int = self.y - 14
        width: int = self.width + 8
        pygame.draw.rect(surface, Colors.surface2, pygame.Rect(x, y, width, 8))
        health_percentage = self.health / self.max_health
        pygame.draw.rect(surface, Colors.red, pygame.Rect(x, y, int(width * health_percentage), 8))


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
