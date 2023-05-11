import math
import pygame.transform
import time

from pygame import Surface

from core.world import Facing
from entities.livingentities.entity_player import PlayerEntity
from entities.projectiles.projectile import Projectile
from util.draw_util import draw_with_scroll
from util.instance import get_client
from util.time_util import has_elapsed


class Arrow(Projectile):
    def __init__(self, x: int, y: int, author: PlayerEntity):
        super().__init__(x, y, sprites_path=r"./resources/sprites/projectiles/arrow", author=author, damage_value=20)
        self.gravity_value = 0 - author.incline  # vitesse verticale, negative : vers le haut, positive : vers le bas
        self.start_time = time.time()

        angle_target: float

        incline_adjust = author.incline * (9 / 10)
        if incline_adjust > 0:
            # 0 -> 10
            # sin(pi) -> sin(pi/2)
            incline_factor: float = (10 - incline_adjust) / 10
            angle_target = math.pi / 2 + ((math.pi / 2) * incline_factor)
        else:
            # 0 -> -15
            # sin(pi/2) -> sin(pi + pi / 2) (i.e pi / .6666)
            incline_factor: float = -incline_adjust / 15
            angle_target = math.pi + (math.pi / 2 * incline_factor)

        self.motion_x = 10 * math.cos(angle_target)
        if self.facing == Facing.EAST:
            self.motion_x *= -1

        self.deceleration = 0.1  # acceleration verticale
        match self.facing:
            case Facing.EAST:
                self.x += author.width
                self.y += 20
            case Facing.WEST:
                self.x -= self.width
                self.y += 20
        self.rotate = self.update_rotation()

    def activity(self):
        super().activity()

        if self.y + self.height + self.gravity_value < get_client().get_screen().get_height() - self.world.floor:
            self.x += self.motion_x
            self.y += self.gravity_value
            self.gravity_value += self.deceleration
            self.gravity_value = max(min(self.gravity_value, 10), -10)

            # print(f"{gravity_factor=}")

            # self.rotate = 180 - math.sin(self.gravity_value * math.pi / 2)
            self.rotate = self.update_rotation()

        else:
            self.to_floor()

        if self.x > get_client().get_screen().get_width() * 5 or self.x + self.width < 0 - get_client().get_screen().get_width() * 5 or self.y > get_client().get_screen().get_height() * 5:
            self.death()
        elif has_elapsed(self.start_time, 10):
            self.death()
        self.do_damage()

    def draw(self, surface: Surface) -> None:
        draw_with_scroll(surface, pygame.transform.rotate(self.sprite_selected, self.rotate), self.x, self.y)

    def update_rotation(self) -> float:
        gravity_factor: float = max(min(self.gravity_value / 10, 1), -1)
        rotate = 90 + math.sin(gravity_factor * math.pi / 2) * 85
        if self.facing == Facing.EAST:
            rotate *= -1
        return rotate
