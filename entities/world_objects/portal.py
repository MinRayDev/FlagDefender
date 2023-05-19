import time

from pygame import Surface

from core.world import World
from entities.entity import Entity
from entities.livingentities.player_entity import PlayerEntity
from util.audio import play_sound
from util.draw_util import draw_with_scroll
from util.world_util import teleport


class PortalEntity(Entity):
    """Class 'PortalEntity'.

        Extends 'Entity'.
        :ivar linked_x: The x coordinate of the linked portal.
        :type linked_x: int.
        :ivar linked_world: The world of the linked portal.
        :type linked_world: World.
        :ivar players_contained: The players contained in the portal.
        :type players_contained: dict[PlayerEntity, float].
        :ivar tick: The tick of the portal.
        :type tick: int.

    """
    linked_x: int
    linked_world: World
    players_contained: dict[PlayerEntity, float]
    tick: int

    def __init__(self, x: int, linked_x: int, world: World, linked_world: World):
        """Constructor of the class 'PortalEntity'.

            :param x: The x coordinate of the entity.
            :type x: int.
            :param linked_x: The x coordinate of the portal.
            :type linked_x: int.
            :param world: The world the entity is in.
            :type world: World.
            :param linked_world: The world of the portal.
            :type linked_world: World.

        """
        super().__init__(x, 0, r"./resources/sprites/world/portal", world, None)
        self.linked_x = linked_x
        self.linked_world = linked_world
        self.has_gravity = False
        self.has_collisions = False
        self.to_floor()
        self.players_contained: dict[PlayerEntity, float] = {}
        self.tick = 0

    def activity(self) -> None:
        """The activity of the entity."""
        for entity in self.world.entities:
            if self.contact(entity) and isinstance(entity, PlayerEntity) and entity not in self.players_contained:
                self.players_contained[entity] = time.time()
            elif isinstance(entity, PlayerEntity) and not self.contact(entity) and entity in self.players_contained:
                self.players_contained.pop(entity)
            elif entity in self.players_contained and self.players_contained[entity] + 1.5 < time.time():
                teleport(entity, self.linked_world, self.linked_x)
                play_sound("portal.mp3")
                self.players_contained.pop(entity)

    def draw(self, surface: Surface) -> None:
        """Draws the entity on the surface.

            :param surface: The surface to draw on.
            :type surface: Surface.
        """
        if len(self.players_contained) > 0:
            if self.tick <= 15:
                draw_with_scroll(surface, self.sprites["hover_0"], self.x, self.y)
                self.tick += 1
            elif self.tick <= 30:
                draw_with_scroll(surface, self.sprites["hover_1"], self.x, self.y)
                self.tick += 1
                if self.tick > 30:
                    self.tick = 0
        else:
            if self.tick <= 15:
                draw_with_scroll(surface, self.sprites["none_0"], self.x, self.y)
                self.tick += 1
            elif self.tick <= 30:
                draw_with_scroll(surface, self.sprites["none_1"], self.x, self.y)
                self.tick += 1
                if self.tick > 30:
                    self.tick = 0
