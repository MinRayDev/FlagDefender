from __future__ import annotations

import time

from core.ingame.spell.spell import Spell
from core.player import Player
from entities.projectiles.impl.arrow import Arrow
from util import audio


class ArrowSpell(Spell):
    cooldown: int = 0.4

    @staticmethod
    def new(author: Player) -> Arrow:
        if Spell.is_launchable(ArrowSpell, author):
            author.cooldowns[ArrowSpell] = time.time()
            fireball_entity = Arrow(author.entity.x, author.entity.y, author.entity)
            audio.play_song("arrow_shoot.mp3")
            return fireball_entity
