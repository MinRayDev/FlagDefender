from __future__ import annotations

import time

from pygame import Surface

from core.chat.chat import entity_register
from core.player import Player
from core.world import Facing
from entities.entity import Entity, EntityType
from entities.projectiles.impl.turret_projectile import TurretBullet
from util.world_util import get_entities_in_area


@entity_register
class TurretEntity(Entity):
    def __init__(self, x, y, world):
        super().__init__(x, y, r"./resources/sprites/build/turret", world, health=400)
        self.to_floor()
        self.creation_time = time.time()
        self.has_gravity = False
        self.has_collisions = False
        self.cooldown = 0
        self.type = EntityType.ALLY

    def draw(self, surface: Surface) -> None:
        super().draw(surface)
        self.draw_health_bar(surface)

    def activity(self):
        super().activity()
        if time.time() >= self.cooldown + 0.5:
            self.cooldown = time.time()
            for entity in self.world.entities:
                if entity.type == EntityType.ENEMY:
                    if self.x - int(self.width * 1.5) <= entity.x <= self.x:
                        self.facing = Facing.WEST
                        TurretBullet(self.x, self.y + 20, self, (entity.x, entity.x))
                    elif self.x + self.width + int(self.width * 1.5) >= entity.x >= self.x + self.width:
                        self.facing = Facing.EAST
                        TurretBullet(self.x, self.y + 20, self, (entity.x, entity.x))
                    break

    @staticmethod
    def new(author: Player) -> TurretEntity:
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