from entities.projectiles.impl.fireball import Fireball
from util.instance import get_game, get_client


class TurretBullet(Fireball):
    def __init__(self, x, y, author, target_pos: tuple[int, int]):
        super().__init__(x, y, author)
        self.motion_x = ((target_pos[0] - self.x) // get_game().TPS) * 2
        self.motion_y = ((target_pos[1] - self.y) // get_game().TPS) * 2

    def activity(self):
        self.x += self.motion_x
        self.y += self.motion_y

        self.do_damage()
        if self.x > get_client().get_screen().get_width()*5 or self.x+self.width < 0-get_client().get_screen().get_width()*5 or self.y > get_client().get_screen().get_height()*5 or self.y + self.height < 0:
            self.death()
