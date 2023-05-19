import random
from typing import Optional, TYPE_CHECKING

from pygame import Surface


from core.ingame.item.item_type import ItemType
from core.world import World, Facing
from entities.entity import Entity, EntityType
from util.instance import get_game, get_client
from util.world_util import area_contains, get_entities_in_area, drop, teleport, nearest_entity

if TYPE_CHECKING:
    from core.client import Client


class Mob(Entity):
    """Class 'Mob'.

        Extend 'Entity'.
        This class is the base class for all mobs. It contains all the basic functions and attributes of a mob.

        :ivar client: The client instances.
        :type client: Client.
        :ivar target_range: The range of the mob.
        :type target_range: int.
        :ivar attack_range: The attack range of the mob.
        :type attack_range: int.
        :ivar cooldown: The cooldown of the mob.
        :type cooldown: int.
        :ivar has_collisions: Whether the mob has collisions.
        :type has_collisions: bool.
        :ivar temp_cooldown: The temporary cooldown of the mob.
        :type temp_cooldown: int.
        :ivar type: The type of the mob.
        :type type: EntityType.
        :ivar target: The target of the mob.
        :type target: Optional[Entity].
        :ivar has_ai: Whether the mob has AI.
        :type has_ai: bool.
        :ivar speed: The speed of the mob.
        :type speed: int.
        :ivar can_move: Whether the mob can move.
        :type can_move: bool.
        :ivar distance_damage: Whether the mob can damage from a distance.
        :type distance_damage: bool.
        :ivar can_attack: Whether the mob can attack.
        :type can_attack: bool.

    """
    client: 'Client'
    target_range: int
    attack_range: int
    cooldown: int
    has_collisions: bool
    temp_cooldown: int
    type: EntityType
    target: Optional[Entity] = None
    has_ai: bool
    speed: int
    can_move: bool
    distance_damage: bool
    can_attack: bool

    def __init__(self, x: int, y: int, sprites_path: str, facing: Facing, world: World, health: float):
        """Constructor of the class 'Mob'.

            :param x: The x coordinate of the mob.
            :type x: int.
            :param y: The y coordinate of the mob.
            :type y: int.
            :param sprites_path: The path to the sprites of the mob.
            :type sprites_path: str.
            :param facing: The direction the mob is facing.
            :type facing: Facing.
            :param world: The world the mob is in.
            :type world: World.
            :param health: The health of the mob.
            :type health: float.

        """
        super().__init__(x, y, sprites_path, world, facing, health)
        self.client = get_client()
        self.to_floor()
        self.target_range = 10 * 100
        self.attack_range = 10 * 50 + random.randint(0, 20)
        self.cooldown = 0
        self.has_collisions = False
        self.temp_cooldown = 0
        self.type = EntityType.ENEMY
        self.target = None
        self.has_ai = True
        self.speed = 3
        self.can_move = True
        self.distance_damage = False
        self.can_attack = False

    def activity(self) -> None:
        """The activity of the mob."""
        from entities.world_objects.flag import Flag
        super().activity()
        if self.x < -self.world.size[0] or self.x > self.world.size[0]:
            self.death()
            return
        if self.check_target():
            temp_entity = nearest_entity(self)
            if not isinstance(self.target, Flag) and isinstance(temp_entity, Flag):
                self.target = temp_entity
            if area_contains((self.x - self.attack_range, None), (self.x + self.attack_range + self.width, None), self.target):
                self.can_attack = True
                if self.cooldown <= self.temp_cooldown:
                    self.attack()
                    self.temp_cooldown = 0
                if self.can_move and ((self.randomize_wait() and random.randint(0, 1) == 0) or not self.randomize_wait()) and not self.distance_damage:
                    self.go_to((self.target.x, self.target.y))
                self.temp_cooldown += 1
            else:
                self.go_to((self.target.x, self.target.y))
        else:
            self.find_target()
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

    def randomize_wait(self) -> bool:
        """Randomizes the wait of the mob."""
        return True

    def find_target(self) -> None:
        """Finds a target for the mob."""
        entities = get_entities_in_area((self.x - self.target_range, None), (self.x + self.width + self.target_range, None),
                                        self.world, EntityType.ALLY)
        if len(entities) > 0:
            self.target = random.choice(entities)
            if self.target.x > self.x:
                self.facing = Facing.EAST
            elif self.target.x < self.x:
                self.facing = Facing.WEST

    def check_target(self) -> bool:
        """Checks if the mob has a target."""
        return self.target is not None and area_contains((int(self.x - self.target_range * 1.25), None),
                                                         (int(self.x + self.target_range * 1.25), None), self.target) and self.target in self.world.entities

    def attack(self) -> None:
        """The attack of the mob."""
        pass

    def go_to(self, pos: tuple[int, int]) -> None:
        """Makes the mob go to a position.

            :param pos: The position the mob has to go to.
            :type pos: tuple[int, int].

        """
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

    def death(self) -> None:
        """The death of the mob."""
        self.loot()
        super().death()
        if self in get_game().current_level.round_manager.round_.mobs:
            del get_game().current_level.round_manager.round_.mobs[get_game().current_level.round_manager.round_.mobs.index(self)]

    def loot(self) -> None:
        """The loot of the mob."""
        random_int = random.randint(1, 100)
        if random_int <= 48:
            drop(ItemType.magical_essence, self.x, self.world)
        elif random_int <= 60:
            drop(ItemType.wall, self.x, self.world)
        elif random_int <= 70:
            drop(ItemType.big_wall, self.x, self.world)
        elif random_int <= 78:
            drop(ItemType.turret, self.x, self.world)
        elif random_int <= 85:
            drop(ItemType.tp_all, self.x, self.world)
        elif random_int <= 90:
            drop(ItemType.kill_all, self.x, self.world)

    def get_collisions(self) -> dict[Facing, bool]:
        """Gets the collisions of the mob.

            :return: The collisions of the mob.
            :rtype: dict[Facing, bool].

        """
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
        """Draws the mob.

            :param surface: The surface the mob has to be drawn on.
            :type surface: Surface.

        """
        super().draw(surface)
        self.draw_health_bar(surface)

    def lock(self) -> None:
        """Locks the mob.

            Make the mob unable to move.

        """
        self.can_move = False

    def unlock(self) -> None:
        """Unlocks the mob.

            Make the mob able to move.

        """
        self.can_move = True
