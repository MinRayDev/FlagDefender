from core.game import Game
from entities.Entity import Entity


class Projectile(Entity):
    def __init__(self, x: int, y: int, sprites_path: str, author: Entity, damage_value=1):
        super().__init__(x, y, sprites_path, author.world, author.facing, health=damage_value)
        self.author = author
        self.has_gravity = False
        self.damage_value = damage_value
        self.motion_x, self.motion_y = 0, 0

    def damage(self):
        for entity in Game.instance.actual_world.entities:
            if entity != self and entity != self.author:
                if ((entity.x <= self.x <= entity.x + entity.width) or (
                        entity.x <= self.x + self.width <= entity.x + entity.width)) and (
                        (entity.y <= self.y <= entity.y + entity.height) or (
                        entity.y <= self.y + self.height <= entity.y + entity.height)):
                    entity.health -= self.damage_value
                    self.death()