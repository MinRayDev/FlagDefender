import enum
from typing import Optional, Callable


from util.sprites import load


class ItemType(enum.Enum):
    gold = {"id": 0, "sprites_path": r"./resources/sprites/items/gold", "stack_limit": 16, "name": "Gold", "is_bindable": False, "usage": None}
    # magic_essence = {"id": 1, "sprites_path": "", "stack_limit": 16, "name": "Magic_Essence"}
    wall_spell = {"id": 2, "sprites_path": r"./resources/sprites/items/wall", "stack_limit": 16, "name": "Wall_Spell", "is_bindable": True, "usage": "Wall.new"}
    turret_spell = {"id": 3, "sprites_path": r"./resources/sprites/items/turret", "stack_limit": 16, "name": "Turret_Spell", "is_bindable": True, "usage": "Turret.new"}
    sword = {"id": 100, "sprites_path": r"./resources/sprites/items/test", "stack_limit": 1, "name": "Sword", "is_bindable": False, "usage": None}
    
    def get_sprites(self):
        return load(self.value["sprites_path"])

    def get_sprite(self):
        return list(self.get_sprites().values())[0]

    def get_id(self):
        return self.value["id"]

    def get_sprite_path(self):
        return self.value["sprites_path"]

    def get_stack_limit(self):
        return self.value["stack_limit"]

    def get_name(self):
        return self.value["name"]

    def is_bindable(self):
        return self.value["is_bindable"]

    def has_usage(self):
        return self.value["usage"] is not None

    def get_usage(self) -> Optional[str]:
        if self.value["usage"] is not None:
            return self.value["usage"]

    @staticmethod
    def get_names():
        for item in ItemType:
            yield item.get_name()

    @staticmethod
    def get_by_name(name: str):
        for item in ItemType:
            if item.get_name() == name:
                return item

    @staticmethod
    def get_by_id(item_id: int):
        for item in ItemType:
            if item.get_id() == item_id:
                return item

    @staticmethod
    def get_name_start(start_name: str, index: int) -> str:
        i = 0
        for name in ItemType.get_names():
            if name.startswith(start_name):
                if index == i:
                    return name
                i += 1
