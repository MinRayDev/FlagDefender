import os

import pygame

from core.game import Game
from entities.Entity import Entity
from core.world import Facing, World
from utils.inputs.controls import EventTypes


class PlayerEntity(Entity):
    def __init__(self, x, y, world: World, facing=Facing.EAST):
        super().__init__(x, y, sprites_path=os.path.join(r"./resources/sprites/main_player"), facing=facing, world=world, health=100)
        world.entities.append(self)
        self.speed = 3
        self.i = 0
        self.max_i = 15
        self.last_facing = self.facing
        self.y = Game.instance.screen.get_height()-Game.instance.actual_world.floor-self.height
        self.gravity_value = 3
        self.jump_test = 0
        self.incline = 0

    def activity(self, keys, events):
        super().activity()
        col = self.get_collisions()
        self.last_facing = self.facing
        if pygame.K_LEFT in keys:
            if self.x > 0-self.world.size[0] and col[Facing.WEST]:
                self.x -= self.speed
                if Game.instance.main_player.entity == self:
                    Game.instance.scroll += self.speed
            if self.facing != Facing.WEST:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                self.facing = Facing.WEST
                # self.change_sprite()

        elif pygame.K_RIGHT in keys:
            if self.x < self.world.size[0] - self.width and col[Facing.EAST]:
                self.x += self.speed
                if Game.instance.main_player.entity == self:
                    Game.instance.scroll -= self.speed
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
            if pygame.K_y == event.code and event.type == EventTypes.DOWN:
                self.speed = 7
                self.max_i = 8
            if pygame.K_y == event.code and event.type == EventTypes.UP:
                self.speed = 3
                self.max_i = 15

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
        if Game.instance.main_player.entity != self:
            surface.blit(self.sprite_selected, (self.x + Game.instance.screen.get_width() // 2 + Game.instance.scroll, self.y))
        else:
            surface.blit(self.sprite_selected, (Game.instance.screen.get_width()//2 - self.width//2, self.y))
