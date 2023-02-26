from core.world import Facing
from util.world_util import teleport
from core.ingame.spell.spell import Spell
from core.player import Player
from entities.Item import ItemEntity


class NearTp(Spell):
    def __init__(self, author: Player):
        super().__init__(author)
        if author.entity.facing == Facing.EAST:
            teleport(author.entity, author.entity.world, author.entity.x + author.entity.width*1.5)
        elif author.entity.facing == Facing.WEST:
            teleport(author.entity, author.entity.world, author.entity.x - author.entity.width*1.5)