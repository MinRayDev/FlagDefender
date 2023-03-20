from __future__ import annotations

import uuid
from time import time

import pygame

from core.ingame.item.inventory import Inventory
from core.world import Facing
from entities.Entity import DamageType, EntityType

from entities.livingentities.entity_player import PlayerEntity
from entities.projectiles.impl.big_fireball import BigFireball
from entities.projectiles.impl.fireball import Fireball
from entities.projectiles.impl.waterball import Waterball
from network.event import EventType
from network.types import NetworkEntityTypes
from util import world_util
from util.input.controls import ControlsEventTypes
from util.instance import get_game


class Player:
    def __init__(self, controller, world):
        from util.instance import get_client
        self.client = get_client()
        self.entity = PlayerEntity(0, 0, world)
        self.controller = controller
        self.keys = []
        self.events = []
        self.inventory: Inventory = Inventory()
        self.kills = 0
        self.user_id = uuid.uuid4()
        self.kills = 0
        self.gold = 0

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

    def attack(self):
        from core.ingame.spell.impl.bomb import Bomb
        from core.ingame.spell.impl.turret import Turret
        from core.ingame.spell.impl.wall import Wall
        if self.entity.death_time + 5 <= time():
            if self.get_event(pygame.K_a, ControlsEventTypes.DOWN):
                fb = Fireball(self.entity.x, self.entity.y, self.entity)
                self.client.send_event(EventType.ENTITY_SPAWN,
                                       {"entity_type": NetworkEntityTypes.from_class(fb).get_value(),
                                        "entity": fb.to_json()})
            if self.get_event(pygame.K_b, ControlsEventTypes.DOWN):
                Waterball(self.entity.x, self.entity.y, self.entity)

            # if self.get_event(pygame.K_x, ControlsEventTypes.DOWN):
            #     TrajBall(self.entity.x, self.entity.y, self.entity)
            if self.get_event(pygame.K_q, ControlsEventTypes.DOWN):
                BigFireball(self.entity.x, self.entity.y, self.entity)
            if self.get_event(pygame.K_z, ControlsEventTypes.DOWN):
                self.entity.incline += 1
            if self.get_event(pygame.K_s, ControlsEventTypes.DOWN):
                self.entity.incline -= 1
            if self.get_event(pygame.K_c, ControlsEventTypes.DOWN):
                Wall(self)
            if self.get_event(pygame.K_v, ControlsEventTypes.DOWN):
                Turret(self)
            if self.get_event(pygame.K_x, ControlsEventTypes.DOWN):
                # NearTp(self)
                Bomb(self)
                # KillAll(self)
                # TpItems(self)
            if self.get_event(pygame.K_d, ControlsEventTypes.DOWN):
                to_attack = world_util.nearest_entity(self.entity, EntityType.ENEMY)
                if to_attack is not None:
                    if self.entity.facing == Facing.EAST and self.entity.x + 150 >= to_attack.x >= self.entity.x:
                        to_attack.damage(25, DamageType.PHYSICAL, self.entity)
                    elif self.entity.facing == Facing.WEST and self.entity.x - 150 <= to_attack.x <= self.entity.x:
                        to_attack.damage(25, DamageType.PHYSICAL, self.entity)

    @staticmethod
    def get_by_entity(entity: PlayerEntity) -> Player:
        for player in get_game().players:
            if player.entity == entity:
                return player
