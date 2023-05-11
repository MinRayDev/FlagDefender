from __future__ import annotations

from core.ingame.item.item_type import ItemType
from core.ingame.spell.spell import Spell
from core.player import Player
from core.world import Facing
from util.world_util import teleport


class NearTp(Spell):
    price: int = 3

    @staticmethod
    def new(author: Player) -> None:
        if author.inventory.get_item_count(ItemType.magical_essence) >= NearTp.price:
            author.inventory.remove_item(ItemType.magical_essence, NearTp.price)
            if author.entity.facing == Facing.EAST:
                teleport(author.entity, author.entity.world, author.entity.x + author.entity.width * 2.5)
            elif author.entity.facing == Facing.WEST:
                teleport(author.entity, author.entity.world, author.entity.x - author.entity.width * 2.5)
