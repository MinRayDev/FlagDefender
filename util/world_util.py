from typing import Optional

from core.ingame.item.item_type import ItemType
from core.world import World
from entities.Entity import Entity, EntityType
from util.instance import get_game


def teleport(entity: Entity, world: World, x: int | str = "~") -> None:
    if isinstance(x, str) and x != "~":
        raise ValueError(f"{x} is not a valid target")
    if x < -world.size[0] or x > world.size[0]:
        raise ValueError(f"{x} is not a valid target")
    if world not in get_game().worlds:
        raise ValueError(f"{world} is not a valid target")
    if world != entity.world:
        entity.world.entities.remove(entity)
        entity.world = world
        world.entities.append(entity)
    if x != entity.x and x != "~":
        entity.x = x
        if get_game().main_player.entity == entity:
            get_game().scroll = -x


def kill(entity: Entity) -> None:
    entity.death()


def nearest_entity(entity: Entity, filter_type: EntityType = None) -> Entity:
    nearest: Optional[Entity] = None
    for entity_ in entity.world.entities:
        if entity != entity_:
            if filter_type is not None:
                if entity_.type != filter_type:
                    continue
            if nearest is not None:
                if abs(nearest.x) - abs(entity.x) > abs(entity_.x) - abs(entity.x):
                    nearest = entity_
            else:
                nearest = entity_
    return nearest


def give_item(name: str = None, item_id: int = None, amount: int = None) -> bool:
    if name is None and item_id is None:
        raise ValueError("You must specify either a name or an item id")
    if item_id is not None:
        if ItemType.get_by_id(item_id) is not None:
            get_game().main_player.inventory.add_item(ItemType.get_by_id(item_id), amount)
            return True
        return False
    elif name is not None:
        if ItemType.get_by_name(name) is not None:
            get_game().main_player.inventory.add_item(ItemType.get_by_name(name), amount)
            return True
        return False


def area_contains(first_pos: tuple[int, Optional[int]], second_pos: tuple[int, Optional[int]], entity: Entity) -> bool:
    if first_pos[1] is None or second_pos[1] is None:
        return (first_pos[0] <= entity.x <= second_pos[0]) or (second_pos[0] <= entity.x <= first_pos[0])
    return (first_pos[0] <= entity.x <= second_pos[0] and first_pos[1] <= entity.y <= second_pos[1]) or (
                second_pos[0] <= entity.x <= first_pos[0] and second_pos[1] <= entity.y <= first_pos[1])


def get_entities_in_area(first_pos: tuple[int, Optional[int]], second_pos: tuple[int, Optional[int]], world: World, filter_type: EntityType = None) -> list[Entity]:
    entities: list[Entity] = []
    for entity_ in world.entities:
        if filter_type is not None:
            if entity_.type != filter_type:
                continue
        if area_contains(first_pos, second_pos, entity_):
            entities.append(entity_)
    return entities
