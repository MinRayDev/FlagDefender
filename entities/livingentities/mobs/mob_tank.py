import math
import random
import time

from core.chat.chat import entity_register
from core.world import Facing, World
from entities.entity import DamageType
from entities.livingentities.mob import Mob
from util.instance import get_client
from util.time_util import has_elapsed


@entity_register
class MobTank(Mob):
    """Class 'MobTank'.

        Extend 'Mob'.
        :ivar incline: The incline of the mob.
        :type incline: float.
        :ivar last_floor: The last floor of the mob.
        :type last_floor: float.

    """
    incline: float
    last_floor: float

    def __init__(self, x: int, y: int, world: World, facing: Facing = Facing.SOUTH):
        """Constructor of the class 'MobTank'.

            :param x: The x coordinate of the mob.
            :type x: int.
            :param y: The y coordinate of the mob.
            :type y: int.
            :param world: The world of the mob.
            :type world: World.
            :param facing: The facing of the mob.
            :type facing: Facing.

        """
        super().__init__(x, y, sprites_path=r"./resources/sprites/mobs/tank", facing=facing, world=world, health=400)
        self.incline = 3.5
        self.gravity_value = -self.incline
        self.can_move = True
        self.last_floor = 0
        self.cooldown = 45
        incline_adjust: float = self.incline * (9 / 10)
        incline_factor: float = (10 - incline_adjust) / 10
        angle_target: float = math.pi / 2 + ((math.pi / 2) * incline_factor)

        self.motion_x = 7 * math.cos(angle_target)
        if self.facing == Facing.WEST:
            self.motion_x *= -1
        # Deceleration pixel/tick² decrease the speed (gravity_value each tick)
        self.deceleration = 0.1

    def activity(self) -> None:
        """Object's activity function."""
        self.sprite_selected = self.sprites["1"]
        if self.y + self.sprites["2"].get_height() + self.gravity_value >= get_client().get_screen().get_height() - self.world.floor:
            self.to_floor()
            self.gravity_value = 0 - self.incline
        if not self.is_flying():
            if has_elapsed(self.last_floor, 0.75):
                self.last_floor = time.time()

            if self.facing == Facing.EAST:
                self.motion_x = abs(self.motion_x)
            elif self.facing == Facing.WEST:
                self.motion_x = -abs(self.motion_x)
            if not has_elapsed(self.last_floor, 0.175) and self.sprite_selected != self.sprites["4"]:
                self.sprite_selected = self.sprites["4"]
                self.height = self.sprite_selected.get_height()
                self.to_floor()
            elif self.sprite_selected:
                self.sprite_selected = self.sprites["1"]
                self.height = self.sprite_selected.get_height()
                self.to_floor()
        elif self.sprite_selected != self.sprites["2"]:
            self.sprite_selected = self.sprites["2"]
            self.height = self.sprite_selected.get_height()
        super().activity()

    def randomize_wait(self) -> bool:
        """Randomize wait function."""
        return False

    def attack(self) -> None:
        """Entity's attack function."""
        if random.randint(0, 100) > 70:
            to_attack = self.target
            if to_attack is not None:
                if self.facing == Facing.EAST and self.x + 150 >= to_attack.x >= self.x:
                    to_attack.damage(50, DamageType.PHYSICAL, self)
                elif self.facing == Facing.WEST and self.x - 150 <= to_attack.x <= self.x:
                    to_attack.damage(50, DamageType.PHYSICAL, self)

    def go_to(self, pos: tuple[int, int]) -> None:
        """Entity's go-to function.

            Moves the entity to the given position.

            :param pos: The position to move to.
            :type pos: tuple[int, int].

        """
        if self.has_ai and self.can_move and has_elapsed(self.last_floor, 0.5):
            col = self.get_collisions()
            if self.x != pos[0]:
                if self.x > pos[0] and col[Facing.WEST]:
                    self.facing = Facing.WEST
                elif self.x < pos[0] and col[Facing.EAST]:
                    self.facing = Facing.EAST
                # motion_x is the horizontal speed of the arrow and gravity_value is the vertical speed of the arrow (negative : up, positive : down) (gravity_value is increased each tick)
                self.x += self.motion_x
                self.y += self.gravity_value
                self.gravity_value += self.deceleration
                self.gravity_value = max(min(self.gravity_value, 10), -10)