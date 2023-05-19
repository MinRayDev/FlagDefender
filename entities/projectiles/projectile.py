from entities.entity import Entity, DamageType
from entities.item import ItemEntity
from entities.world_objects.portal import PortalEntity


class Projectile(Entity):
    """Class 'Projectile'.

        Extends 'Entity'.
        :ivar author: The author of the projectile.
        :type author: Entity
        :ivar damage_value: The damage value of the projectile.
        :type damage_value: int
        :ivar motion_x: The x motion of the projectile.
        :type motion_x: int
        :ivar motion_y: The y motion of the projectile.
        :type motion_y: int

     """
    author: Entity
    damage_value: int
    motion_x: int
    motion_y: int

    def __init__(self, x: int, y: int, sprites_path: str, author: Entity, damage_value: int = 1):
        super().__init__(x, y, sprites_path, author.world, author.facing, health=damage_value)
        self.author = author
        self.type = author.type
        self.has_gravity = False
        self.has_collisions = False
        self.damage_value = damage_value
        self.motion_x, self.motion_y = 0, 0

    def do_damage(self) -> None:
        """Do damage to the entities."""
        for entity in self.world.entities:
            if self.can_damage(entity):
                entity.damage(self.damage_value, DamageType.PROJECTILE, self.author)
                self.death()

    def can_damage(self, entity: Entity) -> bool:
        """Check if the projectile can damage the entity.

            :param entity: The entity to check.
            :type entity: Entity.

            :return: Whether the projectile can damage the entity or not.
            :rtype: bool.

        """
        if entity != self and entity != self.author and not isinstance(entity, ItemEntity) and not isinstance(entity, PortalEntity):
            if (isinstance(entity, Projectile) and entity.author == self.author) or self.type == entity.type:
                return False
            if ((entity.x <= self.x <= entity.x + entity.width) or (
                    entity.x <= self.x + self.width <= entity.x + entity.width)) and (
                    (entity.y <= self.y <= entity.y + entity.height) or (
                    entity.y <= self.y + self.height <= entity.y + entity.height)):
                return True
        return False
