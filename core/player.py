from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

import pygame
from pygame.event import Event

from core.ingame.item.inventory import Inventory
from core.ingame.item.item_type import ItemType

from entities.livingentities.entity_player import PlayerEntity

from util.input.controls import ControlsEventTypes, Controls
from util.instance import get_game, get_client
from util.time_util import has_elapsed
from util.world_util import teleport_level
if TYPE_CHECKING:
    from core.client import Client
    from core.level import Level
    from util.input.controllers import Controller
    from core.world import World, Facing


class Player:
    """Class 'Player'.

        :ivar client: Client.
        :type client: Client.
        :ivar entity: Player's entity.
        :type entity: PlayerEntity.
        :ivar controller: Player's controller.
        :type controller: Controller.
        :ivar inventory: Player's inventory.
        :type inventory: Inventory.
        :ivar kills: Player's kills.
        :type kills: int.
        :ivar user_id: Player's user_id.
        :type user_id: str.
        :ivar cooldowns: Player's spells cooldowns.
        :type cooldowns: dict[object, float].
        :ivar death: Player's death count.
        :type death: int.
        :ivar keys: Player's keys queue.
        :type keys: list[int].

    """
    client: 'Client'
    entity: PlayerEntity
    controller: 'Controller'
    inventory: Inventory
    kills: int
    user_id: str
    cooldowns: dict[object, float]
    death: int
    keys: list[int]
    events: list[Event]

    def __init__(self, controller: 'Controller', world: 'World'):
        """Constructor function for Player class.

            :param controller: Player's controller.
            :type controller: Controller.
            :ivar world: Player's world.
            :type world: World.

        """
        self.client = get_client()
        self.entity = PlayerEntity(0, 0, world)
        self.controller = controller
        self.inventory = Inventory()
        self.inventory.add_item(ItemType.magical_essence, 32)
        self.kills = 0
        self.user_id = self.client.datas["user_id"]
        self.cooldowns = {}
        self.death = 0

        self.keys = []
        self.events = []

    def get_controls(self, events: list[Event]) -> None:
        """Load controls from pygame's events.

            :param events: Pygame's events.
            :type events: list[Event]

        """
        for control in self.controller.get_active_controls(pygame.key.get_pressed()):
            if control not in self.keys:
                self.keys.append(control)
        for event in self.controller.get_event_controls(events):
            if event not in self.events:
                self.events.append(event)

    def reset_queues(self) -> None:
        """Reset events and keys queue."""
        self.keys.clear()
        self.events.clear()

    def get_event(self, code: int, type_: ControlsEventTypes) -> bool:
        """Check if code is in player's event.

            :param code: Code to check.
            :type code: int.
            :param type_: Event type.
            :type type_: ControlsEventTypes.

            :return: True if code is in events else False.
            :rtype: bool.

        """
        for event in self.events:
            if event.code == code and event.type == type_:
                return True
        return False

    def get_inventory(self) -> Inventory:
        """Get player's inventory.

            :return: Player's inventory.
            :rtype: Inventory.

        """
        return self.inventory

    def activity(self) -> None:
        """Does player's activity."""
        from core.ingame.spell.impl.bomb import Bomb
        from core.ingame.spell.impl.turret import Turret
        from core.ingame.spell.impl.wall import Wall
        from core.ingame.spell.impl.big_fireball_spell import BigFireBallSpell
        from core.ingame.spell.impl.fireball_spell import FireBallSpell
        from ui.impl.ingame_menu.chat import ChatMenu
        from ui.impl.ingame_menu.inventory import InventoryMenu
        from ui.impl.ingame_menu.esc_menu import EscMenu
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

    @staticmethod
    def get_by_entity(entity: PlayerEntity) -> Player:
        """Get player by its entity.

            :param entity: Player's entity.
            :type entity: PlayerEntity.
            :return: the Player.
            :rtype: Player.

        """
        for player in get_game().current_level.players:
            if player.entity == entity:
                return player

    def to_json(self) -> dict[str, int | dict[int, int] | str | dict[str, int | float | Facing | None | str]]:
        """Convert this object to json format.

            :return: Json dictionnary.
            :rtype: dict[str, int | dict[int, int] | str | dict[str, int | float | Facing | None | str]].

        """
        return {"entity": self.entity.to_json(), "inventory": self.inventory.to_json(), "user_id": str(self.user_id), "kills": self.kills}

    @staticmethod
    def from_json(level: Level, json_dict: dict, player_uuid: str) -> Player:
        """Load 'Player' object from json dict.

            :param level: Loaded level.
            :type level: Level.
            :param json_dict: Json dictionnary.
            :type json_dict: dict.

            :param player_uuid: Player's uuid.
            :type player_uuid: str.

            :return: The player.
            :rtype: Player.

        """
        player: Player = level.main_player
        player.user_id = uuid.UUID(json_dict["players"][player_uuid]["user_id"])
        player.kills = json_dict["players"][player_uuid]["kills"]
        player.inventory.clear()
        for item_id in json_dict["players"][player_uuid]["inventory"]:
            player.inventory.add_item(ItemType.get_by_id(int(item_id)), json_dict["players"][player_uuid]["inventory"][item_id])
        teleport_level(level, player.entity, level.get_world_by_name(json_dict["players"][player_uuid]["entity"]["world"]), json_dict["players"][player_uuid]["entity"]["x"])
        player.entity.facing = json_dict["players"][player_uuid]["entity"]["facing"]
        player.entity.uuid = uuid.UUID(json_dict["players"][player_uuid]["entity"]["uuid"]).hex
        return player
