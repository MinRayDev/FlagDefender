import time

from core.ingame.spell.spell import Spell
from core.player import Player
from entities.projectiles.impl.fireball import Fireball
from util import audio


class FireBallSpell(Spell):
    """Class 'FireBallSpell'.

        Extend `Spell`.
        :cvar cooldown: Spell's cooldown.
        :type cooldown: int.

    """
    cooldown: int = 0.2

    @staticmethod
    def new(author: Player) -> Fireball:
        """Generate new 'Fireball' spell.

            :param author: Spell's author.
            :type author: Player.

            :return: Fireball entity.
            :rtype: Fireball.

        """
        if Spell.is_launchable(FireBallSpell, author):
            author.cooldowns[FireBallSpell] = time.time()
            fireball_entity = Fireball(author.entity.x, author.entity.y, author.entity)
            audio.play_sound("small_fireball.mp3")
            return fireball_entity
