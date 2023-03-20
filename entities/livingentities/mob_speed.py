import random
import threading

import pygame
from catppuccin import Flavour

from core.client import Client
from core.ingame.item.item_type import ItemType
from core.world import Facing
from entities.Entity import Entity, EntityType
from entities.Item import ItemEntity
from entities.livingentities.mob import Mob
from entities.projectiles.impl.fireball import Fireball
from network.event import EventType
from network.types import NetworkEntityTypes
from util.instance import get_game, get_client


class MobSpeed(Mob):
    def __init__(self, x, y, world, facing=Facing.SOUTH):
        from util.instance import get_client
        super().__init__(x, y, sprites_path=r"./resources/sprites/enemy_speed", facing=facing, world=world, health=100)
        self.type = EntityType.ENEMY
        self.client = get_client()
        self.i = 0
        self.max_i = 15
        self.last_facing = self.facing
        self.to_floor()
        self.cooldown = 30

    def activity(self, **kwargs):
        super().activity()
        self.last_facing = self.facing
        past_facing = self.facing
        if self.facing == Facing.WEST:
            if self.facing != past_facing:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                # self.change_sprite()

        elif self.facing == Facing.EAST:
            if self.facing != past_facing:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                # self.change_sprite()

        elif self.facing == Facing.NORTH:
            if self.facing != past_facing:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                # self.change_sprite()

        elif self.facing == past_facing:
            if self.facing != Facing.SOUTH:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                # self.change_sprite()
        self.i += 1

    def attack(self):
        if random.randint(30, 100) > 70:
            fb = Fireball(self.x, self.y, self)
            self.client.send_event(EventType.ENTITY_SPAWN, {"entity_type": NetworkEntityTypes.from_class(fb).get_value(), "entity": fb.to_json()})

    def death(self):
        ItemEntity(self.x + (self.width//2), r"./resources/sprites/items/test", self.world, ItemType.sword)
        super().death()

    def draw(self, surface):
        super().draw(surface)
        pygame.draw.rect(surface, Flavour.frappe().surface2.rgb, pygame.Rect(self.x - 4 + get_client().get_screen().get_width() // 2 + get_game().scroll - get_game().main_player.entity.width // 2, self.y - 14, self.width+8, 8))
        health_percentage = self.health / self.max_health
        pygame.draw.rect(surface, Flavour.frappe().red.rgb, pygame.Rect(self.x - 4 + get_client().get_screen().get_width() // 2 + get_game().scroll - get_game().main_player.entity.width // 2, self.y - 14, int((self.width+8)*health_percentage), 8))

    # def change_sprite(self):
    #     match self.facing:
    #         case Facing.NORTH:
    #             self.sprite_set(list(self.sprites.values())[7]) if self.sprite_selected == list(self.sprites.values())[6] else self.sprite_set(list(self.sprites.values())[6])
    #         case Facing.SOUTH:
    #             self.sprite_set(list(self.sprites.values())[1]) if self.sprite_selected == list(self.sprites.values())[0] else self.sprite_set(list(self.sprites.values())[0])
    #         case Facing.EAST:
    #             self.sprite_set(list(self.sprites.values())[5]) if self.sprite_selected == list(self.sprites.values())[4] else self.sprite_set(list(self.sprites.values())[4])
    #         case Facing.WEST:
    #             self.sprite_set(list(self.sprites.values())[3]) if self.sprite_selected == list(self.sprites.values())[2] else self.sprite_set(list(self.sprites.values())[2])
    #
    #     # b
