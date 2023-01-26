from entities.Entity import Entity
from entities.projectiles.projectile import Projectile
from core.world import Facing


class Waterball(Projectile):
    def __init__(self, x: int, y: int, author: Entity):
        super().__init__(x, y, sprites_path=r"./resources/sprites/test2", author=author)
        self.gravity = -6
        self.motion_x = 0
        self.motion_y = 5
        match self.facing:
            case Facing.NORTH:
                self.motion_y = -5
                self.x += 78 // 2 - self.width // 2
                self.y -= 16
            case Facing.EAST:
                self.motion_x = 3
                self.motion_y = 0
                self.x += 78
                self.y += 20
            case Facing.SOUTH:
                self.x += 78 // 2 - self.width // 2
                self.y += 80 - 30
            case Facing.WEST:
                self.motion_x = -3
                self.motion_y = 0
                self.x -= 16
                self.y += 20

    def activity(self, **kwargs):
        super().activity()
        self.x += self.motion_x
        self.y += self.motion_y
        if self.facing == Facing.EAST or self.facing == Facing.WEST:
            self.y += self.gravity
            self.gravity += 0.1

        if self.x > 500 or self.x+self.width < 0 or self.y > 500:
            self.death()
