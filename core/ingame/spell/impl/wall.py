from core.ingame.spell.spell import Spell
from core.player import Player
from core.world import Facing
from entities.world_objects.wall_spell_entity import WallEntity


class Wall(Spell):
    def __init__(self, author: Player):
        super().__init__(author)
        self.entity: WallEntity = WallEntity(0, 0, author.entity.world)
        match author.entity.facing:
            case Facing.EAST:
                self.entity.x = author.entity.x + author.entity.width + 10
            case Facing.WEST:
                self.entity.x = author.entity.x - self.entity.width - 10
