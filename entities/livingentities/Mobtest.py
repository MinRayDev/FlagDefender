import threading

import random
from entities.Entity import Entity
from entities.projectiles.Fireball import Fireball
from core.world import Facing
from core.game import Game


class Mob(Entity):
    def __init__(self, x, y, world, facing=Facing.SOUTH):
        super().__init__(x, y, sprites_path=r"./resources/sprites/palkia_test", facing=facing, world=world)
        self.speed = 3
        self.i = 0
        self.max_i = 15
        self.__goto = (x, y)
        self.attack_i = 0
        world.entities.append(self)

    def activity(self, **kwargs):
        if self.attack_i > 30:
            self.attack_i = 0
            if random.randint(30, 100) > 70:
                thread = threading.Thread(target=self.attack, daemon=True)
                thread.start()
        super().activity()

        past_facing = self.facing
        self.goto()
        if self.facing == Facing.WEST:
            if self.facing != past_facing:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                self.change_sprite()

        elif self.facing == Facing.EAST:
            if self.facing != past_facing:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                self.change_sprite()

        elif self.facing == Facing.NORTH:
            if self.facing != past_facing:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                self.change_sprite()

        elif self.facing == past_facing:
            if self.facing != Facing.SOUTH:
                self.i = self.max_i + self.i
            if self.i > self.max_i:
                self.i = 0
                self.change_sprite()
        self.i += 1
        self.attack_i += 1

    def goto(self):
        col = self.collisions()
        if self.x == self.__goto[0] and self.y == self.__goto[1]:
            self.__goto = (random.randint(1, 500 - self.width), random.randint(1, 500 - self.height))
        if self.x != self.__goto[0]:
            if self.x > self.__goto[0]:
                if col[Facing.WEST]:
                    self.x -= 1
                    self.facing = Facing.WEST
            elif col[Facing.EAST]:
                self.x += 1
                self.facing = Facing.EAST
        elif self.y != self.__goto[1]:
            if self.y > self.__goto[1]:
                if col[Facing.NORTH]:
                    self.y -= 1
                    self.facing = Facing.NORTH
            elif col[Facing.SOUTH]:
                self.y += 1
                self.facing = Facing.SOUTH

    def attack(self):
        Game.instance.queue.append(Fireball(self.x, self.y, self))

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
