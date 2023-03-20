from entities.Entity import Entity, DamageType
from entities.Item import ItemEntity


class Projectile(Entity):
    def __init__(self, x: int, y: int, sprites_path: str, author: Entity, damage_value=1):
        super().__init__(x, y, sprites_path, author.world, author.facing, health=damage_value)
        self.author = author
        self.has_gravity = False
        self.damage_value = damage_value
        self.motion_x, self.motion_y = 0, 0

    def do_damage(self):
        for entity in self.world.entities:
            if entity != self and entity != self.author and not isinstance(entity, ItemEntity):
                if isinstance(entity, Projectile) and entity.author == self.author:
                    return
                if ((entity.x <= self.x <= entity.x + entity.width) or (
                        entity.x <= self.x + self.width <= entity.x + entity.width)) and (
                        (entity.y <= self.y <= entity.y + entity.height) or (
                        entity.y <= self.y + self.height <= entity.y + entity.height)):
                    entity.damage(self.damage_value, DamageType.PROJECTILE, self.author)
                    self.death()
