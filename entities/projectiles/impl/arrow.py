import math
import pygame.transform
import time

from pygame import Surface

from core.world import Facing
from entities.livingentities.player_entity import PlayerEntity
from entities.projectiles.projectile import Projectile
from util.draw_util import draw_with_scroll
from util.instance import get_client
from util.time_util import has_elapsed


class Arrow(Projectile):
    """Class 'Arrow'.

        Extends 'Projectile'.
        :ivar start_time: The time when the arrow was created.
        :type start_time: float.
        :ivar deceleration: The deceleration of the arrow.
        :type deceleration: float.
        :ivar rotation: The rotation of the arrow.
        :type rotation: float.

    """
    start_time: float
    deceleration: float
    rotation: float

    def __init__(self, x: int, y: int, author: PlayerEntity):
        """Constructor of the class 'Arrow'.

            :param x: The x position of the arrow.
            :type x: int.
            :param y: The y position of the arrow.
            :type y: int.
            :param author: The author of the arrow.
            :type author: PlayerEntity.

        """
        super().__init__(x, y, sprites_path=r"./resources/sprites/projectiles/arrow", author=author, damage_value=20)
        self.gravity_value = 0 - author.incline  # vitesse verticale, negative : vers le haut, positive : vers le bas
        self.start_time = time.time()

        incline_factor: float
        angle_target: float

        incline_adjust = author.incline * (9 / 10)
        if incline_adjust > 0:
            # 0 -> 10
            # sin(pi) -> sin(pi/2)
            incline_factor = (10 - incline_adjust) / 10
            angle_target = math.pi / 2 + ((math.pi / 2) * incline_factor)
        else:
            # 0 -> -15
            # sin(pi/2) -> sin(pi + pi / 2) (i.e pi / .6666)
            incline_factor = -incline_adjust / 15
            angle_target = math.pi + (math.pi / 2 * incline_factor)

        self.motion_x = int(10 * math.cos(angle_target))
        if self.facing == Facing.EAST:
            self.motion_x *= -1

        # Deceleration pixel/tick² decrease the speed (gravity_value each tick)
        self.deceleration = 0.1
        match self.facing:
            case Facing.EAST:
                self.x += author.width
                self.y += 20
            case Facing.WEST:
                self.x -= self.width
                self.y += 20
        self.rotate = self.update_rotation()

    def activity(self) -> None:
        """The activity of the arrow."""
        super().activity()

        if self.y + self.height + self.gravity_value < get_client().get_screen().get_height() - self.world.floor:
            # motion_x is the horizontal speed of the arrow and gravity_value is the vertical speed of the arrow (negative : up, positive : down) (gravity_value is increased each tick)
            self.x += self.motion_x
            self.y += self.gravity_value
            self.gravity_value += self.deceleration
            self.gravity_value = max(min(self.gravity_value, 10), -10)
            self.rotate = self.update_rotation()
        else:
            self.to_floor()

        if self.x > get_client().get_screen().get_width() * 5 or self.x + self.width < 0 - get_client().get_screen().get_width() * 5 or self.y > get_client().get_screen().get_height() * 5:
            self.death()
        elif has_elapsed(self.start_time, 10):
            self.death()
        self.do_damage()

    def draw(self, surface: Surface) -> None:
        """Draws the arrow.

            :param surface: The surface on which the arrow is drawn.
            :type surface: Surface.

        """

        draw_with_scroll(surface, pygame.transform.rotate(self.sprite_selected, self.rotate), self.x, self.y)

    def update_rotation(self) -> float:
        """Updates the rotation of the arrow.

            :return: The rotation of the arrow.
            :rtype: float.

        """
        gravity_factor: float = max(min(self.gravity_value / 10, 1), -1)
        rotate: float = 90 + math.sin(gravity_factor * math.pi / 2) * 85
        if self.facing == Facing.EAST:
            rotate *= -1
        return rotate
