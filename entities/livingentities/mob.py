import enum
import random
from typing import Optional

from core.world import World, Facing
from entities.Entity import Entity, EntityType
from util.world_util import nearest_entity, area_contains, get_entities_in_area


class Mob(Entity):
    target: Optional[Entity] = None

    def __init__(self, x: int, y: int, sprites_path: str, facing, world: World, health: float):
        super().__init__(x, y, sprites_path, world, facing, health)
        self.target_range = 10 * 100
        self.attack_range = 10 * 50
        self.cooldown = 0
        self.temp_cooldown = 0
        self.target = None
        self.has_ai = True
        self.speed = 3
        self.distance_damage = False

    def activity(self, **kwargs):
        super().activity()
        if self.check_target():
            if area_contains((self.x - self.attack_range, None), (self.x + self.attack_range, None), self.target):
                if self.cooldown <= self.temp_cooldown:
                    self.attack()
                    self.temp_cooldown = 0
                if random.randint(0, 1) == 0 and not self.distance_damage:
                    self.go_to((self.target.x, self.target.y))
                self.temp_cooldown += 1
            else:
                self.go_to((self.target.x, self.target.y))
        else:
            self.get_target()
            if self.check_target():
                self.go_to((0, 0))
        # if no target go mid
        # while range attack < pos -> goto target else attack // si range target < pos -> goto mid
        return

    def get_target(self):
        entities = get_entities_in_area((self.x - self.target_range, None), (self.x + self.target_range, None),
                                        self.world, EntityType.ALLY)
        if len(entities) > 0:
            self.target = random.choice(entities)

    def check_target(self):
        return self.target is not None and area_contains((int(self.x - self.target_range * 1.25), None),
                                                         (int(self.x + self.target_range * 1.25), None), self.target)

    def attack(self):
        pass

    def go_to(self, pos: tuple[int, int]):
        if self.has_ai:
            col = self.get_collisions()
            if self.x != pos[0]:
                if self.x > pos[0] and col[Facing.WEST]:
                    if col[Facing.WEST]:
                        self.x -= self.speed
                        self.facing = Facing.WEST
                elif self.x < pos[0] and col[Facing.EAST]:
                    self.x += self.speed
                    self.facing = Facing.EAST
