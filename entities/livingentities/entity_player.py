import os
from time import time

from pygame import Surface

from util.world_util import teleport
from entities.entity import Entity, EntityType, DamageType
from core.world import Facing, World
from util import sprites
from util.input.controls import ControlsEventTypes, Controls
from util.instance import get_game


class PlayerEntity(Entity):
    def __init__(self, x, y, world: World, facing=Facing.EAST):
        from util.instance import get_client
        super().__init__(x, y, sprites_path=os.path.join(r"./resources/sprites/main_player"), facing=facing, world=world, health=100)
        self.client = get_client()
        self.speed = 7
        self.i = 0
        self.max_i = 15
        self.last_facing = self.facing
        self.to_floor()
        self.gravity_value = 3
        self.incline = 0
        self.type = EntityType.ALLY
        self.death_time = 0
        self.invincible = False
        self.frame = 0
        self.is_walking = False

    def activity(self, keys, events):
        super().activity()
        if self.death_time + 5 > time():
            return
        self.is_walking = False
        col = self.get_collisions()
        self.last_facing = self.facing
        if Controls.left_walk.get_code() in keys:
            self.is_walking = True
            if self.frame < 1 or self.frame > 10:
                self.frame = 1
            if self.x > 0-self.world.size[0] and col[Facing.WEST]:
                self.x -= self.speed
                if get_game().current_level.main_player.entity == self:
                    get_game().current_level.scroll += self.speed
            if self.facing != Facing.WEST:
                self.facing = Facing.WEST

                # self.change_sprite()

        elif Controls.right_walk.get_code() in keys:
            self.is_walking = True
            if self.frame < 11 or self.frame > 22:
                self.frame = 12
            if self.x < self.world.size[0] - self.width and col[Facing.EAST]:
                self.x += self.speed
                if get_game().current_level.main_player.entity == self:
                    get_game().current_level.scroll -= self.speed
            if self.facing != Facing.EAST:
                self.facing = Facing.EAST

        self.i += 1
        for event in events:
            if Controls.run.get_code() == event.code and event.type == ControlsEventTypes.DOWN:
                self.speed += 5
                self.max_i = 8
            if Controls.run.get_code() == event.code and event.type == ControlsEventTypes.UP:
                self.speed -= 5
                self.max_i = 15

    def draw(self, surface: Surface) -> None:
        if get_game().current_level.main_player.entity != self:
            super().draw(surface)
            # surface.blit(self.sprite_selected, (self.x + get_client().get_screen().get_width() // 2 + get_game().scroll, self.y))
        else:
            if self.is_walking:
                self.i += 1
                if self.i > 20:
                    self.i = 0
                    self.frame += 1
                    if self.frame == 11:
                        self.frame = 1
                    elif self.frame == 22:
                        self.frame = 12
            else:
                if self.facing == Facing.WEST:
                    self.frame = 0
                elif self.facing == Facing.EAST:
                    self.frame = 11
            surface.blit(self.sprites[str(self.frame)], (surface.get_width()//2 - self.width//2, self.y))


    def death(self):
        teleport(self, self.world, 0)
        self.health = 100
        self.death_time = time()

    def to_json(self):
        return {"x": self.x, "world": self.world.name, "facing": self.facing, "uuid": str(self.uuid)}

    @staticmethod
    def from_json(json_dict):
        pe = PlayerEntity(json_dict["x"], json_dict["y"], get_game().current_level.get_world_by_name(json_dict["world"]), json_dict["facing"])
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

    def damage(self, amount: float, damage_type: DamageType, author: Entity = None):
        if not self.invincible:
            super().damage(amount, damage_type, author)