from typing import Optional, TYPE_CHECKING

from core.world import World, Facing
from util.instance import get_client

if TYPE_CHECKING:
    from entities.entity import Entity

class Object:
    """Class 'Object' is the base class for all objects in the game.

        :ivar x: The x position of the object.
        :type x: int.
        :ivar y: The y position of the object.
        :type y: int.
        :ivar world: The world the object is in.
        :type world: World.
        :ivar width: The width of the object.
        :type width: int.
        :ivar height: The height of the object.
        :type height: int.
        :ivar has_collisions: Whether the object has collisions or not.
        :type has_collisions: bool.

    """
    x: int
    y: int
    world: Optional[World]
    width: int
    height: int
    has_collisions: bool

    def __init__(self, x: int, y: int, world: Optional[World], width: int, height: int):
        """Constructor for class 'Object'.

            :param x: The x position of the object.
            :type x: int.
            :param y: The y position of the object.
            :type y: int.
            :param world: The world the object is in.
            :type world: World.
            :param width: The width of the object.
            :type width: int.
            :param height: The height of the object.
            :type height: int.

        """
        self.x = x
        self.y = y
        self.world = world
        self.width = width
        self.height = height
        self.has_collisions = True

    def get_collisions(self) -> dict[Facing, bool]:
        """Returns a dictionary of the collisions of the object.

            :return: A dictionary of the collisions of the object.
            :rtype: dict[Facing, bool].

        """
        col: dict[Facing, bool] = {Facing.NORTH: True, Facing.EAST: True, Facing.SOUTH: True, Facing.WEST: True}
        if self.has_collisions:
            for entity in self.world.entities:
                if self != entity and entity.has_collisions:
                    if entity.x < self.x <= entity.x + entity.width and (
                            (entity.y <= self.y <= entity.y + entity.height) or (
                            entity.y <= self.y + self.height <= entity.y + entity.height)):
                        col[Facing.WEST] = False
                    if entity.x <= self.x + self.width < entity.x + entity.width and (
                            (entity.y <= self.y <= entity.y + entity.height) or (
                            entity.y <= self.y + self.height <= entity.y + entity.height)):
                        col[Facing.EAST] = False
                    if entity.y <= self.y <= entity.y + entity.height and (
                            (entity.x <= self.x <= entity.x + entity.width) or (
                            entity.x <= self.x + self.width <= entity.x + entity.width)):
                        col[Facing.NORTH] = False
                    if entity.y <= self.y + self.height <= entity.y + entity.height and (
                            (entity.x <= self.x <= entity.x + entity.width) or (
                            entity.x <= self.x + self.width <= entity.x + entity.width)):
                        col[Facing.SOUTH] = False
        return col

    def activity(self) -> None:
        """Activity of the object."""
        pass

    def contact(self, entity: 'Entity') -> bool:
        """Returns whether the object is in contact with the entity or not.

            :param entity: The entity to check contact with.
            :type entity: Entity.

            :return: Whether the object is in contact with the entity or not.
            :rtype: bool.

        """
        return (
                (entity.x <= self.x <= entity.x + entity.width) or
                (entity.x <= self.x + self.width <= entity.x + entity.width)
        ) and \
            (
                    (entity.y <= self.y <= entity.y + entity.height) or
                    (entity.y <= self.y + self.height <= entity.y + entity.height)
             )

    def to_floor(self) -> None:
        """Sets the object to the floor."""
        self.y = get_client().get_screen().get_height() - self.world.floor - self.height
