import time

import pygame
from catppuccin import Flavour
from pygame import Surface

from core.chat.chat import entity_register
from entities.entity import Entity, EntityType
from util.colors import Colors
from util.instance import get_game


@entity_register
class WallSpellEntity(Entity):
    def __init__(self, x, y, world):
        super().__init__(x, y, r"./resources/sprites/spells/wall", world, health=400)
        self.to_floor()
        self.creation_time = time.time()
        self.has_gravity = False
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
        if time.time() > self.creation_time + 10:
            self.death()
