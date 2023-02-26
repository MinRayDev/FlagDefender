import json
import time

import pygame
from catppuccin import Flavour

from core.client import Client
from core.world import Facing
from entities.Entity import Entity, EntityType
from entities.projectiles.impl.fireball import Fireball
from network.event import EventType
from network.types import NetworkEntityTypes
from util.instance import get_game, get_client


class TurretEntity(Entity):
    def __init__(self, x, y, world):
        super().__init__(x, y, r"./resources/sprites/spells/turret", world, health=200)
        self.y = Client.get_screen().get_height() - self.world.floor - self.height
        self.creation_time = time.time()
        self.has_gravity = False
        self.has_collisions = False
        self.cooldown = 0
        self.type = EntityType.ALLY

    def draw(self, surface):
        surface.blit(self.sprite_selected, (self.x+Client.get_screen().get_width()//2 + get_game().scroll - get_game().main_player.entity.width//2, self.y))
        pygame.draw.rect(surface, Flavour.frappe().surface2.rgb, pygame.Rect(
            self.x - 4 + get_client().get_screen().get_width() // 2 + get_game().scroll - get_game().main_player.entity.width // 2,
            self.y - 14, self.width + 8, 8))
        health_percentage = self.health / self.max_health
        pygame.draw.rect(surface, Flavour.frappe().red.rgb, pygame.Rect(
            self.x - 4 + get_client().get_screen().get_width() // 2 + get_game().scroll - get_game().main_player.entity.width // 2,
            self.y - 14, int((self.width + 8) * health_percentage), 8))

        pygame.draw.rect(surface, Flavour.frappe().green.rgb, pygame.Rect(
            self.x - 4 + get_client().get_screen().get_width() // 2 + get_game().scroll - get_game().main_player.entity.width // 2,
            self.y - 22 - 5, self.width + 8, 8))
        percentage = (time.time() - self.creation_time) / 20
        pygame.draw.rect(surface, Flavour.frappe().surface2.rgb, pygame.Rect(
            int(self.width + 8) + (self.x - 4 + get_client().get_screen().get_width() // 2 + get_game().scroll - get_game().main_player.entity.width // 2) - int((self.width + 8) * percentage) ,
            self.y - 22 - 5, int((self.width + 8) * percentage), 8))

    def activity(self):
        super().activity()
        if time.time() >= self.cooldown + 0.5:
            self.cooldown = time.time()
            for entity in self.world.entities:
                if entity.type == EntityType.ENEMY:
                    if self.x - int(self.width*1.5) <= entity.x <= self.x:
                        self.facing = Facing.WEST
                        fb = Fireball(self.x, self.y+20, self)
                        get_client().send_event(EventType.ENTITY_SPAWN, {"entity_type": NetworkEntityTypes.from_class(fb).get_value(), "entity": fb.to_json()})
                    elif self.x + self.width + int(self.width*1.5) >= entity.x >= self.x + self.width:
                        self.facing = Facing.EAST
                        fb = Fireball(self.x, self.y+20, self)
                        get_client().send_event(EventType.ENTITY_SPAWN, {"entity_type": NetworkEntityTypes.from_class(fb).get_value(), "entity": fb.to_json()})
        if time.time() > self.creation_time + 20:
            self.death()
