import pygame
from pygame import Surface
from typing import TYPE_CHECKING

from core.world import World
from entities.entity import Entity, DamageType
from util.draw_util import draw_with_scroll

if TYPE_CHECKING:
    from core.ingame.item.item_type import ItemType


class ItemEntity(Entity):
    """Class 'ItemEntity'.

        Extends 'Entity'.
        :ivar item_type: The item type of the item entity.
        :type item_type: ItemType.
        :ivar sprites_path: The path of the sprites of the item entity.
        :type sprites_path: str.
        :ivar size: The size of the item entity.
        :type size: tuple[int, int].

    """
    item_type: 'ItemType'
    sprites_path: str
    size: tuple[int, int]

    def __init__(self, x: int, sprites_path: str, world: World, item_type: 'ItemType'):
        super().__init__(x, 0, sprites_path, world, None)
        self.has_gravity = False
        self.has_collisions = False
        self.item_type = item_type
        self.sprites_path = sprites_path
        self.width, self.height = self.size = (48, 48)
        self.to_floor()

    def activity(self) -> None:
        """The activity of the item entity."""
        from core.player import Player
        from entities.livingentities.player_entity import PlayerEntity
        for entity in self.world.entities:
            if isinstance(entity, PlayerEntity):
                if self.contact(entity):
                    player = Player.get_by_entity(entity)
                    if player.get_inventory().add_item(self.item_type, 1):
                        self.death()
                        break

    def draw(self, surface: Surface) -> None:
        """Draws the item entity on the surface."""
        draw_with_scroll(surface, pygame.transform.scale(self.sprite_selected, self.size), self.x, self.y)

    def damage(self, amount: float, damage_type: DamageType, author: Entity = None):
        pass

    def to_json(self) -> dict:
        """Returns the json representation of the item entity."""
        json_dict = super().to_json()
        json_dict["item_id"] = self.item_type.get_id()
        return json_dict
