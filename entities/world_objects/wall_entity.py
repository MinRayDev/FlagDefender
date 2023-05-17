from __future__ import annotations

import time

from pygame import Surface

from core.chat.chat import entity_register
from core.player import Player
from core.world import Facing
from entities.entity import Entity, EntityType
from util.draw_util import draw_with_scroll
from util.world_util import get_entities_in_area


@entity_register
class WallEntity(Entity):
    def __init__(self, x, y, world):
        super().__init__(x, y, r"./resources/sprites/build/wall", world, health=400)
        self.to_floor()
        self.creation_time = time.time()
        self.has_gravity = False
        self.type = EntityType.ALLY

    def draw(self, surface: Surface) -> None:
        draw_with_scroll(surface, self.sprite_selected, self.x, self.y)
        self.draw_health_bar(surface)

    def activity(self):
        super().activity()

    @staticmethod
    def new(author: Player) -> WallEntity:
        match author.entity.facing:
            case Facing.EAST:
                if len(get_entities_in_area((author.entity.x + author.entity.width + 10, None),
                                            (author.entity.x + author.entity.width + 10 + 100, None),
                                            author.entity.world)) == 0:
                    return WallEntity(author.entity.x + author.entity.width + 10, 0, author.entity.world)
            case Facing.WEST:
                if len(get_entities_in_area((author.entity.x - 100 - 10, None),
                                            (author.entity.x - 10, None),
                                            author.entity.world)) == 0:
                    return WallEntity(author.entity.x - 96 - 10, 0, author.entity.world)
