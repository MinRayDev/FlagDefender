from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.ingame.item.item_type import ItemType


class Inventory:
    """Class 'Inventory'.

        :ivar content: Content in the inventory.
        :type content: dict[ItemType, int].

    """
    content: dict['ItemType', int]

    def __init__(self):
        """Constructor function for Inventory class."""
        self.content = {}

    def __len__(self) -> int:
        return len(self.content.keys())

    def add_item(self, item: 'ItemType', count: int = 1) -> bool:
        """Add item in the inventory.

            :param item: Item to add.
            :type item: ItemType.
            :param count: Number of items to add.
            :type count: int.

            :return: True if it could add in the inventory otherwise false.
            :rtype: bool.

        """
        if self.can_add_item(item, count):
            if self.has_item(item):
                self.content[item] = self.content[item] + count
            else:
                self.content[item] = count
            return True
        else:
            return False

    def remove_item(self, item: 'ItemType', count: int) -> None:
        """Remove item in the inventory.

            :param item: Item to remove.
            :type item: ItemType.
            :param count: Number of items to remove.
            :type count: int.

        """
        if self.has_item(item):
            self.content[item] = self.content[item] - count
        if self.get_item_count(item) == 0:
            self.content.pop(item)

    def has_item(self, item_type: 'ItemType') -> bool:
        """Check if inventory has item_type.

            :param item_type: Item to check.
            :type item_type: ItemType.

            :return: True if inventory has item_type else False.
            :rtype: bool.

        """
        for item in self.content.keys():
            if item == item_type:
                return True
        return False

    def get_item_count(self, item_type: 'ItemType') -> int:
        """Get number of item_type.

            :param item_type: Item to check.
            :type item_type: ItemType.

            :return: Number of item_type in the inventory.
            :rtype: int.

        """
        for item in self.content.keys():
            if item == item_type:
                return self.content[item]
        return 0

    def get_index(self, index: int) -> 'ItemType':
        """Get 'ItemType' by 'index'.

            :param index: Index to get.
            :type index: int.

            :return: The 'ItemType' at the 'index'.
            :rtype: ItemType.

        """
        return list(self.content.keys())[index]

    def can_add_item(self, item: 'ItemType', count: int) -> bool:
        """Check if an item can be added in the inventory.

            :param item: ItemType to check.
            :type item: ItemType.
            :param count: INumber of items to check.
            :type count: int.

            :return: The 'ItemType' at the 'index'.
            :rtype: ItemType.

        """
        return self.get_item_count(item) + count <= item.get_stack_limit()

    def clear(self) -> None:
        self.content.clear()

    def to_json(self) -> dict[int, int]:
        """Convert this object to json format.

            :return: Json dictionnary.
            :rtype: dict[int, int].

        """
        json: dict[int, int] = {}
        for item in self.content:
            json[item.get_id()] = self.content[item]
        return json

