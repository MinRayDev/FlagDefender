from core.ingame.spell.spell import Spell
from core.player import Player
from entities.Entity import EntityType


class KillAll(Spell):
    def __init__(self, author: Player):
        super().__init__(author)
        for entity in author.entity.world.entities.copy():
            if entity.type == EntityType.ENEMY:
                entity.death()
