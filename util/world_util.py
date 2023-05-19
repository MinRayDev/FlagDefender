from typing import Optional, TYPE_CHECKING


from core.world import World
from entities.entity import Entity, EntityType
from entities.item import ItemEntity
from util.instance import get_game

if TYPE_CHECKING:
    from core.level import Level
    from entities.livingentities.mob import Mob
    from core.ingame.item.item_type import ItemType


def teleport(entity: Entity, world: World, x: int | str = "~") -> None:
    """Teleports the entity to the given world and x position.

        :param entity: The entity to teleport.
        :type entity: Entity.
        :param world: The world to teleport the entity to.
        :type world: World.
        :param x: The x position to teleport the entity to.
        :type x: int | str.

    """
    if isinstance(x, str) and x != "~":
        raise ValueError(f"{x} is not a valid target")
    if x < -world.size[0] or x > world.size[0]:
        raise ValueError(f"{x} is not a valid target")
    if world not in get_game().current_level.worlds:
        raise ValueError(f"{world} is not a valid target")
    if world != entity.world:
        entity.world.entities.remove(entity)
        entity.world = world
        world.entities.append(entity)
    if x != entity.x and x != "~":
        entity.x = x
        if get_game().current_level.main_player.entity == entity:
            get_game().current_level.scroll = -x


def teleport_level(level: 'Level', entity: Entity, world: World, x: int | str = "~") -> None:
    """Teleports the entity to the given world and x position.

        :param level: The level of the entity.
        :type level: Level.
        :param entity: The entity to teleport.
        :type entity: Entity.
        :param world: The world to teleport to.
        :type world: World.
        :param x: The x position to teleport to.
        :type x: int | str.

    """
    if isinstance(x, str) and x != "~":
        raise ValueError(f"{x} is not a valid target")
    if x < -world.size[0] or x > world.size[0]:
        raise ValueError(f"{x} is not a valid target")
    if world not in level.worlds:
        raise ValueError(f"{world} is not a valid target")
    if world != entity.world:
        entity.world.entities.remove(entity)
        entity.world = world
        world.entities.append(entity)
    if x != entity.x and x != "~":
        entity.x = x
        if level.main_player.entity == entity:
            level.scroll = -x


def kill(entity: Entity) -> None:
    """Kills the entity.

        :param entity: The entity to kill.
        :type entity: Entity.

    """
    entity.death()


def nearest_entity(center: Entity, filter_type: EntityType = None) -> Optional[Entity]:
    """Returns the nearest entity to the center entity.

        :param center: The center entity.
        :type center: Entity.
        :param filter_type: The type of the entity to filter.
        :type filter_type: EntityType.

        :return: The nearest entity to the center entity.
        :rtype: Optional[Entity].

    """
    nearest: Optional[Entity] = None
    last_distance: int = center.world.size[0] * 2

    for entity in center.world.entities:
        if entity == center:
            continue
        if filter_type is not None and entity.type != filter_type:
            continue
        if nearest is None:
            nearest = entity
            continue

        dist: int = center.distance_to(entity)
        if dist < last_distance:
            nearest = entity
            last_distance = dist

    return nearest


def give_item(name: str = None, item_id: int = None, amount: int = None) -> bool:
    """ Gives the player an item.

        :param name: The name of the item.
        :type name: str.
        :param item_id: The id of the item.
        :type item_id: int.
        :param amount: The amount of the item.
        :type amount: int.

        :return: True if the item was given, False if not.
        :rtype: bool.

    """
    from core.ingame.item.item_type import ItemType
    if name is None and item_id is None:
        raise ValueError("You must specify either a name or an item id.")
    if item_id is not None:
        if ItemType.get_by_id(item_id) is not None:
            get_game().current_level.main_player.inventory.add_item(ItemType.get_by_id(item_id), amount)
            return True
        return False
    elif name is not None:
        if ItemType.get_by_name(name) is not None:
            get_game().current_level.main_player.inventory.add_item(ItemType.get_by_name(name), amount)
            return True
        return False


def area_contains(first_pos: tuple[int, Optional[int]], second_pos: tuple[int, Optional[int]], entity: Entity) -> bool:
    """Checks if an area contains an entity.

        If the y value of either position is None, the y value of the entity will be ignored.

        :param first_pos: The first position of the area.
        :type first_pos: tuple[int, Optional[int]].
        :param second_pos: The second position of the area.
        :type second_pos: tuple[int, Optional[int]].
        :param entity: The entity to check for.
        :type entity: Entity.

        :return: Whether the area contains the entity.
        :rtype: bool.

    """
    if first_pos[1] is None or second_pos[1] is None:
        return (first_pos[0] <= entity.x <= second_pos[0]) or (second_pos[0] <= entity.x <= first_pos[0]) or (
                    first_pos[0] <= entity.x + entity.width <= second_pos[0]) or (
                    second_pos[0] <= entity.x + entity.width <= first_pos[0])
    return (first_pos[0] <= entity.x <= second_pos[0] and first_pos[1] <= entity.y <= second_pos[1]) or (
            second_pos[0] <= entity.x <= first_pos[0] and second_pos[1] <= entity.y <= first_pos[1])


def get_entities_in_area(first_pos: tuple[int, Optional[int]], second_pos: tuple[int, Optional[int]], world: World, filter_type: EntityType = None) -> list[Entity]:
    """Gets all entities in an area.

        :param first_pos: The first position of the area.
        :type first_pos: tuple[int, Optional[int]].
        :param second_pos: The second position of the area.
        :type second_pos: tuple[int, Optional[int]].
        :param world: The world to check in.
        :type world: World.
        :param filter_type: The type of entity to check for.
        :type filter_type: EntityType.

        :return: A list of entities in the area.
        :rtype: list[Entity].

    """
    entities: list[Entity] = []
    for entity_ in world.entities:
        if filter_type is not None:
            if entity_.type != filter_type:
                continue
        if area_contains(first_pos, second_pos, entity_):
            entities.append(entity_)
    return entities


def has_entity(first_pos: tuple[int, Optional[int]], second_pos: tuple[int, Optional[int]], world: World, filter_type: EntityType = None) -> bool:
    """Checks if an entity is in an area.

        :param first_pos: The first position of the area.
        :type first_pos: tuple[int, Optional[int]].
        :param second_pos: The second position of the area.
        :type second_pos: tuple[int, Optional[int]].
        :param world: The world to check in.
        :type world: World.
        :param filter_type: The type of entity to check for.
        :type filter_type: EntityType.

        :return: Whether an entity is in the area.
        :rtype: bool.

    """
    return len(get_entities_in_area(first_pos, second_pos, world, filter_type)) > 0


def summon(entity_type: type[Entity], x: int, world: World) -> Entity:
    """Summons an entity.

        :param entity_type: The type of entity to summon.
        :type entity_type: type[Entity].
        :param x: The x position to summon the entity at.
        :type x: int.
        :param world: The world to summon the entity in.

        :return: The entity that was summoned.
        :rtype: Entity.

    """
    if issubclass(entity_type, Entity) and entity_type != Entity:
        return entity_type(x, 0, world)


def summon_mob(entity_type: 'type[Mob]', x: int, world: World) -> 'Mob':
    """Summons a mob.

        :param entity_type: The type of mob to summon.
        :type entity_type: type[Mob].
        :param x: The x position to summon the mob at.
        :type x: int.
        :param world: The world to summon the mob in.
        :type world: World.

        :return: The mob that was summoned.
        :rtype: Mob.

    """
    from entities.livingentities.mob import Mob
    if issubclass(entity_type, Mob) and entity_type != Mob:
        return entity_type(x, 0, world)


def drop(item: 'ItemType', x: int, world: World) -> ItemEntity:
    """Drops an item on the ground.

        :param item: The item to drop.
        :type item: ItemType.
        :param x: The x position to drop the item at.
        :type x: int.
        :param world: The world to drop the item in.
        :type world: World.

        :return: The item entity that was dropped.
        :rtype: ItemEntity.
    """
    return ItemEntity(x, item.get_sprite_path(), world, item)
