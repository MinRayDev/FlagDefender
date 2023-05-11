from __future__ import annotations

import json
import os
import time
import uuid
from typing import Optional
from typing import TYPE_CHECKING
from uuid import UUID

from util import files
from util.instance import get_game

if TYPE_CHECKING:
    from core.world import World, Facing
    from entities.entity import Entity


class Level:
    def __init__(self, name: str, loading: bool = False):
        from util.instance import get_client
        from core.player import Player
        from core.ingame.backgrounds.hell_background import HellBackground
        from core.ingame.backgrounds.overworld_background import OverworldBackground
        from core.world import World, Facing
        from entities.world_objects.flag import Flag
        from util.world_util import summon
        from core.round_manager import RoundManager
        from entities.world_objects.entity_mountain import Mountain
        from entities.world_objects.portal import PortalEntity
        from util.menu import add_check
        add_check("Creating values.", __name__ + "Level.init")
        self.players: list[Player] = []
        self.scroll: int = 0
        self.day_duration = 60*10
        self.day_start = 0
        self.main_player: Optional[Player] = None
        self.skycolor_alpha = 0
        add_check("Creating worlds.", __name__ + "Level.init")
        overworld = World("overworld", 80, (11200, 720))
        self.name = name
        self.worlds: list[World] = [overworld, World("left_world", 80, (2048, 720)),
                                    World("right_world", 80, (2048, 720))]
        self.actual_world: World = self.worlds[0]

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

    def get_world_by_name(self, name: str) -> 'World':
        for world in self.worlds:
            if world.name == name:
                return world

    def get_entity_by_uuid(self, uuid_: UUID) -> 'Entity':
        for world in self.worlds:
            for entity in world.entities:
                if entity.uuid == uuid_:
                    return entity

    def is_morning(self) -> bool:

        return time.time() <= self.day_start + self.day_duration / 2

    def is_afternoon(self) -> bool:
        return self.day_start + self.day_duration / 2 < time.time() <= self.day_start + self.day_duration

    def is_past_midnight(self) -> bool:
        return self.day_start + self.day_duration * 1.25 < time.time() <= self.day_start + self.day_duration * 1.5

    def is_day(self) -> bool:
        return self.is_morning() or self.is_afternoon()

    def is_night(self):
        return self.day_start + self.day_duration < time.time() <= self.day_start + self.day_duration * 1.5

    @staticmethod
    def load_from_save(save: str):
        pass

    def game_over(self):
        from core.ui.impl.game_over import GameOverMenu
        datas = files.get_datas()
        score: int = self.main_player.kills + self.round_manager.round.number*4
        datas["scores"].append({"score": score, "time": time.time()})
        files.write_datas(datas)
        get_game().instance.set_menu(GameOverMenu(self.main_player.kills, self.round_manager.round.number))

    def save(self) -> None:
        players = {}
        for player in self.players:
            players[str(player.user_id)] = player.to_json()
        worlds = {}
        for world in self.worlds:
            worlds[world.name] = world.to_json()
        x = {
            "players": players,
            "worlds": worlds,
            "round": {"number": self.round_manager.round.number, "start_time": self.round_manager.round.start_time},
            "delta_time": time.time()-self.day_start
        }
        path = os.path.join(files.get_save_path(), self.name + ".json")
        file = open(path, "w+", encoding="utf-8")
        file.write(json.dumps(x))
        file.close()

    @staticmethod
    def load(name: str, json_fp: str) -> Level:
        from util.menu import add_check
        from core.player import Player
        from core.round_manager import Round
        from entities.livingentities.mob import Mob
        add_check("Creating new level.", __name__ + ".load", 1)
        level = Level(name, True)
        add_check("Opening saved level.", __name__ + ".load", 1)
        json_dict = json.load(open(json_fp, "r"))

        add_check("Loading players.", __name__ + ".load", 1)
        level.round_manager.round = Round(json_dict["round"]["number"])
        for player in json_dict["players"]:
            Player.from_json(level, json_dict, player)
        add_check("Loading worlds.", __name__ + ".load", 1)
        for world_name in json_dict["worlds"]:
            world = level.get_world_by_name(world_name)
            # world.entities.clear()
            for entity in json_dict["worlds"][world_name]["entities"]:
                module = __import__('.'.join(entity["entity_type"].split(".")[:-1]), globals(), locals(), entity["entity_type"].split(".")[-1])
                # print(module)
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
                entity_.uuid = uuid.UUID(str(entity["uuid"]))
                level.round_manager.round.mobs.append(entity_)
            if world_name == "overworld":
                from core.ingame.backgrounds.overworld_background import OverworldBackground
                world.set_background(OverworldBackground.from_json(json_dict, level))
        level.day_start = time.time()-json_dict["delta_time"]
        add_check("Loading is complete", __name__ + ".load", 1)
        level.round_manager.start()
        return level
