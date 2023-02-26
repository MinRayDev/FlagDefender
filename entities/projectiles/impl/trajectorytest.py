from core.client import Client
from core.world import Facing
from entities.livingentities.entity_player import PlayerEntity
from entities.projectiles.projectile import Projectile


class TrajBall(Projectile):
    def __init__(self, x: int, y: int, author: PlayerEntity):
        super().__init__(x, y, sprites_path=r"./resources/sprites/test", author=author, damage_value=20)
        print(author.incline)  # incline max: 10, min: -12
        self.gravity_value = 0-author.incline  # vitesse verticale, negative : vers le haut, positive : vers le bas (-50 max, 0, 5)
        self.strength = 1
        if author.incline > 0:
            self.motion_x = (10/(author.incline + 1))*1.25*self.strength  # vitesse horizontale
        else:
            self.motion_x = 10*self.strength/2
        self.acceleration = 0.1  # acceleration verticale
        match self.facing:
            case Facing.EAST:
                self.x += author.width
                self.y += 20
            case Facing.WEST:
                self.motion_x = -self.motion_x
                self.x -= self.width
                self.y += 20

    def activity(self, **kwargs):
        super().activity()
        if self.y + self.height + self.gravity_value < Client.get_screen().get_height() - self.world.floor:
            self.x += self.motion_x
            self.y += self.gravity_value
            self.gravity_value += self.acceleration

        if self.x > Client.get_screen().get_width() * 5 or self.x + self.width < 0 - Client.get_screen().get_width() * 5 or self.y > Client.get_screen().get_height() * 5:
            self.death()
