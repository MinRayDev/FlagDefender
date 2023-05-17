import time

from pygame import Surface

from core.world import World
from entities.entity import Entity
from entities.livingentities.entity_player import PlayerEntity
from util.audio import play_sound
from util.draw_util import draw_with_scroll
from util.world_util import teleport


def filler(surface: Surface) -> None:
    for i in range(255):
        surface.fill((220, 220, 220, i))
        time.sleep(1 / 30)
    time.sleep(1)
    for i in range(255):
        surface.fill((220, 220, 220, 255 - i))
        time.sleep(1 / 30)


class PortalEntity(Entity):
    def __init__(self, x: int, linked_x: int | str, world: World, linked_world: World):
        super().__init__(x, 0, r"./resources/sprites/world/portal", world, None)
        self.linked_x = linked_x
        self.linked_world = linked_world
        self.has_gravity = False
        self.has_collisions = False
        self.to_floor()
        self.players_contained: dict[PlayerEntity, float] = {}
        self.tick = 0

    def activity(self):
        for entity in self.world.entities:
            if self.contact(entity) and isinstance(entity, PlayerEntity) and entity not in self.players_contained:
                self.players_contained[entity] = time.time()
            elif isinstance(entity, PlayerEntity) and not self.contact(entity) and entity in self.players_contained:
                self.players_contained.pop(entity)
            elif entity in self.players_contained and self.players_contained[entity] + 1.5 < time.time():
                teleport(entity, self.linked_world, self.linked_x)
                play_sound("portal.mp3")
                self.players_contained.pop(entity)

    def draw(self, surface: Surface) -> None:
        if len(self.players_contained) > 0:
            if self.tick <= 15:
                draw_with_scroll(surface, self.sprites["hover_0"], self.x, self.y)
                self.tick += 1
            elif self.tick <= 30:
                draw_with_scroll(surface, self.sprites["hover_1"], self.x, self.y)
                self.tick += 1
                if self.tick > 30:
                    self.tick = 0
        else:
            if self.tick <= 15:
                draw_with_scroll(surface, self.sprites["none_0"], self.x, self.y)
                self.tick += 1
            elif self.tick <= 30:
                draw_with_scroll(surface, self.sprites["none_1"], self.x, self.y)
                self.tick += 1
                if self.tick > 30:
                    self.tick = 0
