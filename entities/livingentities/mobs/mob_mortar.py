import random

from core.chat.chat import entity_register
from core.world import Facing
from entities.entity import EntityType
from entities.livingentities.mob import Mob
from entities.projectiles.impl.mortar_bullet import MortarBullet
from util import world_util

# TODO
@entity_register
class MobMortar(Mob):
    def __init__(self, x, y, world, facing=Facing.SOUTH):
        super().__init__(x, y, sprites_path=r"./resources/sprites/mobs/mortar", facing=facing, world=world, health=100)
        self.attack_sprites = (self.sprites["1"], self.sprites["3"])
        self.walk_sprites = (self.sprites["2"], self.sprites["4"])
        self.cooldown = 31
        self.distance_damage = True
        # self.target_range = 10 * 200 + 10 * random.randint(0, 20)
        # self.attack_range = 10 * 100 + 7 * random.randint(0, 20)

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
            to_attack = world_util.nearest_entity(self, EntityType.ALLY)
            if to_attack is not None:
                if to_attack.x > self.x + self.width:
                    self.facing = Facing.EAST
                    MortarBullet(0, 0, self, to_attack)
                elif self.x > to_attack.x + to_attack.width:
                    self.facing = Facing.WEST
                    MortarBullet(0, 0, self, to_attack)