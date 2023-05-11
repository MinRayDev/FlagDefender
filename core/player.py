from __future__ import annotations

import uuid

import pygame

from core.ingame.item.inventory import Inventory
from core.ingame.item.item_type import ItemType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.level import Level
from core.world import Facing
from entities.entity import DamageType, EntityType
from entities.livingentities.entity_player import PlayerEntity
from util import world_util
from util.input.controls import ControlsEventTypes, Controls
from util.instance import get_game
from util.time_util import has_elapsed
from util.world_util import teleport, teleport_level


class Player:
    def __init__(self, controller, world):
        from util.instance import get_client
        self.client = get_client()
        self.entity = PlayerEntity(0, 0, world)
        self.controller = controller
        self.keys = []
        self.events = []
        self.inventory: Inventory = Inventory()
        self.inventory.add_item(ItemType.magical_essence, 32)
        self.kills = 0
        self.user_id = get_client().datas["user_id"]
        self.cooldowns = {}
        self.death = 0

    def get_controls(self, events):
        for control in self.controller.get_active_controls(pygame.key.get_pressed()):
            if control not in self.keys:
                self.keys.append(control)
        for event in self.controller.get_event_controls(events):
            if event not in self.events:
                self.events.append(event)

    def reset_queues(self):
        self.keys = []
        self.events = []

    def get_event(self, code, type_):
        for event in self.events:
            if event.code == code and event.type == type_:
                return True
        return False

    def get_inventory(self) -> Inventory:
        return self.inventory

    def activity(self):
        from core.ingame.spell.impl.bomb import Bomb
        from core.ingame.spell.impl.turret import Turret
        from core.ingame.spell.impl.wall import Wall
        from core.ingame.spell.impl.big_fireball_spell import BigFireBallSpell
        from core.ingame.spell.impl.fireball_spell import FireBallSpell
        from core.ui.impl.ingame_menu.chat import ChatMenu
        from core.ui.impl.ingame_menu.inventory import InventoryMenu
        from core.ui.impl.ingame_menu.esc_menu import EscMenu
        from core.ingame.spell.impl.arrow_spell import ArrowSpell
        if self.get_event(Controls.esc.get_code(), ControlsEventTypes.DOWN) and get_game().current_menu is None:
            get_game().set_menu(EscMenu())
        if self.get_event(Controls.return_.get_code(), ControlsEventTypes.DOWN) and get_game().current_menu is None:
            get_game().set_menu(ChatMenu())
        if self.get_event(Controls.inventory.get_code(), ControlsEventTypes.DOWN) and get_game().current_menu is None:
            get_game().set_menu(InventoryMenu())
        if has_elapsed(self.entity.death_time, 5):
            if self.get_event(Controls.attack_1.get_code(), ControlsEventTypes.DOWN):
                FireBallSpell.new(self)
            if self.get_event(Controls.attack_2.get_code(), ControlsEventTypes.DOWN):

                ArrowSpell.new(self)
            if self.get_event(Controls.attack_3.get_code(), ControlsEventTypes.DOWN):
                BigFireBallSpell.new(self)
            if self.get_event(Controls.incline_up.get_code(), ControlsEventTypes.DOWN) and self.entity.incline < 10:
                self.entity.incline += 1
            if self.get_event(Controls.incline_down.get_code(), ControlsEventTypes.DOWN) and self.entity.incline > -15:
                self.entity.incline -= 1
            if self.get_event(Controls.spell_1.get_code(), ControlsEventTypes.DOWN):
                Wall.new(self)
            if self.get_event(Controls.spell_2.get_code(), ControlsEventTypes.DOWN):
                Turret.new(self)
            if self.get_event(Controls.spell_3.get_code(), ControlsEventTypes.DOWN):
                Bomb.new(self)
            if self.get_event(Controls.attack_4.get_code(), ControlsEventTypes.DOWN):
                to_attack = world_util.nearest_entity(self.entity, EntityType.ENEMY)
                if to_attack is not None:
                    if self.entity.facing == Facing.EAST and self.entity.x + 150 >= to_attack.x >= self.entity.x:
                        to_attack.damage(25, DamageType.PHYSICAL, self.entity)
                    elif self.entity.facing == Facing.WEST and self.entity.x - 150 <= to_attack.x <= self.entity.x:
                        to_attack.damage(25, DamageType.PHYSICAL, self.entity)

    @staticmethod
    def get_by_entity(entity: PlayerEntity) -> Player:
        for player in get_game().current_level.players:
            if player.entity == entity:
                return player

    def to_json(self) -> dict:
        return {"entity": self.entity.to_json(), "inventory": self.inventory.to_json(), "user_id": str(self.user_id), "kills": self.kills}

    @staticmethod
    def from_json(level: Level, json_dict: dict, player_uuid: str) -> None:
        player: Player = level.main_player
        player.user_id = uuid.UUID(json_dict["players"][player_uuid]["user_id"])
        player.kills = json_dict["players"][player_uuid]["kills"]
        player.inventory.clear()
        for item_id in json_dict["players"][player_uuid]["inventory"]:
            player.inventory.add_item(ItemType.get_by_id(int(item_id)), json_dict["players"][player_uuid]["inventory"][item_id])
        teleport_level(level, player.entity, level.get_world_by_name(json_dict["players"][player_uuid]["entity"]["world"]), json_dict["players"][player_uuid]["entity"]["x"])
        player.entity.facing = json_dict["players"][player_uuid]["entity"]["facing"]
        player.entity.uuid = uuid.UUID(json_dict["players"][player_uuid]["entity"]["uuid"]).hex
