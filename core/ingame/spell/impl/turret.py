import time

from core.ingame.item.item_type import ItemType
from core.ingame.spell.spell import Spell
from core.player import Player
from core.world import Facing
from entities.world_objects.turret_spell_entity import TurretSpellEntity
from util.world_util import has_entity


class Turret(Spell):
    """Class 'Turret'.

        Extend `Spell`.
        :cvar cooldown: Spell's cooldown.
        :type cooldown: int.

        :cvar price: Spell's price (Magical Essence).
        :type price: int.

    """
    cooldown: int = 5
    price: int = 10

    @staticmethod
    def new(author: Player) -> TurretSpellEntity:
        """Generate new 'TurretSpellEntity' spell.

            :param author: Spell's author.
            :type author: Player.

            :return: TurretSpellEntity entity.
            :rtype: TurretSpellEntity.

        """
        if Spell.is_launchable(Turret, author) and author.inventory.get_item_count(ItemType.magical_essence) >= Turret.price:
            author.inventory.remove_item(ItemType.magical_essence, Turret.price)
            if author.entity.facing == Facing.EAST:
                if not has_entity((author.entity.x + author.entity.width + 10, None), (author.entity.x + author.entity.width + 10 + 100, None), author.entity.world):
                    author.cooldowns[Turret] = time.time()
                    turret_entity = TurretSpellEntity(0, 0, author.entity.world)
                    turret_entity.x = author.entity.x + author.entity.width + 10
                    return turret_entity
            else:
                if not has_entity((author.entity.x - 100 - 10, None), (author.entity.x - 10, None), author.entity.world):
                    author.cooldowns[Turret] = time.time()
                    turret_entity = TurretSpellEntity(0, 0, author.entity.world)
                    turret_entity.x = author.entity.x - turret_entity.width - 10
                    return turret_entity
