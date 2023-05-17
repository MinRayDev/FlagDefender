
from core.world import Facing
from entities.entity import Entity
from entities.projectiles.impl.fireball import Fireball
from util.instance import get_client, get_game
from util.logger import log


class RemoteFireball(Fireball):
    def __init__(self, x: int, y: int, author: Entity, target: Entity):
        super().__init__(x, y, author)
        target_x = target.x + target.width//2
        target_y = target.y + target.height//2
        match self.facing:
            case Facing.EAST:
                self.x = author.x + author.width
                self.y = author.y + self.height + 2
                self.motion_x = (target_x - self.x)*2 // get_game().TPS
                self.motion_y = abs((self.y - target_y)*2 // get_game().TPS)
            case Facing.WEST:
                self.x = author.x
                self.y = author.y + self.height + 2
                self.motion_x = (target_x - self.x)*2 // get_game().TPS
                self.motion_y = abs((self.y - target_y)*2 // get_game().TPS)

    def activity(self):
        log(str(self.x) + " " + str(self.y))
        if self.health <= 0:
            self.death()
        self.gravity()
        self.x += self.motion_x
        self.y += self.motion_y

        self.do_damage()
        if self.x > get_client().get_screen().get_width()*5 or self.x+self.width < 0-get_client().get_screen().get_width()*5 or self.y > get_client().get_screen().get_height()*5 or self.y + self.height < 0:
            self.death()

    def to_json(self):
        return {"x": self.x, "y": self.y, "world": self.world.name, "facing": self.facing.value, "uuid": str(self.uuid), "author_uuid": str(self.author.uuid)}

    @staticmethod
    def from_json(json_dict):
        fb = Fireball(json_dict["x"], json_dict["y"], get_game().current_level.get_entity_by_uuid(json_dict["author_uuid"]))
        fb.uuid = json_dict["uuid"]
        fb.source = 1
        return fb
