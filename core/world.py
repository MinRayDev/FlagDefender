import enum
import traceback
from typing import Tuple


class Facing(enum.IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class World:
    def __init__(self, name, floor: int, size: Tuple[int, int]):
        self.name = name
        self.background = None
        self.entities = []
        self.floor = floor
        self.size = size

    def has_player(self) -> bool:
        from entities.livingentities.entity_player import PlayerEntity
        for entity in self.entities:
            if isinstance(entity, PlayerEntity):
                return True
        return False

    def set_background(self, background):
        self.background = background

    def to_json(self) -> dict:
        world = {"entities": []}
        from entities.entity import Entity
        entity: Entity
        for entity in self.entities:
            from entities.livingentities.entity_player import PlayerEntity
            from entities.projectiles.projectile import Projectile
            from entities.world_objects.entity_mountain import Mountain
            from entities.world_objects.flag import Flag
            from entities.world_objects.portal import PortalEntity
            if not isinstance(entity, PlayerEntity) and not isinstance(entity, Projectile) and not isinstance(entity, Mountain) and not isinstance(entity, Flag) and not isinstance(entity, PortalEntity):
                world["entities"].append(entity.to_json())
        from core.ui.impl.ingame_menu.backgrounds.overworld_background import OverworldBackground
        if isinstance(self.background, OverworldBackground):
            try:
                world["background"] = self.background.to_json()
            except:
                traceback.print_exc()
        return world
