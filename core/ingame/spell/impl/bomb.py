from core.ingame.spell.spell import Spell
from core.player import Player
from entities.projectiles.impl.bomb_entity import BombEntity


class Bomb(Spell):
    def __init__(self, author: Player):
        super().__init__(author)
        self.entity: BombEntity = BombEntity(author.entity.x, author.entity.y, author.entity)
