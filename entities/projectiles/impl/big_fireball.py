from core.client import Client
from core.world import Facing
from entities.Entity import Entity, DamageType
from entities.Item import ItemEntity
from entities.projectiles.projectile import Projectile


class BigFireball(Projectile):
    def __init__(self, x: int, y: int, author: Entity):
        super().__init__(x, y, sprites_path=r"./resources/sprites/big_fireball", author=author, damage_value=100)
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

        self.do_damage()
        if self.x > Client.get_screen().get_width()*5 or self.x+self.width < 0-Client.get_screen().get_width()*5 or self.y > Client.get_screen().get_height()*5 or self.y + self.height < 0:
            self.death()

    def do_damage(self):
        for entity in self.world.entities:
            if entity != self and entity != self.author and not isinstance(entity, ItemEntity):
                if isinstance(entity, Projectile) and entity.author == self.author:
                    return
                if ((entity.x <= self.x <= entity.x + entity.width) or (
                        entity.x <= self.x + self.width <= entity.x + entity.width)) and (
                        (entity.y <= self.y <= entity.y + entity.height) or (
                        entity.y <= self.y + self.height <= entity.y + entity.height)):
                    self.health -= entity.health
                    entity.damage(self.damage_value, DamageType.PROJECTILE, self.author)
