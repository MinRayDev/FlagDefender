from entities.entity import Entity, DamageType
from entities.item import ItemEntity
from entities.world_objects.portal import PortalEntity


class Projectile(Entity):
    def __init__(self, x: int, y: int, sprites_path: str, author: Entity, damage_value=1):
        super().__init__(x, y, sprites_path, author.world, author.facing, health=damage_value)
        self.author = author
        self.type = author.type
        self.has_gravity = False
        self.has_collisions = False
        self.damage_value = damage_value
        self.motion_x, self.motion_y = 0, 0

    def do_damage(self):
        for entity in self.world.entities:
            if self.can_damage(entity):
                entity.damage(self.damage_value, DamageType.PROJECTILE, self.author)
                self.death()

    def can_damage(self, entity: Entity):
        if entity != self and entity != self.author and not isinstance(entity, ItemEntity) and not isinstance(entity, PortalEntity):
            if (isinstance(entity, Projectile) and entity.author == self.author) or self.type == entity.type:
                return False
            if ((entity.x <= self.x <= entity.x + entity.width) or (
                    entity.x <= self.x + self.width <= entity.x + entity.width)) and (
                    (entity.y <= self.y <= entity.y + entity.height) or (
                    entity.y <= self.y + self.height <= entity.y + entity.height)):
                return True
        return False
