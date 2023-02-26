import time

from core.client import Client
from core.player import Player
from core.world import Facing
from entities.Entity import Entity, EntityType, DamageType
from entities.livingentities.entity_player import PlayerEntity
from entities.projectiles.projectile import Projectile
from util import sprites
from util.instance import get_game


class BombEntity(Projectile):
    def __init__(self, x, y, author: PlayerEntity):
        super().__init__(x, y, r"./resources/sprites/spells/bomb", author, 60)
        self.creation_time = time.time()
        self.has_gravity = False
        self.type = EntityType.ALLY
        self.gravity_value = 0 - author.incline  # vitesse verticale, negative : vers le haut, positive : vers le bas (-50 max, 0, 5)
        self.strength = 1
        self.has_collisions = False
        self.is_explosing = False
        self.explosion_frame = 0
        if author.incline > 0:
            self.motion_x = (10 / (author.incline + 1)) * 1.25 * self.strength  # vitesse horizontale
        else:
            self.motion_x = 10 * self.strength / 2
        self.acceleration = 0.1  # acceleration verticale
        match self.facing:
            case Facing.EAST:
                self.x += author.width
                self.y += 20
            case Facing.WEST:
                self.motion_x = -self.motion_x
                self.x -= self.width
                self.y += 20

    def draw(self, surface):
        if not self.is_explosing:
            surface.blit(self.sprite_selected, (self.x+Client.get_screen().get_width()//2 + get_game().scroll - get_game().main_player.entity.width//2, self.y))
        elif self.is_explosing and round(self.explosion_frame) < len(self.sprites):
            surface.blit(list(self.sprites.values())[round(self.explosion_frame)], (self.x + Client.get_screen().get_width() // 2 + get_game().scroll - get_game().main_player.entity.width // 2, self.y))
            self.explosion_frame += 0.2

    def activity(self):
        if self.y + self.height + self.gravity_value < Client.get_screen().get_height() - self.world.floor:
            self.x += self.motion_x
            self.y += self.gravity_value
            self.gravity_value += self.acceleration
        if time.time() > self.creation_time + 3 or self.health <= 30:
            self.explosion_start()
            for entity in self.world.entities:
                if entity.type != self.type and entity != self:
                    if self.x - self.width//2 <= entity.x <= self.x + self.width//2 + self.width and self.y <= entity.y <= self.y + entity.height:
                        entity.damage(entity.health, DamageType.EXPLOSION)
                    elif self.x - self.width//2 - self.width <= entity.x <= self.x + self.width//2 + self.width*2 and self.y <= entity.y <= self.y + entity.height:
                        entity.damage(50, DamageType.EXPLOSION)
                    elif self.x - self.width//2 - self.width - 50 <= entity.x <= self.x + self.width//2 + self.width*2 + 50:
                        entity.damage(30, DamageType.EXPLOSION)
        if self.is_explosing and not round(self.explosion_frame) < len(self.sprites):
            self.death()

    def explosion_start(self):
        self.sprites = sprites.load(r"./resources/sprites/spells/explosion")
        self.sprite_selected = list(self.sprites.values())[0]
        self.max_height = 0
        self.max_width = 0
        for sprite in self.sprites:
            if self.max_height < self.sprites[sprite].get_height():
                self.max_height = self.sprites[sprite].get_height()
            if self.max_width < self.sprites[sprite].get_width():
                self.max_width = self.sprites[sprite].get_width()
        self.is_explosing = True
