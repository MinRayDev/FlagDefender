import time

import pygame
from catppuccin import Flavour
from pygame import Surface

from core.chat.chat import entity_register
from core.world import Facing
from entities.entity import Entity, EntityType
from entities.projectiles.impl.fireball import Fireball
from util.colors import Colors
from util.instance import get_game


@entity_register
class TurretSpellEntity(Entity):
    def __init__(self, x, y, world):
        super().__init__(x, y, r"./resources/sprites/spells/turret", world, health=200)
        self.to_floor()
        self.creation_time = time.time()
        self.has_gravity = False
        self.has_collisions = False
        self.cooldown = 0
        self.type = EntityType.ALLY

    def draw(self, surface: Surface) -> None:
        super().draw(surface)
        self.draw_health_bar(surface)
        x: int = self.x - 4 + surface.get_width() // 2 + get_game().current_level.scroll - get_game().current_level.main_player.entity.width // 2
        y: int = self.y - 27
        width: int = self.width + 8
        pygame.draw.rect(surface, Flavour.frappe().green.rgb, pygame.Rect(x, y, width, 8))
        percentage = (time.time() - self.creation_time) / 20
        pygame.draw.rect(surface, Colors.surface2, pygame.Rect(width + x - int(width * percentage), y, int(width * percentage), 8))

    def activity(self):
        super().activity()
        if time.time() >= self.cooldown + 0.5:
            self.cooldown = time.time()
            for entity in self.world.entities:
                if entity.type == EntityType.ENEMY:
                    if self.x - int(self.width * 1.5) <= entity.x <= self.x:
                        self.facing = Facing.WEST
                        Fireball(self.x, self.y + 20, self)
                    elif self.x + self.width + int(self.width * 1.5) >= entity.x >= self.x + self.width:
                        self.facing = Facing.EAST
                        Fireball(self.x, self.y + 20, self)
        if time.time() > self.creation_time + 20:
            self.death()
