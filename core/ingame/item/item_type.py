from __future__ import annotations

import enum
from typing import Optional, Callable
from pygame import Surface

from util.sprites import load

# TODO: damage bombe player, bug traget mob fly2  bug attack mobfly1 target mob speed
class ItemType(enum.Enum):
    magical_essence = {"id": 0, "sprites_path": r"./resources/sprites/items/magical_essence", "stack_limit": 128, "name": "MagicalEssence", "usage": None}
    wall = {"id": 2, "sprites_path": r"./resources/sprites/items/wall", "stack_limit": 16, "name": "Wall", "usage": "ItemUsage.wall_use"}
    big_wall = {"id": 3, "sprites_path": r"./resources/sprites/items/big_wall", "stack_limit": 16, "name": "BigWall", "usage": "ItemUsage.big_wall_use"}
    turret = {"id": 4, "sprites_path": r"./resources/sprites/items/turret", "stack_limit": 16, "name": "Turret", "usage": "ItemUsage.turret_use"}
    kill_all = {"id": 5, "sprites_path": r"./resources/sprites/items/kill_all", "stack_limit": 16, "name": "KillAll", "usage": "ItemUsage.kill_all"}
    tp_all = {"id": 6, "sprites_path": r"./resources/sprites/items/tp_all", "stack_limit": 16, "name": "TpAll", "usage": "ItemUsage.tp_all"}
    arrow = {"id": 7, "sprites_path": r"./resources/sprites/items/arrow", "stack_limit": 16, "name": "Arrow", "usage": None}

    def get_sprites(self) -> dict[str, Surface]:
        return load(self.value["sprites_path"])

    def get_sprite(self):
        return list(self.get_sprites().values())[0]

    def get_id(self) -> int:
        return self.value["id"]

    def get_sprite_path(self) -> str:
        return self.value["sprites_path"]

    def get_stack_limit(self) -> int:
        return self.value["stack_limit"]

    def get_name(self) -> str:
        return self.value["name"]

    def has_usage(self) -> bool:
        return self.value["usage"] is not None

    def get_usage(self) -> Optional[str]:
        if self.value["usage"] is not None:
            return self.value["usage"]

    @staticmethod
    def get_names() -> list[str]:
        for item in ItemType:
            yield item.get_name()

    @staticmethod
    def get_by_name(name: str) -> Optional[ItemType]:
        for item in ItemType:
            if item.get_name() == name:
                return item

    @staticmethod
    def get_by_id(item_id: int) -> Optional[ItemType]:
        for item in ItemType:
            print(item.get_id(), item_id)
            print(item.get_id(), item_id)
            if item.get_id() == item_id:
                print("aaaa")
                return item

    @staticmethod
    def get_name_start(start_name: str, index: int) -> str:
        i = 0
        for name in ItemType.get_names():
            if name.lower().startswith(start_name):
                if index == i:
                    return name
                i += 1