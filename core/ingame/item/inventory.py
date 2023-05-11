from core.ingame.item.item_type import ItemType


class Inventory:
    content: dict[ItemType, int]

    def __init__(self):
        self.content = {}

    def __len__(self) -> int:
        return len(self.content.keys())

    def add_item(self, item: ItemType, count: int) -> bool:
        if self.can_add_item(item, count):
            if self.has_item(item):
                self.content[item] = self.content[item] + count
            else:
                self.content[item] = count
            return True
        else:
            return False

    def remove_item(self, item: ItemType, count: int) -> None:
        if self.has_item(item):
            self.content[item] = self.content[item] - count
        if self.get_item_count(item) == 0:
            self.content.pop(item)

    def has_item(self, item_type: ItemType) -> bool:
        for item in self.content.keys():
            if item == item_type:
                return True
        return False

    def get_item_count(self, item_type: ItemType) -> int:
        for item in self.content.keys():
            if item == item_type:
                return self.content[item]
        return 0

    def get_index(self, index: int) -> ItemType:
        return list(self.content.keys())[index]

    def can_add_item(self, item: ItemType, count: int) -> bool:
        return self.get_item_count(item) + count <= item.get_stack_limit()

    def clear(self) -> None:
        self.content.clear()

    def to_json(self) -> dict[int, int]:
        json: dict[int, int] = {}
        for item in self.content:
            json[item.get_id()] = self.content[item]
        return json

