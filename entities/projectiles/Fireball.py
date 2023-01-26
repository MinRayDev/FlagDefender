from entities.Entity import Entity
from entities.projectiles.projectile import Projectile
from core.game import Game
from core.world import Facing


class Fireball(Projectile):
    def __init__(self, x: int, y: int, author: Entity):
        super().__init__(x, y, sprites_path=r"./resources/sprites/test", author=author)
        self.motion_x = 0
        self.motion_y = 0
        self.damage = 20
        self.author = author
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

        for entity in Game.instance.actual_world.entities:
            if entity != self and entity != self.author:
                if ((entity.x <= self.x <= entity.x + entity.width) or (
                        entity.x <= self.x + self.width <= entity.x + entity.width)) and (
                        (entity.y <= self.y <= entity.y + entity.height) or (
                        entity.y <= self.y + self.height <= entity.y + entity.height)):
                    entity.health -= self.damage
                    self.death()
        if self.x > 500 or self.x + self.width < 0 or self.y > 500 or self.y + self.height < 0:
            self.death()
