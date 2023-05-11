import random

from core.chat.chat import entity_register
from core.world import Facing
from entities.entity import EntityType, DamageType
from entities.livingentities.mob import Mob
from util import world_util


@entity_register
class MobTank(Mob):
    def __init__(self, x, y, world, facing=Facing.SOUTH):
        super().__init__(x, y, sprites_path=r"./resources/sprites/mobs/tank", facing=facing, world=world, health=500)
        self.cooldown = 30
        self.distance_damage = True

    def activity(self) -> None:
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
                if self.facing == Facing.EAST and self.x + 150 >= to_attack.x >= self.x:
                    to_attack.damage(25, DamageType.PHYSICAL, self)
                elif self.facing == Facing.WEST and self.x - 150 <= to_attack.x <= self.x:
                    to_attack.damage(25, DamageType.PHYSICAL, self)
