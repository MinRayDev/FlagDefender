import os
from time import time

import pygame

from network.event import EventType
from util.world_util import teleport
from entities.Entity import Entity, EntityType
from core.world import Facing, World
from util import sprites
from util.input.controls import ControlsEventTypes
from util.instance import get_game
from util.instance import get_client


class PlayerEntity(Entity):
    def __init__(self, x, y, world: World, facing=Facing.EAST):
        super().__init__(x, y, sprites_path=os.path.join(r"./resources/sprites/main_player"), facing=facing, world=world, health=100)
        self.speed = 3
        self.i = 0
        self.max_i = 15
        self.last_facing = self.facing
        self.y = get_client().get_screen().get_height()-self.world.floor-self.height
        self.gravity_value = 3
        self.jump_test = 0
        self.incline = 0
        self.type = EntityType.ALLY
        self.death_time = 0

    def activity(self, keys, events):
        super().activity()
        temp_x = self.x
        temp_y = self.y
        if self.death_time + 5 > time():
            return
        col = self.get_collisions()
        self.last_facing = self.facing
        if pygame.K_LEFT in keys:
            if self.x > 0-self.world.size[0] and col[Facing.WEST]:
                self.x -= self.speed
                if get_game().main_player.entity == self:
                    get_game().scroll += self.speed
            if self.facing != Facing.WEST:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                self.facing = Facing.WEST
                # self.change_sprite()

        elif pygame.K_RIGHT in keys:
            if self.x < self.world.size[0] - self.width and col[Facing.EAST]:
                self.x += self.speed
                if get_game().main_player.entity == self:
                    get_game().scroll -= self.speed
            if self.facing != Facing.EAST:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                self.facing = Facing.EAST
                # self.change_sprite()
        # elif pygame.K_UP in keys:
        #     self.jump_test = 5
        #     if self.y > 0 and col[Facing.NORTH]:
        #         self.y -= self.speed - self.jump_test
        #     if self.facing != Facing.NORTH:
        #         self.i = self.max_i + self.i
        #     if self.i > self.max_i:
        #         self.i = 0
        #         self.facing = Facing.NORTH
        #         # self.change_sprite()
        #
        # if self.jump_test != 0:
        #     print("-----")
        #     print(self.y)
        #     self.y -= self.speed - self.jump_test*2
        #     print(self.y)
        #     self.jump_test -= 1

        self.i += 1
        for event in events:
            if pygame.K_y == event.code and event.type == ControlsEventTypes.DOWN:
                self.speed = 7
                self.max_i = 8
            if pygame.K_y == event.code and event.type == ControlsEventTypes.UP:
                self.speed = 3
                self.max_i = 15
        if self.x != temp_x or temp_y != self.y:
            get_client().send_event(EventType.ENTITY_MOVEMENT, {"x": self.x, "y": self.y, "entity_id": str(self.uuid)})

    def change_sprite(self):
        match self.facing:
            case Facing.NORTH:
                self.sprite_set(list(self.sprites.values())[7]) if self.sprite_selected == list(self.sprites.values())[6] else self.sprite_set(list(self.sprites.values())[6])
            case Facing.SOUTH:
                self.sprite_set(list(self.sprites.values())[1]) if self.sprite_selected == list(self.sprites.values())[0] else self.sprite_set(list(self.sprites.values())[0])
            case Facing.EAST:
                self.sprite_set(list(self.sprites.values())[5]) if self.sprite_selected == list(self.sprites.values())[4] else self.sprite_set(list(self.sprites.values())[4])
            case Facing.WEST:
                self.sprite_set(list(self.sprites.values())[3]) if self.sprite_selected == list(self.sprites.values())[2] else self.sprite_set(list(self.sprites.values())[2])
        if self.facing != self.last_facing and self.last_facing not in [Facing.NORTH, Facing.SOUTH]:
            self.x = self.x + self.max_width // 2 - self.sprite_selected.get_width() // 2

        if self.facing != self.last_facing and self.last_facing not in [Facing.EAST, Facing.WEST]:
            self.y = self.y + self.max_height // 2 - self.sprite_selected.get_height() // 2

    def draw(self, surface):
        if get_game().main_player.entity != self:
            super().draw(surface)
            # surface.blit(self.sprite_selected, (self.x + get_client().get_screen().get_width() // 2 + get_game().scroll, self.y))
        else:
            surface.blit(self.sprite_selected, (get_client().get_screen().get_width()//2 - self.width//2, self.y))

    def death(self):
        teleport(self, self.world, 0)
        self.health = 100
        self.death_time = time()

    def to_json(self):
        return {"x": self.x, "y": self.y, "world": self.world.name, "facing": self.facing.value, "uuid": str(self.uuid)}

    @staticmethod
    def from_json(json_dict):
        pe = PlayerEntity(json_dict["x"], json_dict["y"], get_game().get_world_by_name(json_dict["world"]), json_dict["facing"])
        pe.uuid = json_dict["uuid"]
        pe.source = 1
        pe.sprites = sprites.load(os.path.join(r"./resources/sprites/online_player"))
        pe.sprite_selected = list(pe.sprites.values())[0]
        for sprite in pe.sprites:
            if pe.max_height < pe.sprites[sprite].get_height():
                pe.max_height = pe.sprites[sprite].get_height()
            if pe.max_width < pe.sprites[sprite].get_width():
                pe.max_width = pe.sprites[sprite].get_width()
        return pe
