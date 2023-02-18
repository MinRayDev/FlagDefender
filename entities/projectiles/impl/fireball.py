from entities.Entity import Entity
from entities.projectiles.projectile import Projectile
from core.game import Game
from core.world import Facing


class Fireball(Projectile):
    def __init__(self, x: int, y: int, author: Entity):
        super().__init__(x, y, sprites_path=r"./resources/sprites/test", author=author, damage_value=20)
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

    def activity(self, **kwargs):
        super().activity()
        self.x += self.motion_x
        self.y += self.motion_y

        self.damage()
        if self.x > Game.instance.screen.get_width()*5 or self.x+self.width < 0-Game.instance.screen.get_width()*5 or self.y > Game.instance.screen.get_height()*5 or self.y + self.height < 0:
            self.death()
