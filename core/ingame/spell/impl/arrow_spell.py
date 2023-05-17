import time

from core.ingame.spell.spell import Spell
from core.player import Player
from entities.projectiles.impl.arrow import Arrow
from util import audio


class ArrowSpell(Spell):
    """Class 'ArrowSpell'.

        Extend `Spell`.
        :cvar cooldown: Spell's cooldown.
        :type cooldown: int.

    """
    cooldown: int = 0.4

    @staticmethod
    def new(author: Player) -> Arrow:
        """Generate new 'Arrow' spell.

            :param author: Spell's author.
            :type author: Player.

            :return: Arrow entity.
            :rtype: Arrow.

        """
        if Spell.is_launchable(ArrowSpell, author):
            author.cooldowns[ArrowSpell] = time.time()
            fireball_entity = Arrow(author.entity.x, author.entity.y, author.entity)
            audio.play_sound("arrow_shoot.mp3")
            return fireball_entity
