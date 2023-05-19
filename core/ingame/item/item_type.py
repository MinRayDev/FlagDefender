from __future__ import annotations

import enum
from typing import Optional, Callable, Generator, Any
from pygame import Surface

from core.ingame.item.item import ItemUsage
from util.sprites import load


class ItemType(enum.Enum):
    """Class representing different types of items.

        Extend `Enum`. An item is defined by its id, sprites_path, stack_limit, name and its usage.

    """
    magical_essence = {"id": 0, "sprites_path": r"./resources/sprites/items/magical_essence", "stack_limit": 128, "name": "MagicalEssence", "usage": None}
    wall = {"id": 2, "sprites_path": r"./resources/sprites/items/wall", "stack_limit": 16, "name": "Wall", "usage": ItemUsage.wall_use}
    big_wall = {"id": 3, "sprites_path": r"./resources/sprites/items/big_wall", "stack_limit": 16, "name": "BigWall", "usage": ItemUsage.big_wall_use}
    turret = {"id": 4, "sprites_path": r"./resources/sprites/items/turret", "stack_limit": 16, "name": "Turret", "usage": ItemUsage.turret_use}
    kill_all = {"id": 5, "sprites_path": r"./resources/sprites/items/kill_all", "stack_limit": 16, "name": "KillAll", "usage": ItemUsage.kill_all}
    tp_all = {"id": 6, "sprites_path": r"./resources/sprites/items/tp_all", "stack_limit": 16, "name": "TpAll", "usage": ItemUsage.tp_all}

    def get_sprites(self) -> dict[str, Surface]:
        """Loads item's sprites.

            :return: Dict of sprites associated with their names.
            :rtype: dict[str, Surface].

        """
        return load(self.value["sprites_path"])

    def get_sprite(self) -> Surface:
        """Loads item's sprite.

            :return: Sprite.
            :rtype: Surface.

        """
        return list(self.get_sprites().values())[0]

    def get_id(self) -> int:
        """Get- item's id.

            :return: Item's id.
            :rtype: int.

        """
        return self.value["id"]

    def get_sprite_path(self) -> str:
        """Get item's sprites path.

            :return: Item's sprites path.
            :rtype: str.

        """
        return self.value["sprites_path"]

    def get_stack_limit(self) -> int:
        """Get item's sprites path.

            :return: Item's stack limit.
            :rtype: int.

        """
        return self.value["stack_limit"]

    def get_name(self) -> str:
        """Get item's name.

            :return: Item's name.
            :rtype: str.

        """
        return self.value["name"]

    def has_usage(self) -> bool:
        """Check if item has usage.

            :return: True if item has usage else False.
            :rtype: bool.

        """
        return self.value["usage"] is not None

    def get_usage(self) -> Optional[Callable]:
        """Get item usage.

            :return: Item usage class and function.
            :rtype: str.

        """
        if self.value["usage"] is not None:
            return self.value["usage"]

    @staticmethod
    def get_names() -> Generator[str, Any, None]:
        """Get items names."""
        for item in ItemType:
            yield item.get_name()

    @staticmethod
    def get_by_name(name: str) -> Optional[ItemType]:
        """Get item by its name.

            :param name: Item's name.
            :type name: str.

            :return: Item if 'name' exists else None
            :rtype: Optional[ItemType]

        """
        for item in ItemType:
            if item.get_name() == name:
                return item

    @staticmethod
    def get_by_id(item_id: int) -> Optional[ItemType]:
        """Get item by its id.

            :param item_id: Item's id.
            :type item_id: int.

            :return: Item if 'item_id' exists else None
            :rtype: Optional[ItemType]

        """
        for item in ItemType:
            if item.get_id() == item_id:
                return item

    @staticmethod
    def get_name_start(start_name: str, index: int) -> Optional[str]:
        """Get items names by their starts.

            :param start_name: Start of the name researched.
            :type start_name: str.

            :param index: Tab index.
            :type index: int.

            :return: Item if 'start_name' exists else None
            :rtype: Optional[str]

        """
        i = 0
        for name in ItemType.get_names():
            if name.lower().startswith(start_name):
                if index == i:
                    return name
                i += 1
