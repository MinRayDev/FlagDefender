import time

import pygame
from catppuccin import Flavour
from pygame import Surface

from core.chat.chat import entity_register
from core.world import World
from entities.entity import Entity, EntityType
from util.colors import Colors
from util.instance import get_game


@entity_register
class WallSpellEntity(Entity):
    """Class 'WallSpellEntity'.

        Extends 'Entity'.
        :ivar creation_time: The time the entity was created.
        :type creation_time: float.

    """
    creation_time: float

    def __init__(self, x: int, y: int, world: World):
        """Constructor of the class 'WallSpellEntity'.

            :param x: The x coordinate of the entity.
            :type x: int.
            :param y: The y coordinate of the entity.
            :type y: int.
            :param world: The world the entity is in.
            :type world: World.

        """
        super().__init__(x, y, r"./resources/sprites/spells/wall", world, health=400)
        self.to_floor()
        self.creation_time = time.time()
        self.has_gravity = False
        self.type = EntityType.ALLY

    def draw(self, surface: Surface) -> None:
        """Draws the entity on the surface.

            :param surface: The surface to draw on.
            :type surface: Surface.

        """
        super().draw(surface)
        self.draw_health_bar(surface)
        x: int = self.x - 4 + surface.get_width() // 2 + get_game().current_level.scroll - get_game().current_level.main_player.entity.width // 2
        y: int = self.y - 27
        width: int = self.width + 8
        pygame.draw.rect(surface, Flavour.frappe().green.rgb, pygame.Rect(x, y, width, 8))
        percentage = (time.time() - self.creation_time) / 20
        pygame.draw.rect(surface, Colors.surface2, pygame.Rect(width + x - int(width * percentage), y, int(width * percentage), 8))

    def activity(self) -> None:
        """The activity of the entity."""
        super().activity()
        if time.time() > self.creation_time + 10:
            self.death()
