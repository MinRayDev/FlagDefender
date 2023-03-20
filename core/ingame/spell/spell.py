from typing import Optional

from core.player import Player
from entities.Entity import Entity

class Spell:
    def __init__(self, author: Player):
        self.author: Player = author
        self.entity: Optional[Entity] = None
