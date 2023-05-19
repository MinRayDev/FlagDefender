from __future__ import annotations

import json
import os
import time
import uuid
import traceback


from util import files
from typing import Optional
from util.menu import add_check
from typing import TYPE_CHECKING
from util.instance import get_game, get_client

if TYPE_CHECKING:
    from core.world import World, Facing
    from entities.entity import Entity
    from core.player import Player
    from core.round_manager import RoundManager


class Level:
    """Class 'Level'.

        :ivar players: Level's players.
        :type players: list[Player].
        :ivar scroll: Current level's scroll.
        :type scroll: int.
        :ivar day_duration: Day's duration.
        :type day_duration: int.
        :ivar day_start: Timestamp at the start of the day.
        :type day_start: float.
        :ivar main_player: Level's main player.
        :type main_player: Optional[Player].
        :ivar skycolor_alpha: Sky's opacity.
        :type skycolor_alpha: int.
        :ivar name: Level's name.
        :type name: str.
        :ivar worlds: Level's worlds.
        :type worlds: list[World].
        :ivar round_manager: Level's round manager.
        :type round_manager: RoundManager.

    """
    players: 'list[Player]'
    scroll: int
    day_duration: int
    day_start: float
    main_player: 'Optional[Player]'
    skycolor_alpha: int
    name: str
    worlds: list[World]
    round_manager: 'RoundManager'

    def __init__(self, name: str, loading: bool = False):
        """Constructor function for Level class.

            :param name: Level's name.
            :type name: str.
            :ivar loading: Player's world.
            :type loading: bool.

        """
        from core.player import Player
        from util.world_util import summon
        from core.world import World, Facing
        from core.round_manager import RoundManager
        from entities.world_objects.flag import Flag
        from entities.world_objects.portal import PortalEntity
        from entities.world_objects.entity_mountain import Mountain
        from core.ingame.backgrounds.hell_background import HellBackground
        from core.ingame.backgrounds.overworld_background import OverworldBackground

        add_check("Creating values.", __name__ + "Level.init")
        self.players = []
        self.scroll = 0
        self.day_duration = 60*10
        self.day_start = 0
        self.skycolor_alpha = 0
        add_check("Creating worlds.", __name__ + "Level.init")
        self.name = name
        self.worlds = [
            World("overworld", 80, (11200, 720)),
            World("left_world", 80, (2048, 720)),
            World("right_world", 80, (2048, 720))
        ]

        add_check("Loading Backgrounds.", __name__ + "Level.init")
        if not loading:
            self.worlds[0].set_background(OverworldBackground(self.worlds[0]))
        self.worlds[1].set_background(HellBackground(self.worlds[1]))
        self.worlds[2].set_background(HellBackground(self.worlds[2]))

        add_check("Creating base entities.", __name__ + "Level.init")
        Mountain(self.worlds[0].size[0] - 30, self.worlds[0], Facing.EAST)
        Mountain(-self.worlds[0].size[0] + 30, self.worlds[0], Facing.WEST)

        PortalEntity(-self.worlds[0].size[0] + 2700, self.worlds[1].size[0] - 700,
                     self.worlds[0],
                     self.worlds[1])
        PortalEntity(self.worlds[1].size[0] - 500, -self.worlds[0].size[0] + 2250,
                     self.worlds[1], self.worlds[0])
        PortalEntity(self.worlds[0].size[0] - 2200, -self.worlds[2].size[0] + 700,
                     self.worlds[0],
                     self.worlds[2])
        PortalEntity(-self.worlds[2].size[0] + 500, self.worlds[0].size[0] - 700,
                     self.worlds[2], self.worlds[0])
        summon(Flag, 0, self.worlds[0])
        add_check("Adding players.", __name__ + "Level.init")
        self.players.append(Player(get_client().controllers[0], self.worlds[0]))
        self.main_player = self.players[0]
        add_check("Round manager initialization.", __name__ + "Level.init")
        self.round_manager: RoundManager = RoundManager(self, not loading)
        add_check("Level initialization finished.", __name__ + "Level.init")

    def get_world_by_name(self, name: str) -> 'World':
        """Get world by its name.

            :param name: World's name.
            :type name: str.

            :return: The world.
            :rtype: World.

        """
        for world in self.worlds:
            if world.name == name:
                return world

    def get_entity_by_uuid(self, uuid_: uuid.UUID) -> 'Entity':
        """Get entity by its uuid.

            :param uuid_: Entity's uuid.
            :type uuid_: uuid.UUID.

            :return: The Entity.
            :rtype: Entity.

        """
        for world in self.worlds:
            for entity in world.entities:
                if entity.uuid_ == uuid_:
                    return entity

    def is_morning(self) -> bool:
        """Check if it's morning.

            :return: True if it is else False.
            :rtype: bool.

        """
        return time.time() <= self.day_start + self.day_duration / 2

    def is_afternoon(self) -> bool:
        """Check if it's afternoon.

            :return: True if it is else False.
            :rtype: bool.

        """
        return self.day_start + self.day_duration / 2 < time.time() <= self.day_start + self.day_duration

    def is_past_midnight(self) -> bool:
        """Check if it's after midnight.

            :return: True if it is else False.
            :rtype: bool.

        """
        return self.day_start + self.day_duration * 1.25 < time.time() <= self.day_start + self.day_duration * 1.5

    def is_day(self) -> bool:
        """Check if it's day.

            :return: True if it is else False.
            :rtype: bool.

        """
        return self.is_morning() or self.is_afternoon()

    def is_night(self):
        """Check if it's nightS.

            :return: True if it is else False.
            :rtype: bool.

        """
        return self.day_start + self.day_duration < time.time() <= self.day_start + self.day_duration * 1.5

    def game_over(self) -> None:
        """Game's end function.

            Save the score, and start the game over menu.

        """
        from ui.impl.game_over import GameOverMenu
        datas = files.get_datas()
        score: int = self.main_player.kills + self.round_manager.round_.number * 4
        datas["scores"].append({"score": score, "time": time.time()})
        files.write_datas(datas)
        get_game().instance.set_menu(GameOverMenu(self.main_player.kills, self.round_manager.round_.number))

    def save(self) -> None:
        """Saves the level.

            Saves players, worlds, entities, round.

        """
        players = {}
        for player in self.players:
            players[str(player.user_id)] = player.to_json()
        worlds = {}
        for world in self.worlds:
            worlds[world.name] = world.to_json()
        x = {
            "players": players,
            "worlds": worlds,
            "round": {"number": self.round_manager.round_.number, "start_time": self.round_manager.round_.start_time},
            "delta_time": time.time()-self.day_start
        }
        path = os.path.join(files.get_save_path(), self.name + ".json")
        file = open(path, "w+", encoding="utf-8")
        file.write(json.dumps(x))
        file.close()

    @staticmethod
    def load(name: str, json_fp: str) -> Level:
        """Load a level from a json file.

            :param name: Level's name.
            :type name: str.
            :param json_fp: Json File path.
            :type json_fp: str

            :return: The level.
            :rtype: Level.

        """
        try:
            from util.menu import add_check
            from core.player import Player
            from core.round_manager import Round
            from entities.livingentities.mob import Mob
            add_check("Creating new level.", __name__ + ".load", 1)
            level = Level(name, True)
            add_check("Opening saved level.", __name__ + ".load", 1)
            json_dict = json.load(open(json_fp, "r"))

            add_check("Loading players.", __name__ + ".load", 1)
            level.round_manager.round_ = Round(json_dict["round"]["number"])
            for player in json_dict["players"]:
                Player.from_json(level, json_dict, player)
            add_check("Loading worlds.", __name__ + ".load", 1)
            for world_name in json_dict["worlds"]:
                world = level.get_world_by_name(world_name)
                for entity in json_dict["worlds"][world_name]["entities"]:
                    module = __import__('.'.join(entity["entity_type"].split(".")[:-1]), globals(), locals(), entity["entity_type"].split(".")[-1])
                    class_ = getattr(module, entity["entity_type"].split(".")[-1])
                    from entities.item import ItemEntity
                    if issubclass(class_, Mob):
                        entity_ = class_(entity["x"], entity["y"], world, entity["facing"])
                        entity_.health = entity["health"]
                    elif issubclass(class_, ItemEntity):
                        from core.ingame.item.item_type import ItemType
                        item = ItemType.get_by_id(entity["item_id"])
                        entity_ = class_(entity["x"], item.get_sprite_path(), world, item)
                    else:
                        entity_ = class_(entity["x"], entity["y"], world)
                        entity_.health = entity["health"]
                    entity_.uuid_ = uuid.UUID(str(entity["uuid"]))
                    level.round_manager.round_.mobs.append(entity_)
                if world_name == "overworld":
                    from core.ingame.backgrounds.overworld_background import OverworldBackground
                    world.set_background(OverworldBackground.from_json(json_dict, level))
            level.day_start = time.time()-json_dict["delta_time"]
            add_check("Loading is complete", __name__ + ".load", 1)
            level.round_manager.start()
            return level
        except:
            traceback.print_exc()
