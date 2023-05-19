import os
from time import time

from pygame import Surface
from pygame.event import Event

from util.time_util import has_elapsed
from util.world_util import teleport
from entities.entity import Entity, EntityType, DamageType
from core.world import Facing, World
from util import sprites
from util.input.controls import ControlsEventTypes, Controls
from util.instance import get_game, get_client
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.client import Client


class PlayerEntity(Entity):
    """Class 'PlayerEntity'.

        Extends 'Entity'.
        :ivar client: The client instances.
        :type client: Client
        :ivar speed: The speed of the player.
        :type speed: int
        :ivar i: The current frame of the player.
        :type i: int
        :ivar incline: The incline of the player.
        :type incline: int
        :ivar death_time: The time of death.
        :type death_time: float
        :ivar invincible: Whether the player is invincible or not.
        :type invincible: bool
        :ivar frame: The current frame of the player.
        :type frame: int

    """
    client: 'Client'
    speed: int
    i: int
    incline: int
    death_time: float
    invincible: bool
    frame: int
    is_walking: bool

    def __init__(self, x: int, y: int, world: World, facing: Facing = Facing.EAST):
        """Constructor of the class 'PlayerEntity'.

            :param x: The x position of the player.
            :type x: int.
            :param y: The y position of the player.
            :type y: int.
            :param world: The world instance.
            :type world: World.
            :param facing: The facing of the player.
            :type facing: Facing.

        """
        super().__init__(x, y, sprites_path=os.path.join(r"./resources/sprites/main_player"), facing=facing, world=world, health=100)
        self.client = get_client()
        self.speed = 7
        self.i = 0
        self.to_floor()
        self.gravity_value = 3
        self.incline = 0
        self.type = EntityType.ALLY
        self.death_time = 0
        self.invincible = False
        self.frame = 0
        self.is_walking = False

    def activity(self, keys: list[int], events: list[Event]) -> None:
        """The activity of the player.

            This method is called every tick.

            :param keys: The keys pressed.
            :type keys: list[int].
            :param events: The events.
            :type events: list[Event].

        """
        super().activity()
        if self.death_time + 5 > time():
            return
        self.is_walking = False
        col = self.get_collisions()
        if Controls.left_walk.get_code() in keys:
            self.is_walking = True
            if self.frame < 1 or self.frame > 10:
                self.frame = 1
            if self.x > 0-self.world.size[0] and col[Facing.WEST]:
                self.x -= self.speed
                if get_game().current_level.main_player.entity == self:
                    get_game().current_level.scroll += self.speed
            if self.facing != Facing.WEST:
                self.facing = Facing.WEST

        elif Controls.right_walk.get_code() in keys:
            self.is_walking = True
            if self.frame < 11 or self.frame > 22:
                self.frame = 12
            if self.x < self.world.size[0] - self.width and col[Facing.EAST]:
                self.x += self.speed
                if get_game().current_level.main_player.entity == self:
                    get_game().current_level.scroll -= self.speed
            if self.facing != Facing.EAST:
                self.facing = Facing.EAST

        self.i += 1
        for event in events:
            if Controls.run.get_code() == event.code and event.type == ControlsEventTypes.DOWN:
                self.speed += 5
            if Controls.run.get_code() == event.code and event.type == ControlsEventTypes.UP:
                self.speed -= 5

    def draw(self, surface: Surface) -> None:
        """Draws the player.

            :param surface: The surface to draw on.
            :type surface: Surface.

        """
        if get_game().current_level.main_player.entity != self:
            super().draw(surface)
        else:
            if self.is_walking:
                self.i += 1
                if self.i > 20:
                    self.i = 0
                    self.frame += 1
                    if self.frame == 11:
                        self.frame = 1
                    elif self.frame == 22:
                        self.frame = 12
            else:
                if self.facing == Facing.WEST:
                    self.frame = 0
                elif self.facing == Facing.EAST:
                    self.frame = 11
            surface.blit(self.sprites[str(self.frame)], (surface.get_width()//2 - self.width//2, self.y))

    def death(self) -> None:
        """The death of the player."""
        teleport(self, self.world, 0)
        self.is_walking = False
        self.health = 100
        self.death_time = time()

    def to_json(self) -> dict[str, int | float | Facing | None | str]:
        """Converts the player entity to a json dict.

            :return: The json dict.
            :rtype: dict[str, int | float | Facing | None | str].

        """
        return {"x": self.x, "world": self.world.name, "facing": self.facing, "uuid": str(self.uuid_)}

    @staticmethod
    def from_json(json_dict: dict[str, int | float | Facing | None | str]) -> 'PlayerEntity':
        """Converts a json dict to a player entity.

            :param json_dict: The json dict.
            :type json_dict: dict[str, int | float | Facing | None | str]

            :return: The player entity.
            :rtype: PlayerEntity.

        """
        pe = PlayerEntity(json_dict["x"], json_dict["y"], get_game().current_level.get_world_by_name(json_dict["world"]), json_dict["facing"])
        pe.uuid_ = json_dict["uuid"]
        pe.source = 1
        pe.sprites = sprites.load(os.path.join(r"./resources/sprites/online_player"))
        pe.sprite_selected = list(pe.sprites.values())[0]
        for sprite in pe.sprites:
            if pe.max_height < pe.sprites[sprite].get_height():
                pe.max_height = pe.sprites[sprite].get_height()
            if pe.max_width < pe.sprites[sprite].get_width():
                pe.max_width = pe.sprites[sprite].get_width()
        return pe

    def damage(self, amount: float, damage_type: DamageType, author: Entity = None) -> None:
        """Damages the player."""
        if not self.invincible and has_elapsed(self.death_time, 5):
            super().damage(amount, damage_type, author)
