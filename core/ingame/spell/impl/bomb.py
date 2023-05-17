import time

from core.ingame.item.item_type import ItemType
from core.ingame.spell.spell import Spell
from core.player import Player
from entities.projectiles.impl.bomb_entity import BombEntity


class Bomb(Spell):
    """Class 'Bomb'.

        Extend `Spell`.
        :cvar cooldown: Spell's cooldown.
        :type cooldown: int.

        :cvar price: Spell's price (Magical Essence).
        :type price: int.

    """
    cooldown: int = 3
    price: int = 15

    @staticmethod
    def new(author: Player) -> BombEntity:
        """Generate new 'BombEntity' spell.

            :param author: Spell's author.
            :type author: Player.

            :return: BombEntity entity.
            :rtype: BombEntity.

        """
        if Spell.is_launchable(Bomb, author) and author.inventory.get_item_count(ItemType.magical_essence) >= Bomb.price:
            author.inventory.remove_item(ItemType.magical_essence, Bomb.price)
            author.cooldowns[Bomb] = time.time()
            return BombEntity(author.entity.x, author.entity.y, author.entity, author.entity.incline)
