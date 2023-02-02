import os

import pygame

from entities.Entity import Entity
from core.world import Facing, World


class PlayerEntity(Entity):
    def __init__(self, x, y, world: World, facing=Facing.SOUTH):
        super().__init__(x, y, sprites_path=os.path.join(r"./resources/sprites/dialga_test"), facing=facing, world=world, health=100)
        world.entities.append(self)
        self.speed = 3
        self.i = 0
        self.max_i = 15

    def activity(self, **kwargs):
        super().activity()
        keys = kwargs["keys"]
        d_events = kwargs["d_events"]
        u_events = kwargs["u_events"]
        col = self.collisions()
        if pygame.K_LEFT in keys:
            if self.x > 0 and col[Facing.WEST]:
                self.x -= self.speed
            if self.facing != Facing.WEST:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                self.facing = Facing.WEST
                self.change_sprite()

        elif pygame.K_RIGHT in keys:
            if self.x < 500 - self.width and col[Facing.EAST]:
                self.x += self.speed
            if self.facing != Facing.EAST:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                self.facing = Facing.EAST
                self.change_sprite()

        elif pygame.K_UP in keys:
            if self.y > 0 and col[Facing.NORTH]:
                self.y -= self.speed
            if self.facing != Facing.NORTH:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                self.facing = Facing.NORTH
                self.change_sprite()

        elif pygame.K_DOWN in keys:
            if self.y < 500 - self.height and col[Facing.SOUTH]:
                self.y += self.speed
            if self.facing != Facing.SOUTH:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                self.facing = Facing.SOUTH
                self.change_sprite()
        self.i += 1
        if pygame.K_y in d_events:
            self.speed = 7
            self.max_i = 8
        if pygame.K_y in u_events:
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
