from core.world import Facing
from entities.entity import EntityType
from entities.item import ItemEntity
from entities.world_objects.big_wall_entity import BigWallEntity
from entities.world_objects.turret_entity import TurretEntity
from entities.world_objects.wall_entity import WallEntity
from util.instance import get_game
from util.world_util import get_entities_in_area, teleport


class ItemUsage:
    """Class 'Inventory'.

        In this class there is all usage of items.

    """

    @staticmethod
    def wall_use() -> WallEntity:
        """Usage of wall item, summon a wall and return it.

            :return: Wall Entity.
            :rtype: WallEntity.

        """
        author = get_game().current_level.main_player
        match author.entity.facing:
            case Facing.EAST:
                if len(get_entities_in_area((author.entity.x + author.entity.width + 10, None),
                                            (author.entity.x + author.entity.width + 10 + 100, None),
                                            author.entity.world)) == 0:
                    wall_entity = WallEntity(0, 0, author.entity.world)
                    wall_entity.x = author.entity.x + author.entity.width + 10
                    return wall_entity
            case Facing.WEST:
                if len(get_entities_in_area((author.entity.x - 100 - 10, None),
                                            (author.entity.x - 10, None),
                                            author.entity.world)) == 0:
                    wall_entity = WallEntity(0, 0, author.entity.world)
                    wall_entity.x = author.entity.x - wall_entity.width - 10
                    return wall_entity

    @staticmethod
    def big_wall_use() -> BigWallEntity:
        """Usage of big wall item, summon a big wall and return it.

            :return: Big Wall Entity.
            :rtype: BigWallEntity.

        """
        author = get_game().current_level.main_player
        match author.entity.facing:
            case Facing.EAST:
                if len(get_entities_in_area((author.entity.x + author.entity.width + 10, None),
                                            (author.entity.x + author.entity.width + 10 + 100, None),
                                            author.entity.world)) == 0:
                    big_wall_entity: BigWallEntity = BigWallEntity(0, 0, author.entity.world)
                    big_wall_entity.x = author.entity.x + author.entity.width + 10
                    return big_wall_entity
            case Facing.WEST:
                if len(get_entities_in_area((author.entity.x - 100 - 10, None),
                                            (author.entity.x - 10, None),
                                            author.entity.world)) == 0:
                    big_wall_entity = BigWallEntity(0, 0, author.entity.world)
                    big_wall_entity.x = author.entity.x - big_wall_entity.width - 10
                    return big_wall_entity

    @staticmethod
    def turret_use() -> TurretEntity:
        """Usage of turret item, summon a turret and return it.

            :return: Turret Entity.
            :rtype: TurretEntity.

        """
        author = get_game().current_level.main_player
        match author.entity.facing:
            case Facing.EAST:
                if len(get_entities_in_area((author.entity.x + author.entity.width + 10, None),
                                            (author.entity.x + author.entity.width + 10 + 100, None),
                                            author.entity.world)) == 0:
                    turret_entity = TurretEntity(0, 0, author.entity.world)
                    turret_entity.x = author.entity.x + author.entity.width + 10
                    return turret_entity
            case Facing.WEST:
                if len(get_entities_in_area((author.entity.x - 100 - 10, None),
                                            (author.entity.x - 10, None),
                                            author.entity.world)) == 0:
                    turret_entity = TurretEntity(0, 0, author.entity.world)
                    turret_entity.x = author.entity.x - turret_entity.width - 10
                    return turret_entity

    @staticmethod
    def kill_all() -> bool:
        """Usage of kill all item.

            Kill all mobs in author's world.

            :rtype: bool.

        """
        author = get_game().current_level.main_player
        for entity in author.entity.world.entities.copy():
            if entity.type == EntityType.ENEMY:
                entity.death()
        return True

    @staticmethod
    def tp_all() -> bool:
        """Usage of tp all item.

            Tp all items in author's world at author's location.

            :rtype: bool.

        """
        author = get_game().current_level.main_player
        for entity in author.entity.world.entities:
            if isinstance(entity, ItemEntity):
                teleport(entity, author.entity.world, author.entity.x)
        return True
