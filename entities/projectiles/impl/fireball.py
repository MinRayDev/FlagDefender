from core.client import Client
from core.world import Facing
from entities.Entity import Entity
from entities.projectiles.projectile import Projectile
from network.event import EventType
from util import sprites
from util.instance import get_client, get_game


class Fireball(Projectile):
    def __init__(self, x: int, y: int, author: Entity):
        super().__init__(x, y, sprites_path=r"./resources/sprites/test", author=author, damage_value=20)
        match self.facing:
            case Facing.NORTH:
                self.motion_y = -5
                self.x += 78 // 2 - self.width // 2
                self.y -= 16
            case Facing.EAST:
                self.motion_x = 5
                self.x += 78
                self.y += 20
            case Facing.SOUTH:
                self.motion_y = 5
                self.x += 78 // 2 - self.width // 2
                self.y += 80 - 30
            case Facing.WEST:
                self.motion_x = -5
                self.x -= 16
                self.y += 20

    def activity(self, **kwargs):
        super().activity()
        self.x += self.motion_x
        self.y += self.motion_y

        self.do_damage()
        get_client().send_event(EventType.ENTITY_MOVEMENT, {"x": self.x, "y": self.y, "entity_id": str(self.uuid)})
        if self.x > Client.get_screen().get_width()*5 or self.x+self.width < 0-Client.get_screen().get_width()*5 or self.y > Client.get_screen().get_height()*5 or self.y + self.height < 0:
            self.death()

    def to_json(self):
        return {"x": self.x, "y": self.y, "world": self.world.name, "facing": self.facing.value, "uuid": str(self.uuid), "author_uuid": str(self.author.uuid)}

    @staticmethod
    def from_json(json_dict):
        fb = Fireball(json_dict["x"], json_dict["y"], get_game().get_entity_by_uuid(json_dict["author_uuid"]))
        fb.uuid = json_dict["uuid"]
        fb.source = 1
        return fb