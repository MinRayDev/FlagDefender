import pygame
from pygame import Surface

from core.ingame.backgrounds.elements.floor import Floor
from core.world import World
from util.instance import get_game
from util.sprites import load


class Background:
    def __init__(self, sprites_path: str, floor_path: str, world: World, skycolor: tuple[int, int, int], loading: bool = False):
        from util.menu import add_check
        add_check("Loading sprites.", __name__ + "Background.init")
        self.sprites = load(sprites_path)
        self.floor: Floor
        if not loading:
            add_check("Creating floor.", __name__ + "Background.init")
            self.floor = Floor(floor_path, world.size[0]*2, world.floor)
        add_check("Floor creating ended.", __name__ + "Background.init")
        self.world = world
        self.sky_color: tuple[int, int, int] = skycolor

    def draw(self, surface: Surface) -> None:
        sprite = self.sprites["0"]
        surface.fill(self.sky_color)

        sprite = self.resize(sprite, surface.get_width())
        sprite.set_alpha(180)
        surface.blit(sprite, (0, surface.get_height() - sprite.get_height()*1.5))
        sprite = self.resize(self.sprites["1"], surface.get_width() * 1.2)
        t_size = (sprite.get_width() - surface.get_width()) // 2
        ratio = (surface.get_width() / ((self.world.size[0] * 2 + sprite.get_width() * 2) * 2 + self.world.size[0] / 1.5))*0.5
        surface.blit(sprite, (- t_size + get_game().current_level.scroll * ratio - get_game().current_level.main_player.entity.width // 2, surface.get_height() - sprite.get_height() / 2.2))
        # surface.blit(sprite, (0, surface.get_height() - sprite.get_height()/2))
        sprite = self.resize(self.sprites["2"], surface.get_width() * 1.6)
        t_size = (sprite.get_width() - surface.get_width())//2
        ratio = (surface.get_width()/((self.world.size[0]*2 + sprite.get_width()*2)*2 + self.world.size[0]/4))
        surface.blit(sprite, (- t_size + get_game().current_level.scroll*ratio - get_game().current_level.main_player.entity.width // 2, surface.get_height() - sprite.get_height()//2.9))
        # surface.blit(sprite, (0, surface.get_height() - sprite.get_height()//2.7))
        self.floor.draw(surface)

    @classmethod
    def resize(cls, to_resize: Surface, new_width) -> Surface:
        ratio = new_width / to_resize.get_width()
        return pygame.transform.scale(to_resize, (new_width, to_resize.get_height() * ratio))
