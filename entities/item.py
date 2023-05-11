import pygame
from pygame import Surface

from core.ingame.item.item_type import ItemType
from core.world import World
from entities.entity import Entity, DamageType
from util.draw_util import draw_with_scroll


class ItemEntity(Entity):
    def __init__(self, x: int, sprites_path: str, world: World, item_type: ItemType):
        from core.player import Player
        super().__init__(x, 0, sprites_path, world, None)
        self.player_class = Player
        self.has_gravity = False
        self.has_collisions = False
        self.item_type = item_type
        self.sprites_path = sprites_path
        self.width, self.height = self.size = (48, 48)
        self.to_floor()

    def activity(self):
        from entities.livingentities.entity_player import PlayerEntity
        for entity in self.world.entities:
            if isinstance(entity, PlayerEntity):
                if self.contact(entity):
                    player = self.player_class.get_by_entity(entity)
                    if player.get_inventory().add_item(self.item_type, 1):
                        self.death()
                        break

    def draw(self, surface: Surface) -> None:
        draw_with_scroll(surface, pygame.transform.scale(self.sprite_selected, self.size), self.x, self.y)

    def damage(self, amount: float, damage_type: DamageType, author: Entity = None):
        pass

    def to_json(self) -> dict:
        json_dict = super().to_json()
        json_dict["item_id"] = self.item_type.get_id()
        return json_dict
