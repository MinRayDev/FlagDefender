from __future__ import annotations

from util.world_util import teleport
from core.ingame.spell.spell import Spell
from core.player import Player
from entities.Item import ItemEntity


class TpItems(Spell):
    def __init__(self, author: Player):
        super().__init__(author)
        for entity in author.entity.world.entities:
            if isinstance(entity, ItemEntity):
                teleport(entity, author.entity.world, author.entity.x)

    @staticmethod
    def new(author: Player) -> TpItems:
        return TpItems(author)
