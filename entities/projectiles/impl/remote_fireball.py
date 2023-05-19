
from core.world import Facing
from entities.entity import Entity
from entities.projectiles.impl.fireball import Fireball
from util.instance import get_client, get_game


class RemoteFireball(Fireball):
    """Class 'RemoteFireball'.

        Extends 'Fireball'.

    """
    def __init__(self, x: int, y: int, author: Entity, target: Entity):
        """Constructor of the class 'RemoteFireball'.

            :param x: The x position of the fireball.
            :type x: int.
            :param y: The y position of the fireball.
            :type y: int.
            :param author: The author of the fireball.
            :type author: Entity.
            :param target: The target of the fireball.
            :type target: Entity.

        """
        super().__init__(x, y, author)
        target_x: int = target.x + target.width//2
        target_y: int = target.y + target.height//2
        match self.facing:
            case Facing.EAST:
                self.x = author.x + author.width
                self.y = author.y + self.height + 2
                self.motion_x = int((target_x - self.x)*2 // get_game().TPS)
                self.motion_y = int(abs((self.y - target_y)*2 // get_game().TPS))
            case Facing.WEST:
                self.x = author.x
                self.y = author.y + self.height + 2
                self.motion_x = int((target_x - self.x)*2 // get_game().TPS)
                self.motion_y = int(abs((self.y - target_y)*2 // get_game().TPS))

    def activity(self) -> None:
        """The activity of the fireball."""
        if self.health <= 0:
            self.death()
        self.gravity()
        self.x += self.motion_x
        self.y += self.motion_y

        self.do_damage()
        if self.x > get_client().get_screen().get_width()*5 or self.x+self.width < 0-get_client().get_screen().get_width()*5 or self.y > get_client().get_screen().get_height()*5 or self.y + self.height < 0:
            self.death()
