import math
import random

from core.chat.chat import entity_register
from core.world import Facing
from entities.entity import DamageType
from entities.livingentities.mob import Mob
from util.instance import get_client
from util.logger import log


# TODO
@entity_register
class MobSpeedPhysical(Mob):
    def __init__(self, x, y, world, facing=Facing.SOUTH):
        super().__init__(x, y, sprites_path=r"./resources/sprites/mobs/speed_physical", facing=facing, world=world, health=100)
        self.walk_sprites = (self.sprites["1"], self.sprites["2"], self.sprites["3"], self.sprites["4"])
        self.cooldown = 30
        self.incline = 2
        self.gravity_value = 0 - self.incline
        self.can_move = True
        self.to_floor_time = 0
        self.jump_time = 0

        incline_adjust = self.incline * (9 / 10)
        incline_factor: float = (10 - incline_adjust) / 10
        angle_target: float = math.pi / 2 + ((math.pi / 2) * incline_factor)

        self.motion_x = 7 * math.cos(angle_target)
        if self.facing == Facing.WEST:
            self.motion_x *= -1

        self.deceleration = 0.1  # acceleration verticale

    def activity(self) -> None:
        super().activity()
        log("Target: " + str(self.target) + " Motion: " + str(self.motion_x))
        self.sprite_selected = self.walk_sprites[1]
        if not self.is_flying():
            if self.facing == Facing.EAST:
                self.motion_x = abs(self.motion_x)
            elif self.facing == Facing.WEST:
                self.motion_x = - abs(self.motion_x)
        if self.y + self.height + self.gravity_value >= get_client().get_screen().get_height() - self.world.floor:
            self.to_floor()
            self.gravity_value = 0 - self.incline

    def attack(self) -> None:
        if random.randint(30, 100) > 70:
            to_attack = self.target
            if to_attack is not None:
                if self.facing == Facing.EAST and self.x + 150 >= to_attack.x >= self.x:
                    to_attack.damage(10, DamageType.PHYSICAL, self)
                elif self.facing == Facing.WEST and self.x - 150 <= to_attack.x <= self.x:
                    to_attack.damage(10, DamageType.PHYSICAL, self)

    def go_to(self, pos: tuple[int, int]) -> None:
        if self.has_ai and self.can_move:
            col = self.get_collisions()
            if self.x != pos[0]:
                if self.x > pos[0] and col[Facing.WEST]:
                    self.facing = Facing.WEST
                elif self.x < pos[0] and col[Facing.EAST]:
                    self.facing = Facing.EAST
                self.x += self.motion_x
                self.y += self.gravity_value
                self.gravity_value += self.deceleration
                self.gravity_value = max(min(self.gravity_value, 10), -10)
