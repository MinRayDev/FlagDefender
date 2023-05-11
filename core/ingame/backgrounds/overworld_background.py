from __future__ import annotations

import random
import time
from pygame import Surface
from typing import TYPE_CHECKING

from core.ingame.backgrounds.elements.cloud import Cloud
from util.draw_util import draw_with_scroll

if TYPE_CHECKING:
    from core.level import Level
from core.ingame.background import Background
from core.ingame.backgrounds.elements.floor import Floor
from core.ingame.backgrounds.elements.tree import Tree
from core.world import World
from util.instance import get_game, get_client
from util.sprites import load
from util.time_util import has_elapsed


class OverworldBackground(Background):
    def __init__(self, world: World, loading: bool = False):
        from util.menu import add_check
        add_check("Loading background.", __name__ + "OverworldBackground.init")
        super().__init__(r"./resources/sprites/world/background",
                         r"./resources/sprites/world/background/floor",
                         world, (130, 240, 255), loading)
        self.trees: list[tuple[Tree, int]] = []
        if not loading:
            add_check("Generating trees.", __name__ + "OverworldBackground.init")
            self.trees: list[tuple[Tree, int]] = self.generate_trees()
        add_check("Loading clouds.", __name__ + "OverworldBackground.init")
        self.clouds = [x for x in self.sprites.keys() if "Cloud" in x]
        self.clouds_draw: list[Cloud] = self.generate_clouds()
        add_check("Loading sprites.", __name__ + "OverworldBackground.init")
        self.stars = load(r"./resources/sprites/world/background/star")
        self.moons = load(r"./resources/sprites/world/background/moon")
        self.last_time = 0
        self.last_sprite = 2
        self.night_color = self.sky_color
        surface = get_client().get_screen()
        add_check("Resizing background's sprites.", __name__ + "OverworldBackground.init")
        self.parts = [
            self.resize(self.sprites["0"], surface.get_width()),
            self.resize(self.sprites["1"], surface.get_width() * 1.2),
            self.resize(self.sprites["20"], surface.get_width() * 1.6),
            self.resize(self.sprites["21"], surface.get_width() * 1.6),
            self.resize(self.sprites["22"], surface.get_width() * 1.6),
            self.resize(self.sprites["23"], surface.get_width() * 1.6)
        ]
        self.ratios = [
            (surface.get_width() / (
                        (self.world.size[0] * 2 + self.parts[1].get_width() * 2) * 2 + self.world.size[0] / 1.5)) * 0.2,
            (surface.get_width() / (
                        (self.world.size[0] * 2 + self.parts[2].get_width() * 2) * 2 + self.world.size[0] / 4))

        ]

    def draw(self, surface: Surface) -> None:
        self.draw_sky(surface)
        surface.blit(self.parts[0], (0, surface.get_height() - self.parts[0].get_height() * 1.5))
        surface.blit(
            self.parts[1],
            (
                - ((self.parts[1].get_width() - surface.get_width()) // 2) + get_game().current_level.scroll * self.ratios[
                    0] - get_game().current_level.main_player.entity.width // 2,
                surface.get_height() - self.parts[1].get_height() / 2.2
            )
        )
        surface.blit(
            self.parts[self.last_sprite],
            (
                - ((self.parts[2].get_width() - surface.get_width()) // 2) + get_game().current_level.scroll * self.ratios[
                    1] - get_game().current_level.main_player.entity.width // 2,
                surface.get_height() - self.parts[2].get_height() // 2.9
            )
        )

        if has_elapsed(self.last_time, 0.2):
            self.last_time = time.time()
            self.last_sprite += 1
            if self.last_sprite > 5:
                self.last_sprite = 2

        self.floor.draw(surface)
        for cloud in self.clouds_draw:
            surface.blit(cloud.sprite, (
                cloud.x + get_game().current_level.scroll * cloud.offset - get_game().current_level.main_player.entity.width // 2, cloud.y))
        for tree in self.trees:
            to_draw = tree[0].get_surface()
            draw_with_scroll(surface, to_draw, tree[1], get_client().screen.get_height() - self.world.floor - to_draw.get_height())

    def generate_clouds(self) -> list[Cloud]:
        x = -self.world.size[0] - 800
        clouds: list[Cloud] = []
        while True:
            sprite: Surface = self.sprites[random.choice(self.clouds)]
            if sprite.get_width() >= 150:
                cloud: Cloud = Cloud(sprite, x, random.randint(0, 150))
            else:
                cloud: Cloud = Cloud(sprite, x, random.randint(0, 150 - sprite.get_width()))
            clouds.append(cloud)
            x += random.randint(int(cloud.sprite.get_width() // 1.2), 500)
            if x > self.world.size[0] + 800:
                clouds.sort(key=lambda cloud_: cloud_.offset)
                return clouds

    def generate_trees(self) -> list[tuple[Tree, int]]:
        # x = -self.world.size[0] + 500
        x = -700
        trees: list[tuple[Tree, int]] = []
        while True:
            tree: Tree = Tree()
            if not -300 < x < 300:
                trees.append((tree, x))
            x += random.randint(int(tree.get_surface().get_width() // 1.4), int(tree.get_surface().get_width() * 2.2))
            # if x > self.world.size[0] - 500:
            if x > 700:
                return trees

    def draw_sky(self, surface: Surface) -> None:
        surface.fill(self.sky_color)
        if get_game().current_level.is_night():
            if self.night_color[0] > 6 or self.night_color[1] > 6 or self.night_color[2] > 21:
                r, g, b = self.night_color[0], self.night_color[1], self.night_color[2]
                if r > 6:
                    r -= 2
                if g > 6:
                    g -= 2
                if b > 21:
                    b -= 2
                self.night_color = (r, g, b)
            surface.fill(self.night_color)
        elif get_game().current_level.is_morning():
            if self.night_color[0] < 130 or self.night_color[1] < 240 or self.night_color[2] < 255:
                r, g, b = self.night_color[0], self.night_color[1], self.night_color[2]
                if r < 130:
                    r += 2
                if g < 240:
                    g += 2
                if b < 255:
                    b += 2
                self.night_color = (r, g, b)
            surface.fill(self.night_color)
        if get_game().current_level.is_morning():
            surface.blit(self.stars["sun"], (100, get_client().screen.get_height() - (
                    (time.time() - get_game().current_level.day_start) * surface.get_height()) / (get_game().current_level.day_duration / 2) -
                                             self.stars["sun"].get_height()))
        elif get_game().current_level.is_afternoon():
            surface.blit(self.stars["sun"], (get_client().screen.get_width() - 100 - self.stars["sun"].get_width(), (
                    (time.time() - get_game().current_level.day_start - get_game().current_level.day_duration / 2) * surface.get_height()) / (
                                                     get_game().current_level.day_duration / 2) - self.stars["sun"].get_height()))
        elif get_game().current_level.is_night() and not get_game().current_level.is_past_midnight():
            moon = self.moons["moonfull"]
            # moon_mask = pygame.mask.from_surface(moon)
            # mask.draw(moon_mask, (100, get_client().screen.get_height() - ((time.time() - get_game().day_start - get_game().day_duration) * surface.get_height()) / (get_game().day_duration / 4) - moon.get_height()))
            surface.blit(moon, (100, get_client().screen.get_height() - (
                    (time.time() - get_game().current_level.day_start - get_game().current_level.day_duration) * surface.get_height()) / (
                                        get_game().current_level.day_duration / 4) - moon.get_height()))
        elif get_game().current_level.is_past_midnight():
            moon = self.moons["moonfull"]
            # moon_mask = pygame.mask.from_surface(moon)
            # mask.draw(moon_mask, (get_client().screen.get_width()-100-moon.get_width(), ((time.time() - get_game().day_start - get_game().day_duration * 1.25) * surface.get_height()) / (get_game().day_duration / 4) - moon.get_height()))
            surface.blit(moon, (get_client().screen.get_width() - 100 - moon.get_width(), ((
                                                                                                   time.time() - get_game().current_level.day_start - get_game().current_level.day_duration * 1.25) * surface.get_height()) / (
                                        get_game().current_level.day_duration / 4) - moon.get_height()))

    def to_json(self) -> dict:
        json_dict = {"floor": self.floor.maps, "trees": {}}
        for tree in self.trees:
            json_dict["trees"][tree[1]] = tree[0].to_json()
        return json_dict

    @staticmethod
    def from_json(json_dict: dict, level: 'Level') -> OverworldBackground:
        print("AHOUGA")
        background = OverworldBackground(level.worlds[0], True)
        floor: Floor = Floor(r"./resources/sprites/world/background/floor", level.worlds[0].size[0]*2, level.worlds[0].floor, True)
        floor.maps = json_dict["worlds"]["overworld"]["background"]["floor"]
        for x in range(level.worlds[0].size[0]*4//16):
            for y in range(level.worlds[0].floor//16):
                if y == 0:
                    floor.surface.blit(floor.floor_sprites[floor.maps[x][y]], (16 * x, 0))
                else:
                    floor.surface.blit(floor.floor_sprites[floor.maps[x][y]], (16 * x, 16 * y))
        # TODO: check loading
        # Loading trees
        background.floor = floor
        for x in json_dict["worlds"]["overworld"]["background"]["trees"]:
            print(x)
            background.trees.append((Tree.from_json(json_dict["worlds"]["overworld"]["background"]["trees"][x]), int(x)))
        return background
