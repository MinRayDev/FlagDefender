from core.client import Client
from util.world_util import teleport
from core.world import World
from entities.Entity import Entity, DamageType
from util.instance import get_game


class PortalEntity(Entity):
    def __init__(self, x: int, linked_x: int | str, world: World, linked_world: World):
        super().__init__(x, 0, r"./resources/sprites/portal", world, None)
        self.linked_x = linked_x
        self.linked_world = linked_world
        self.has_gravity = False
        self.has_collisions = False
        self.y = Client.get_screen().get_height() - self.world.floor - self.height

    def activity(self, **kwargs):
        for entity in self.world.entities:
            if self.contact(entity) and entity != self:
                teleport(entity, self.linked_world, self.linked_x)

    def draw(self, surface):
        surface.blit(self.sprite_selected, (self.x+Client.get_screen().get_width()//2 + get_game().scroll - self.width//2, self.y))

    def damage(self, amount: float, type: DamageType):
        pass
