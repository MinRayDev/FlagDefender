from pygame import Surface

from core.chat.chat import MessageType
from core.world import World
from entities.entity import Entity, EntityType
from entities.livingentities.mob import Mob
from util.instance import get_game
from util.world_util import nearest_entity, area_contains


class Flag(Entity):
    """Class 'Flag'.

        Extends 'Entity'.
        :ivar is_attacked: Whether the flag is under attack.
        :type is_attacked: bool.

    """
    is_attacked: bool

    def __init__(self, x: int, y: int, world: World):
        """Constructor of the class 'Flag'.

            :param x: The x coordinate of the entity.
            :type x: int.
            :param y: The y coordinate of the entity.
            :type y: int.
            :param world: The world the entity is in.
            :type world: World.

        """
        super().__init__(x, y, r"./resources/sprites/world/flag", world, health=1000)
        self.to_floor()
        self.type = EntityType.ALLY
        self.has_collisions = False
        self.is_attacked = False

    def draw(self, surface: Surface) -> None:
        """Draws the entity on the surface.

            :param surface: The surface to draw on.
            :type surface: Surface.

        """
        super().draw(surface)
        self.draw_health_bar(surface)

    def activity(self) -> None:
        """The activity of the entity."""
        super().activity()
        nentity = nearest_entity(self)
        if isinstance(nentity, Mob) and area_contains((self.x - 500, None), (self.x + self.width + 500, None), nentity):
            if not self.is_attacked:
                get_game().chat.write("Your flag is under attack.", MessageType.GAME)
                self.is_attacked = True
        else:
            self.is_attacked = False
