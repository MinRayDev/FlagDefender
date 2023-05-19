import time

from core.world import Facing
from entities.entity import Entity
from entities.projectiles.impl.fireball import Fireball
from util.instance import get_game, get_client
from util.logger import log, LogColors
from util.time_util import has_elapsed


class MortarBullet(Fireball):
    """Class 'MortarBullet'.

        Extends 'Fireball'.
        :ivar start_x: The start x position of the mortar bullet.
        :type start_x: int.
        :ivar start_y: The start y position of the mortar bullet.
        :type start_y: int.
        :ivar formula: The formula of the parabola.
        :type formula: str.
        :ivar start_time: The start time of the mortar bullet.
        :type start_time: float.

    """
    start_x: int
    start_y: int
    formula: str
    start_time: float
    dist_base: int

    def __init__(self, x: int, y: int, author: Entity, target: Entity) -> None:
        """Constructor of the class 'MortarBullet'.

            :param x: The x position of the mortar bullet.
            :type x: int.
            :param y: The y position of the mortar bullet.
            :type y: int.
            :param author: The author of the mortar bullet.
            :type author: Entity.
            :param target: The target of the mortar bullet.
            :type target: Entity.

        """
        super().__init__(x, y, author)
        self.y = author.y + 10
        self.start_y = self.y
        self.motion_x = 2
        self.facing = author.facing
        if self.facing == Facing.WEST:
            self.dist_base = abs(self.x - target.x)
            self.x = author.x - self.width - 2
            self.motion_x = -2
        else:
            self.dist_base = abs(self.x - target.x)
            self.x = author.x + author.width + 2
        self.start_x = self.x

        # Formula: (1/65)*x**2 - (dist_base/65)*x + start_y
        # 1/65 so the parabola is not too high
        # dist_base/65 so the parabola is not too long (dist_base is the distance between the mortar bullet (at the start) and the target)
        # start_y so the parabola starts at the right height
        self.formula = f"(1/65)*x**2 - ({self.dist_base}/65)*x + {self.start_y}"
        self.start_time = time.time()

    def activity(self) -> None:
        """Activity of the mortar bullet."""
        self.do_damage()
        # If the mortar bullet is not on the floor and its next y position is not on the floor, it goes down
        if eval(self.formula.replace("x", str(self.x-self.start_x + self.motion_x))) < get_client().get_screen().get_height() - self.world.floor:
            # X increases by 2 every tick (motion_x)
            self.x += self.motion_x
            # Y is calculated with the formula (see above)
            self.y = eval(self.formula.replace("x", str(self.x-self.start_x)))
        else:
            # If the mortar bullet goes to the floor, it will die faster
            self.start_time -= 15
            self.to_floor()
        if self.x > get_client().get_screen().get_width() * 5 or self.x + self.width < 0 - get_client().get_screen().get_width() * 5 or self.y > get_client().get_screen().get_height() * 5:
            self.death()
        elif has_elapsed(self.start_time, 20):
            self.death()
