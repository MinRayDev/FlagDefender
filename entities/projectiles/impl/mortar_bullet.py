import random

import pygame.time

from core.client import Client
from core.world import Facing
from entities.Entity import Entity
from entities.projectiles.impl.fireball import Fireball
from entities.projectiles.projectile import Projectile
from network.event import EventType
from util import sprites
from util.instance import get_client, get_game


class MortarBullet(Fireball):
    def __init__(self, x: int, y: int, author: Entity, target: Entity):
        super().__init__(x, y, author)

        target_x = random.randint(target.x, target.x + target.width // 2)

        match self.facing:
            case Facing.EAST:
                self.x = author.x + author.width
                self.y = author.y - self.height
            case Facing.WEST:
                self.x = author.x
                self.y = author.y - self.height
        self.motion_x = (target_x - self.x) // get_game().TPS
        self.gravity_value = (target.x - self.x) * 2 // get_game().TPS

    def activity(self, **kwargs):
        if self.health <= 0:
            self.death()
        self.x += self.motion_x
        if self.facing == Facing.EAST or self.facing == Facing.WEST:
            self.y += self.gravity_value
            self.gravity_value += 1

        self.do_damage()
        if self.x > Client.get_screen().get_width() * 5 or self.x + self.width < 0 - Client.get_screen().get_width() * 5 or self.y > Client.get_screen().get_height() * 5:
            self.death()

    def to_json(self):
        return {"x": self.x, "y": self.y, "world": self.world.name, "facing": self.facing.value, "uuid": str(self.uuid), "author_uuid": str(self.author.uuid)}

    @staticmethod
    def from_json(json_dict):
        fb = Fireball(json_dict["x"], json_dict["y"], get_game().get_entity_by_uuid(json_dict["author_uuid"]))
        fb.uuid = json_dict["uuid"]
        fb.source = 1
        return fb
