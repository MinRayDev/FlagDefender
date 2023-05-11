from pygame import Surface

from core.chat.chat import MessageType
from entities.entity import Entity, EntityType
from entities.livingentities.mob import Mob
from util.instance import get_game
from util.world_util import nearest_entity, area_contains


class Flag(Entity):
    def __init__(self, x, y, world):
        super().__init__(x, y, r"./resources/sprites/world/flag", world, health=1000)
        self.to_floor()
        self.type = EntityType.ALLY
        self.has_collisions = False
        self.is_attacked = False

    def draw(self, surface: Surface) -> None:
        super().draw(surface)
        self.draw_health_bar(surface)

    def activity(self):
        super().activity()
        nentity = nearest_entity(self)
        if isinstance(nentity, Mob) and area_contains((self.x - 500, None), (self.x + self.width + 500, None), nentity):
            if not self.is_attacked:
                get_game().chat.write("Your flag is under attack.", MessageType.GAME)
                self.is_attacked = True
        else:
            self.is_attacked = False

    def death(self):
        get_game().current_level.game_over()
