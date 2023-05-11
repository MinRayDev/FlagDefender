import random
from typing import Optional

from pygame import Surface

from core.ingame.item.item_type import ItemType
from core.world import World, Facing
from entities.entity import Entity, EntityType
from util.instance import get_game
from util.world_util import area_contains, get_entities_in_area, drop, teleport


class Mob(Entity):
    target: Optional[Entity] = None

    def __init__(self, x: int, y: int, sprites_path: str, facing, world: World, health: float):
        from util.instance import get_client
        super().__init__(x, y, sprites_path, world, facing, health)
        self.client = get_client()
        self.to_floor()
        self.target_range = 10 * 100
        self.attack_range = 10 * 50 + random.randint(0, 20)
        self.cooldown = 0
        self.temp_cooldown = 0
        self.type = EntityType.ENEMY
        self.target = None
        self.has_ai = True
        self.speed = 3
        self.distance_damage = False
        self.can_attack = False

    def activity(self):
        super().activity()
        if self.check_target():
            if area_contains((self.x - self.attack_range, None), (self.x + self.attack_range + self.width, None), self.target):
                self.can_attack = True
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
            if not self.check_target():
                if self.world.name == "overworld":
                    self.go_to((0, 0))
                elif self.world.name == "right_world":
                    self.go_to((-2048, 0))
                elif self.world.name == "left_world":
                    self.go_to((2048, 0))
        if self.world.name == "right_world" and self.x <= -1850:
            teleport(self, get_game().current_level.get_world_by_name("overworld"), get_game().current_level.get_world_by_name("overworld") .size[0]-700)
        elif self.world.name == "left_world" and self.x >= 1850:
            teleport(self, get_game().current_level.get_world_by_name("overworld"), -get_game().current_level.get_world_by_name("overworld").size[0]+2250)

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

    def death(self):
        self.loot()
        super().death()
        if self in get_game().current_level.round_manager.round.mobs:
            del get_game().current_level.round_manager.round.mobs[get_game().current_level.round_manager.round.mobs.index(self)]

    def loot(self):
        random_int = random.randint(1, 100)
        if random_int <= 40:
            drop(ItemType.magical_essence, self.x, self.world)
        elif random_int <= 55:
            drop(ItemType.wall, self.x, self.world)
        elif random_int <= 65:
            drop(ItemType.big_wall, self.x, self.world)
        elif random_int <= 72:
            drop(ItemType.turret, self.x, self.world)
        elif random_int <= 75:
            drop(ItemType.tp_all, self.x, self.world)
        elif random_int <= 77:
            drop(ItemType.kill_all, self.x, self.world)

    def get_collisions(self):
        col = {Facing.NORTH: True, Facing.EAST: True, Facing.SOUTH: True, Facing.WEST: True}
        if self.has_collisions:
            for entity in self.world.entities:
                if entity.type != EntityType.ENEMY:
                    if self != entity and entity.has_collisions:
                        if entity.x < self.x <= entity.x + entity.width and (
                                (entity.x <= self.y <= entity.x + entity.height) or (
                                entity.x <= self.y + self.height <= entity.x + entity.height)):
                            col[Facing.WEST] = False
                        if entity.x <= self.x + self.width < entity.x + entity.width and (
                                (entity.x <= self.y <= entity.x + entity.height) or (
                                entity.x <= self.y + self.height <= entity.x + entity.height)):
                            col[Facing.EAST] = False
                        if entity.x <= self.y <= entity.x + entity.height and (
                                (entity.x <= self.x <= entity.x + entity.width) or (
                                entity.x <= self.x + self.width <= entity.x + entity.width)):
                            col[Facing.NORTH] = False
                        if entity.x <= self.y + self.height <= entity.x + entity.height and (
                                (entity.x <= self.x <= entity.x + entity.width) or (
                                entity.x <= self.x + self.width <= entity.x + entity.width)):
                            col[Facing.SOUTH] = False
        return col

    def draw(self, surface: Surface) -> None:
        super().draw(surface)
        self.draw_health_bar(surface)
