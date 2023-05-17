import enum
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from entities.entity import Entity
    from core.ingame.background import Background


class Facing(enum.IntEnum):
    """Class representing different facings.

        Extend `IntEnum`.
        :cvar NORTH: NORTH facing (up).
        :cvar EAST: EAST facing (right).
        :cvar SOUTH: SOUTH facing (down).
        :cvar WEST: WEST facing (left).

    """
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class World:
    """Class 'World'.

        :ivar name: World's name.
        :type name: str.
        :ivar background: World's background.
        :type background: Optional[Background].
        :ivar entities: List of all entities in the world.
        :type entities: list[Entity].
        :ivar floor: World's floor size.
        :type floor: int.
        :ivar size: World's size (width, height).
        :type size: tuple[int, int].

    """
    name: str
    background: 'Optional[Background]'
    entities: 'list[Entity]'
    floor: int
    size: tuple[int, int]

    def __init__(self, name: str, floor: int, size: tuple[int, int]):
        """Constructor function for World class.

            :param name: World's name.
            :type name: str.
            :param floor: World's floor size.
            :type floor: int.
            :param size: World's size (width, height).
            :type size: tuple[int, int].

        """
        self.name = name
        self.background = None
        self.entities = []
        self.floor = floor
        self.size = size

    def has_player(self) -> bool:
        """Checks if this world contains at least one player.

            :return: True if this world contains a player else False.
            :rtype: bool.

        """
        from entities.livingentities.entity_player import PlayerEntity
        for entity in self.entities:
            if isinstance(entity, PlayerEntity):
                return True
        return False

    def set_background(self, background: 'Background') -> None:
        """Change the background of the world by 'background'.

            :param background: Background to set.
            :type: Background.

        """
        self.background = background

    def to_json(self) -> dict[str, list | dict[str, list[list[str]] | dict]]:
        """Convert this object to json format.

            :return: Json dictionnary.
            :rtype: dict[str, list | dict[str, list[list[str]] | dict]].

        """
        world = {"entities": []}
        from entities.entity import Entity
        from entities.livingentities.entity_player import PlayerEntity
        from entities.projectiles.projectile import Projectile
        from entities.world_objects.entity_mountain import Mountain
        from entities.world_objects.flag import Flag
        from entities.world_objects.portal import PortalEntity
        entity: Entity
        for entity in self.entities:
            if not isinstance(entity, PlayerEntity) and not isinstance(entity, Projectile) and not isinstance(entity, Mountain) and not isinstance(entity, Flag) and not isinstance(entity, PortalEntity):
                world["entities"].append(entity.to_json())
        from core.ingame.backgrounds.overworld_background import OverworldBackground
        if isinstance(self.background, OverworldBackground):
            world["background"] = self.background.to_json()
        return world
