import random

from core.chat.chat import entity_register
from core.world import Facing
from entities.livingentities.mob import Mob
from entities.projectiles.impl.fireball import Fireball


@entity_register
class MobSpeed(Mob):
    def __init__(self, x, y, world, facing=Facing.SOUTH):
        super().__init__(x, y, sprites_path=r"./resources/sprites/mobs/speed", facing=facing, world=world, health=100)
        self.attack_sprites = (self.sprites["1"], self.sprites["3"])
        self.walk_sprites = (self.sprites["2"], self.sprites["4"])
        self.cooldown = 30
        self.distance_damage = True

    def activity(self):
        super().activity()
        if self.facing == Facing.WEST:
            if self.can_attack:
                self.sprite_selected = self.attack_sprites[0]
            else:
                self.sprite_selected = self.walk_sprites[0]
        elif self.facing == Facing.EAST:
            if self.can_attack:
                self.sprite_selected = self.attack_sprites[1]
            else:
                self.sprite_selected = self.walk_sprites[1]

    def attack(self):
        if random.randint(30, 100) > 70:
            Fireball(self.x, self.y, self)
