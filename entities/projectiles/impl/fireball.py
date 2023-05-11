from pygame import Surface

from core.world import Facing
from entities.entity import Entity
from entities.projectiles.projectile import Projectile
from util.draw_util import draw_with_scroll
from util.instance import get_client


class Fireball(Projectile):
    def __init__(self, x: int, y: int, author: Entity):
        super().__init__(x, y, sprites_path=r"./resources/sprites/projectiles/fireball", author=author, damage_value=20)
        self.frame = 0
        self.start_x = x
        match self.facing:
            case Facing.NORTH:
                self.motion_y = -5
                self.x += 78 // 2 - self.width // 2
                self.y -= 16
            case Facing.EAST:
                self.motion_x = 5
                self.x += 78
                self.y += 20
            case Facing.SOUTH:
                self.motion_y = 5
                self.x += 78 // 2 - self.width // 2
                self.y += 80 - 30
            case Facing.WEST:
                self.motion_x = -5
                self.x -= 16
                self.y += 20

    def draw(self, surface: Surface) -> None:
        if round(self.frame) < len(self.sprites):
            draw_with_scroll(surface, list(self.sprites.values())[round(self.frame)], self.x, self.y)
        else:
            self.frame = 0
            draw_with_scroll(surface, list(self.sprites.values())[self.frame], self.x, self.y)
        self.frame += 0.2

    def activity(self):
        super().activity()
        self.x += self.motion_x
        self.y += self.motion_y

        self.do_damage()
        if self.x > get_client().get_screen().get_width() * 5 or self.x + self.width < 0 - get_client().get_screen().get_width() * 5 or self.y > get_client().get_screen().get_height() * 5 or self.y + self.height < 0:
            self.death()
        if abs(self.x - self.start_x) > 1000:
            self.death()
