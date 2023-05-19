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
    """Class 'Entity' is the base class for all entities in the game.

        Extends 'Object'.
        :ivar has_gravity: Whether the entity has gravity or not.
        :type has_gravity: bool.
        :ivar world: The world the entity is in.
        :type world: World.
        :ivar health: The health of the entity.
        :type health: float.
        :ivar max_health: The maximum health of the entity.
        :type max_health: float.
        :ivar facing: The facing of the entity.
        :type facing: Facing.
        :ivar sprites_files: The files of the sprites of the entity.
        :type sprites_files: list[str].
        :ivar sprites: The sprites of the entity.
        :type sprites: dict[str, Surface].
        :ivar sprite_selected: The selected sprite of the entity.
        :type sprite_selected: Surface.
        :ivar max_height: The maximum height of the entity.
        :type max_height: int.
        :ivar max_width: The maximum width of the entity.
        :type max_width: int.
        :ivar gravity_value: The gravity value of the entity.
        :type gravity_value: float.
        :ivar uuid_: The uuid of the entity.
        :type uuid_: uuid.UUID.
        :ivar source: The source of the entity.
        :type source: int.
        :ivar type: The type of the entity.
        :type type: EntityType.

    """
    has_gravity: bool
    world: World
    health: float
    max_health: float
    facing: Optional[Facing]
    sprites_files: list[str]
    sprites: dict[str, Surface]
    sprite_selected: Surface
    max_height: int
    max_width: int
    gravity_value: float
    uuid_: uuid.UUID
    source: int
    type: EntityType

    def __init__(self, x: int, y: int, sprites_path: str, world: World, facing: Optional[Facing] = None, health=float("inf"), gravity=True):
        """Constructor for class 'Entity'.

            :param x: The x position of the entity.
            :type x: int.
            :param y: The y position of the entity.
            :type y: int.
            :param sprites_path: The path of the sprites of the entity.
            :type sprites_path: str.
            :param world: The world the entity is in.
            :type world: World.
            :param facing: The facing of the entity.
            :type facing: Facing.
            :param health: The health of the entity.
            :type health: float.
            :param gravity: Whether the entity has gravity or not.
            :type gravity: bool.

        """
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
        self.uuid_: uuid.UUID = uuid.uuid4()
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

    def activity(self) -> None:
        """The activity of the entity."""
        super().activity()
        if self.health <= 0:
            self.death()
        self.gravity()

    def death(self) -> None:
        """The death of the entity."""
        if self in self.world.entities:
            del self.world.entities[self.world.entities.index(self)]

    def draw(self, surface: Surface) -> None:
        """Draws the entity on the surface.

            :param surface: The surface to draw the entity on.
            :type surface: Surface.

        """
        draw_with_scroll(surface, self.sprite_selected, self.x, self.y)

    def is_flying(self) -> bool:
        """Returns whether the entity is flying or not.

            :return: Whether the entity is flying or not.
            :rtype: bool.

        """
        return self.y + self.height < get_client().get_screen().get_height() - self.world.floor

    def get_floor_dist(self) -> int:
        """Returns the distance between the entity and the floor.

            :return: The distance between the entity and the floor.
            :rtype: int.

        """
        return get_client().get_screen().get_height() - self.world.floor - self.y - self.height

    def damage(self, amount: float, damage_type: DamageType, author: Entity = None) -> None:
        """Damages the entity.

            :param amount: The amount of damage.
            :type amount: float.
            :param damage_type: The type of damage.
            :type damage_type: DamageType.
            :param author: The author of the damage.
            :type author: Entity.

        """
        from entities.livingentities.player_entity import PlayerEntity
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
        """Applies gravity to the entity."""
        if self.has_gravity:
            if self.is_flying():
                if self.y + self.height + self.gravity_value < get_client().get_screen().get_height() - self.world.floor:
                    self.y += self.gravity_value
                else:
                    self.to_floor()

    @staticmethod
    def get_entity_by_uuid(entity_uuid: str | uuid.UUID) -> Entity:
        """Returns the entity with the specified uuid.

            :param entity_uuid: The uuid of the entity.
            :type entity_uuid: str | uuid.UUID.
            :return: The entity with the specified uuid.
            :rtype: Entity.

        """
        if isinstance(entity_uuid, str):
            entity_uuid = uuid.UUID(entity_uuid)
        for world in get_game().current_level.worlds:
            for entity_ in world.entities:
                if entity_.uuid_ == entity_uuid:
                    return entity_

    def to_json(self) -> dict[str, int | float | Facing | None | str]:
        """Returns the json representation of the entity.

            :return: The json representation of the entity.
            :rtype: dict[str, int | float | Facing | None | str].
        """
        return {"entity_type": str(self.__class__).split("'")[1], "x": self.x, "y": self.y, "health": self.health,
                "facing": self.facing, "uuid": str(self.uuid_)}

    def draw_health_bar(self, surface: Surface, offset: int = 0) -> None:
        """Draws the health bar of the entity.

            :param surface: The surface to draw the health bar on.
            :type surface: Surface.
            :param offset: The offset of the health bar.
            :type offset: int.

        """
        x: int = self.x - 4 + surface.get_width() // 2 + get_game().current_level.scroll - get_game().current_level.main_player.entity.width // 2 + offset
        y: int = self.y - 14
        width: int = self.width + 8
        pygame.draw.rect(surface, Colors.surface2, pygame.Rect(x, y, width, 8))
        health_percentage = self.health / self.max_health
        pygame.draw.rect(surface, Colors.red, pygame.Rect(x, y, int(width * health_percentage), 8))

    def distance_to(self, other: Entity) -> int:
        """Returns the distance between the entity and another entity.

            :param other: The other entity.
            :type other: Entity.
            :return: The distance between the entity and another entity.
            :rtype: int.

        """
        return abs(self.x - other.x)


class DamageType(enum.IntEnum):
    """Class 'DamageType' contains the different types of damage.

        Extends 'IntEnum'.
        :cvar WORLD: The damage is caused by the world.
        :cvar GAME: The damage is caused by the game.
        :cvar PROJECTILE: The damage is caused by a projectile.
        :cvar PHYSICAL: The damage is caused by a physical entity.
        :cvar EXPLOSION: The damage is caused by an explosion.

    """
    WORLD = 0
    GAME = 1
    PROJECTILE = 2
    PHYSICAL = 3
    EXPLOSION = 4


class EntityType(enum.IntEnum):
    """Class 'EntityType' contains the different types of entities.

        Extends 'IntEnum'.
        :cvar DEFAULT: The entity is a default entity.
        :cvar ENEMY: The entity is an enemy.
        :cvar ALLY: The entity is an ally.

    """
    DEFAULT = 1
    ALLY = 2
    ENEMY = 3
