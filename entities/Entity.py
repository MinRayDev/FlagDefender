from entities.Object import Object
from core.game import Game
from utils import sprites
from core.world import Facing, World
from typing import Optional


# TODO: passer les collisions sur les objets et en fonction d'une taille et pas du sprite (recalc au changement de sprite)
class Entity(Object):
    def __init__(self, x: int, y: int, sprites_path: str, world: World, facing: Optional[Facing] = None,
                 health=float("inf"), gravity=True):
        self.has_gravity = gravity
        self.world = world
        self.health = health
        self.facing = facing
        self.sprites_files = []
        self.sprites = sprites.load(sprites_path)
        self.sprite_selected = list(self.sprites.values())[0]
        self.max_height = 0
        self.max_width = 0
        self.gravity_value = 3
        for sprite in self.sprites:
            if self.max_height < self.sprites[sprite].get_height():
                self.max_height = self.sprites[sprite].get_height()
            if self.max_width < self.sprites[sprite].get_width():
                self.max_width = self.sprites[sprite].get_width()
        super().__init__(x, y, world=world, width=list(self.sprites.values())[0].get_width(),
                         height=list(self.sprites.values())[0].get_height())

    def activity(self, **kwargs):
        super().activity()
        if self.health <= 0:
            self.death()
        self.gravity()

    def death(self):
        if self in Game.instance.actual_world.entities:
            del Game.instance.actual_world.entities[Game.instance.actual_world.entities.index(self)]

    def sprite_set(self, sprite):
        self.sprite_selected = sprite

    def draw(self, surface):
        surface.blit(self.sprite_selected, (self.x+Game.instance.screen.get_width()//2 + Game.instance.scroll - Game.instance.main_player.entity.width//2, self.y))

    def change_sprite(self):
        pass

    def is_flying(self):
        return self.y + self.height < Game.instance.screen.get_height() - self.world.floor

    def gravity(self):
        if self.has_gravity:
            if self.is_flying():
                if self.y + self.height + self.gravity_value < Game.instance.screen.get_height() - self.world.floor:
                    self.y += self.gravity_value
                else:
                    # print(Game.instance.screen.get_height() - self.world.floor - self.y + self.height)
                    pass
                # prin
            # else:
            #     self.y += Game.instance.screen.get_height() - self.world.floor and self.has_gravity - self.y + self.height

