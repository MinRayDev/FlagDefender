import time

import pygame
from catppuccin import Flavour

from core.client import Client
from entities.Entity import Entity, EntityType
from util.instance import get_game, get_client


class WallEntity(Entity):
    def __init__(self, x, y, world):
        super().__init__(x, y, r"./resources/sprites/spells/wall", world, health=400)
        self.y = Client.get_screen().get_height() - self.world.floor - self.height
        self.creation_time = time.time()
        self.has_gravity = False
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
        percentage = (time.time() - self.creation_time) / 10
        pygame.draw.rect(surface, Flavour.frappe().surface2.rgb, pygame.Rect(
            int(self.width + 8) + (
                        self.x - 4 + get_client().get_screen().get_width() // 2 + get_game().scroll - get_game().main_player.entity.width // 2) - int(
                (self.width + 8) * percentage),
            self.y - 22 - 5, int((self.width + 8) * percentage), 8))
    def activity(self):
        super().activity()
        if time.time() > self.creation_time + 10:
            self.death()
