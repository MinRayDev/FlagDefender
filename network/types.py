import enum

from entities.livingentities.entity_player import PlayerEntity
from entities.projectiles.impl.fireball import Fireball


class NetworkEntityTypes(enum.Enum):
    PLAYER = {"value": 0, "class": PlayerEntity}
    FIREBALL = {"value": 1, "class": Fireball}

    def get_json(self):
        return self.value

    def get_value(self):
        return self.value["value"]

    def get_class(self):
        return self.value["class"]

    @staticmethod
    def from_json(value):
        for entity_type in NetworkEntityTypes:
            if entity_type.get_value() == value:
                return entity_type

    @staticmethod
    def from_class(class_):
        for entity_type in NetworkEntityTypes:
            if entity_type.get_class() == class_.__class__:
                return entity_type
