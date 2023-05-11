from __future__ import annotations

import time

from core.ingame.spell.spell import Spell
from core.player import Player
from entities.projectiles.impl.big_fireball import BigFireball
from util import audio


class BigFireBallSpell(Spell):
    cooldown: int = 0.5

    @staticmethod
    def new(author: Player) -> BigFireball:
        if Spell.is_launchable(BigFireBallSpell, author):
            author.cooldowns[BigFireBallSpell] = time.time()
            fireball_entity = BigFireball(author.entity.x, author.entity.y, author.entity)
            audio.play_song("large_fireball.mp3")
            return fireball_entity
