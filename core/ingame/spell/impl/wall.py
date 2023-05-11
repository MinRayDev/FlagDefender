from __future__ import annotations

import time

from core.ingame.item.item_type import ItemType
from core.ingame.spell.spell import Spell
from core.player import Player
from core.world import Facing
from entities.world_objects.wall_spell_entity import WallSpellEntity
from util.world_util import has_entity


class Wall(Spell):
    cooldown: int = 5
    price: int = 10

    @staticmethod
    def new(author: Player) -> WallSpellEntity:
        if Spell.is_launchable(Wall, author) and author.inventory.get_item_count(ItemType.magical_essence) >= Wall.price:
            author.inventory.remove_item(ItemType.magical_essence, Wall.price)
            if author.entity.facing == Facing.EAST:
                if not has_entity((author.entity.x + author.entity.width + 10, None), (author.entity.x + author.entity.width + 10 + 100, None), author.entity.world):
                    author.cooldowns[Wall] = time.time()
                    wall_entity = WallSpellEntity(0, 0, author.entity.world)
                    wall_entity.x = author.entity.x + author.entity.width + 10
                    return wall_entity
            else:
                if not has_entity((author.entity.x - 100 - 10, None), (author.entity.x - 10, None), author.entity.world):
                    author.cooldowns[Wall] = time.time()
                    wall_entity = WallSpellEntity(0, 0, author.entity.world)
                    wall_entity.x = author.entity.x - wall_entity.width - 10
                    return wall_entity
