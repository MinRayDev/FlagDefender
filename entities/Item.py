import pygame

from core.client import Client
from core.ingame.item.item_type import ItemType

from core.world import World
from entities.Entity import Entity, DamageType
from entities.livingentities.entity_player import PlayerEntity
from util.instance import get_game


class ItemEntity(Entity):
    def __init__(self, x: int, sprites_path: str, world: World, item_type: ItemType):
        from core.player import Player
        super().__init__(x, 0, sprites_path, world, None)
        self.player_class = Player
        self.has_gravity = False
        self.has_collisions = False
        self.item_type = item_type
        self.sprites_path = sprites_path
        self.size = (48, 48)
        self.width, self.height = self.size
        self.y = Client.get_screen().get_height() - self.world.floor - self.height

    def activity(self, **kwargs):
        for entity in self.world.entities:
            if isinstance(entity, PlayerEntity):
                if self.contact(entity):
                    player = self.player_class.get_by_entity(entity)
                    if player.get_inventory().add_item(self.item_type, 1):
                        self.death()
                        break

    def draw(self, surface):
        img = pygame.transform.scale(self.sprite_selected, self.size)
        surface.blit(img, (self.x+Client.get_screen().get_width()//2 + get_game().scroll - self.width//2, self.y))

    def damage(self, amount: float, damage_type: DamageType):
        pass