from __future__ import annotations

import time

from core.ingame.item.item_type import ItemType
from core.ingame.spell.spell import Spell
from core.player import Player
from entities.projectiles.impl.bomb_entity import BombEntity


class Bomb(Spell):
    cooldown: int = 3
    price: int = 15

    def __init__(self, author: Player):
        super().__init__(author)
        self.entity: BombEntity = BombEntity(author.entity.x, author.entity.y, author.entity, author.entity.incline)

    @staticmethod
    def new(author: Player) -> BombEntity:
        if Spell.is_launchable(Bomb, author) and author.inventory.get_item_count(ItemType.magical_essence) >= Bomb.price:
            author.inventory.remove_item(ItemType.magical_essence, Bomb.price)
            author.cooldowns[Bomb] = time.time()
            return BombEntity(author.entity.x, author.entity.y, author.entity, author.entity.incline)
