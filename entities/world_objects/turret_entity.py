from __future__ import annotations

import time

from pygame import Surface

from core.chat.chat import entity_register
from core.player import Player
from core.world import Facing, World
from entities.entity import Entity, EntityType
from entities.projectiles.impl.fireball import Fireball
from entities.projectiles.impl.turret_projectile import TurretBullet
from entities.projectiles.projectile import Projectile
from util.world_util import get_entities_in_area


@entity_register
class TurretEntity(Entity):
    """Class 'TurretEntity'.

        Extends 'Entity'.
        :ivar creation_time: The time the entity was created.
        :type creation_time: float.

    """
    creation_time: float

    def __init__(self, x: int, y: int, world: World):
        """Constructor of the class 'TurretEntity'.

            :param x: The x coordinate of the entity.
            :type x: int.
            :param y: The y coordinate of the entity.
            :type y: int.
            :param world: The world the entity is in.
            :type world: World.

        """
        super().__init__(x, y, r"./resources/sprites/build/turret", world, health=400)
        self.to_floor()
        self.creation_time = time.time()
        self.has_gravity = False
        self.has_collisions = False
        self.cooldown = 0
        self.type = EntityType.ALLY

    def draw(self, surface: Surface) -> None:
        """Draws the entity on the surface.

            :param surface: The surface to draw on.
            :type surface: Surface.

        """
        super().draw(surface)
        self.draw_health_bar(surface)

    def activity(self) -> None:
        """The activity of the entity."""
        super().activity()
        if time.time() >= self.cooldown + 0.5:
            self.cooldown = time.time()
            for entity in self.world.entities:
                if entity.type == EntityType.ENEMY and not isinstance(entity, Projectile):
                    if self.x - int(self.width * 1.5) <= entity.x <= self.x and entity.y <= self.y * 1.2:
                        self.facing = Facing.WEST
                        Fireball(self.x, self.y + 20, self)
                    elif self.x + self.width + int(
                            self.width * 1.5) >= entity.x >= self.x + self.width and entity.y <= self.y * 1.2:
                        self.facing = Facing.EAST
                        Fireball(self.x, self.y + 20, self)

    @staticmethod
    def new(author: Player) -> TurretEntity:
        """Creates a new entity.

            :param author: The player who created the entity.
            :type author: Player.

            :return: The new entity.
            :rtype: TurretEntity.

        """
        match author.entity.facing:
            case Facing.EAST:
                if len(get_entities_in_area((author.entity.x + author.entity.width + 10, None),
                                            (author.entity.x + author.entity.width + 10 + 100, None),
                                            author.entity.world)) == 0:
                    return TurretEntity(author.entity.x + author.entity.width + 10, 0, author.entity.world)
            case Facing.WEST:
                if len(get_entities_in_area((author.entity.x - 100 - 10, None),
                                            (author.entity.x - 10, None),
                                            author.entity.world)) == 0:
                    return TurretEntity(author.entity.x - 100 - 10, 0, author.entity.world)
