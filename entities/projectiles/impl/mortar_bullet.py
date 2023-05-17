import math
import time

from core.world import Facing
from entities.entity import Entity
from entities.projectiles.impl.fireball import Fireball
from util.instance import get_game, get_client
from util.time_util import has_elapsed
from util.world_util import get_dist


class MortarBullet(Fireball):
    def __init__(self, x: int, y: int, author: Entity, target: Entity):
        super().__init__(x, y, author)
        self.y = author.y + 10
        if self.facing == Facing.WEST:
            self.x = author.x - self.width - 2
        else:
            self.x = author.x + author.width + 2
        self.t = 0
        incline = 5
        self.gravity_value = 0 - incline  # vitesse verticale, negative : vers le haut, positive : vers le bas
        self.start_time = time.time()
        self.target = target

        incline_factor: float = (10 - incline) / 10
        angle_target = math.pi / 2 + ((math.pi / 2) * incline_factor)

        self.motion_x = 10 * math.cos(angle_target)
        if self.facing == Facing.EAST:  # /summon MobMortar 3000 overworld
            self.motion_x *= -1

        print("dist", get_dist(author, self.target), author.x, self.target.x, max(author.x, self.target.x), min(author.x, self.target.x))
        self.deceleration = 0.1

    def activity(self):
        super().activity()
        if self.y + self.height + self.gravity_value < get_client().get_screen().get_height() - self.world.floor:
            self.x += self.motion_x
            self.y += self.gravity_value
            self.gravity_value += self.deceleration
            self.gravity_value = max(min(self.gravity_value, 10), -10)

        elif self.t >= 30:
            self.death()
        else:
            self.t += 1

        if self.x > get_client().get_screen().get_width() * 5 or self.x + self.width < 0 - get_client().get_screen().get_width() * 5 or self.y > get_client().get_screen().get_height() * 5:
            self.death()
        elif has_elapsed(self.start_time, 10):
            self.death()

        self.do_damage()

    def to_json(self):
        return {"x": self.x, "y": self.y, "world": self.world.name, "facing": self.facing.value, "uuid": str(self.uuid), "author_uuid": str(self.author.uuid)}

    @staticmethod
    def from_json(json_dict):
        fb = Fireball(json_dict["x"], json_dict["y"], get_game().current_level.get_entity_by_uuid(json_dict["author_uuid"]))
        fb.uuid = json_dict["uuid"]
        fb.source = 1
        return fb
