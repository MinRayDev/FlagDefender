import random

from core.client import Client
from entities.Entity import Entity, DamageType, EntityType
from entities.livingentities.mob_basic import MobBasic
from util.instance import get_game


class Flag(Entity):
    def __init__(self, x, y, world):
        super().__init__(x, y, r"./resources/sprites/spawner", world)
        self.y = Client.get_screen().get_height() - self.world.floor - self.height
        self.has_collisions = False
        self.type = EntityType.ENEMY

    def draw(self, surface):
        surface.blit(self.sprite_selected, (self.x+Client.get_screen().get_width()//2 + get_game().scroll - get_game().main_player.entity.width//2, self.y))

    def activity(self):
        if random.randint(70, 5000) < 100:
            MobBasic(self.x, 0, self.world)
