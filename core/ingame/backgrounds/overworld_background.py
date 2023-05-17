import random
import time
from typing import TYPE_CHECKING

from pygame import Surface

from core.world import World
from util.sprites import load
from util.menu import add_check
from util.time_util import has_elapsed
from util.draw_util import draw_with_scroll
from core.ingame.background import Background
from util.instance import get_game, get_client
from core.ingame.backgrounds.elements.tree import Tree
from core.ingame.backgrounds.elements.floor import Floor
from core.ingame.backgrounds.elements.cloud import Cloud

if TYPE_CHECKING:
    from core.level import Level


class OverworldBackground(Background):
    """Class 'OverworldBackground'.

        OverworldBackground class is the class for background of the overworld.

        :ivar trees: List of tree.
        :type trees: list[tuple[Tree, int]].
        :ivar __cloud_sprites: List of clouds sprites names.
        :type __cloud_sprites: list[str].
        :ivar __clouds: List of clouds.
        :type __clouds: list[Cloud].
        :ivar __stars: Dict of stars sprites associated with their names.
        :type __stars: dict[str, Surface].
        :ivar __moons: Dict of moons sprites associated with their names.
        :type __moons: dict[str, Surface].

        :ivar __last_time: Time of the last time the sprite was modified.
        :type __last_time: float.
        :ivar __last_sprite: Last sprite indexes.
        :type __last_sprite: int.
        :ivar night_color: Night sky color (rgb).
        :type night_color: tuple[int, int, int].

        :ivar __parts: List of parts making up the background.
        :type __parts: list[Surface].
        :ivar __ratios: List of ratios modifying the scroll.
        :type __ratios: list[float].

    """
    trees: list[tuple[Tree, int]]
    __cloud_sprites: list[str]
    __clouds: list[Cloud]
    __stars: dict[str, Surface]
    __moons: dict[str, Surface]
    __last_time: float
    __last_sprite: int
    night_color: tuple[int, int, int]
    __parts: list[Surface]
    __ratios: list[float]

    def __init__(self, world: World, loading: bool = False):
        """Constructor function for OverworldBackground class.

            :param world: World of the background.
            :type world: World.
            :param loading: If the level is loaded or not.
            :type loading: bool.

        """
        add_check("Loading background.", __name__ + "OverworldBackground.init")
        super().__init__(r"./resources/sprites/world/background", r"./resources/sprites/world/background/floor", world, (130, 240, 255), loading)
        self.trees = []
        if not loading:
            add_check("Generating trees.", __name__ + "OverworldBackground.init")
            self.trees = self.generate_trees()

        add_check("Loading clouds.", __name__ + "OverworldBackground.init")
        self.__cloud_sprites = [x for x in self.sprites.keys() if "Cloud" in x]
        self.__clouds = self.generate_clouds()

        add_check("Loading sprites.", __name__ + "OverworldBackground.init")
        self.__stars = load(r"./resources/sprites/world/background/star")
        self.__moons = load(r"./resources/sprites/world/background/moon")
        self.__last_time = 0
        self.__last_sprite = 2
        self.night_color = self.sky_color

        surface = get_client().get_screen()
        add_check("Resizing background's sprites.", __name__ + "OverworldBackground.init")
        self.__parts = [
            self.resize(self.sprites["0"], surface.get_width()),
            self.resize(self.sprites["1"], int(surface.get_width() * 1.2)),
            self.resize(self.sprites["20"], int(surface.get_width() * 1.6)),
            self.resize(self.sprites["21"], int(surface.get_width() * 1.6)),
            self.resize(self.sprites["22"], int(surface.get_width() * 1.6)),
            self.resize(self.sprites["23"], int(surface.get_width() * 1.6))
        ]
        self.__ratios = [
            (surface.get_width() / ((self.world.size[0] * 2 + self.__parts[1].get_width() * 2) * 2 + self.world.size[0] / 1.5)) * 0.2,
            (surface.get_width() / ((self.world.size[0] * 2 + self.__parts[2].get_width() * 2) * 2 + self.world.size[0] / 4))
        ]

    def draw(self, surface: Surface) -> None:
        """Draw this object on the client's screen.

            :param surface: Surface to draw.
            :type surface: Surface.

        """
        self.draw_sky(surface)
        surface.blit(self.__parts[0], (0, surface.get_height() - self.__parts[0].get_height() * 1.5))
        surface.blit(
            self.__parts[1],
            (
                - ((self.__parts[1].get_width() - surface.get_width()) // 2) + get_game().current_level.scroll *
                self.__ratios[0] - get_game().current_level.main_player.entity.width // 2,
                surface.get_height() - self.__parts[1].get_height() / 2.2
            )
        )
        surface.blit(
            self.__parts[self.__last_sprite],
            (
                - ((self.__parts[2].get_width() - surface.get_width()) // 2) + get_game().current_level.scroll *
                self.__ratios[1] - get_game().current_level.main_player.entity.width // 2,
                surface.get_height() - self.__parts[2].get_height() // 2.9
            )
        )

        if has_elapsed(self.__last_time, 0.2):
            self.__last_time = time.time()
            self.__last_sprite += 1
            if self.__last_sprite > 5:
                self.__last_sprite = 2

        self.floor.draw(surface)

        for cloud in self.__clouds:
            surface.blit(
                cloud.sprite, (
                    cloud.x + get_game().current_level.scroll * cloud.offset - get_game().current_level.main_player.entity.width // 2,
                    cloud.y
                )
            )
        for tree in self.trees:
            to_draw = tree[0].get_surface()
            draw_with_scroll(surface, to_draw, tree[1], get_client().get_screen().get_height() - self.world.floor - to_draw.get_height())

    def generate_clouds(self) -> list[Cloud]:
        """Generates clouds.

            :return: List of clouds.
            :rtype: list[Cloud].

        """
        x = -self.world.size[0] - 800
        clouds: list[Cloud] = []
        while True:
            sprite: Surface = self.sprites[random.choice(self.__cloud_sprites)]
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
        """Generates trees.

            :return: List of trees and their x coordinates.
            :rtype: list[tuple[Tree, int]].

        """
        x = -self.world.size[0] + 500
        trees: list[tuple[Tree, int]] = []
        while True:
            width: int = 10
            if not -300 < x < 300:
                tree: Tree = Tree()
                trees.append((tree, x))
                width = tree.get_surface().get_width()
            x += random.randint(int(width * 0.7), int(width * 2.2))
            if x > self.world.size[0] - 500:
                return trees

    def draw_sky(self, surface: Surface) -> None:
        """Draw sky on the client's screen.

            :param surface: Surface to draw.
            :type surface: Surface.

        """
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
            surface.blit(
                self.__stars["sun"],
                (
                    100,
                    get_client().get_screen().get_height() - ((time.time() - get_game().current_level.day_start)
                                                              * surface.get_height()) / (get_game().current_level.day_duration / 2) - self.__stars["sun"].get_height()
                 )
            )
        elif get_game().current_level.is_afternoon():
            surface.blit(
                self.__stars["sun"],
                (
                    get_client().get_screen().get_width() - 100 - self.__stars["sun"].get_width(),
                    (
                            (
                                    time.time() - get_game().current_level.day_start - get_game().current_level.day_duration / 2) *
                            surface.get_height()) / (get_game().current_level.day_duration / 2) - self.__stars["sun"].get_height()
                )
            )

        elif get_game().current_level.is_night() and not get_game().current_level.is_past_midnight():
            moon = self.__moons["moonfull"]
            surface.blit(
                moon,
                (
                    100,
                    get_client().get_screen().get_height() - ((time.time() - get_game().current_level.day_start - get_game().current_level.day_duration)
                                                              * surface.get_height()) / (get_game().current_level.day_duration / 4) - moon.get_height()
                )
            )

        elif get_game().current_level.is_past_midnight():
            moon = self.__moons["moonfull"]
            surface.blit(
                moon,
                (
                    get_client().get_screen().get_width() - 100 - moon.get_width(),
                    ((time.time() - get_game().current_level.day_start - get_game().current_level.day_duration * 1.25)
                     * surface.get_height()) / (get_game().current_level.day_duration / 4) - moon.get_height()
                )
            )

    def to_json(self) -> dict[str, list[list[str]] | dict]:
        """Convert this object to json format.

            :return: Json dictionnary.
            :rtype: dict[str, list[list[str]] | dict].

        """
        json_dict = {"floor": self.floor.maps, "trees": {}}
        for tree in self.trees:
            json_dict["trees"][tree[1]] = tree[0].to_json()
        return json_dict

    @staticmethod
    def from_json(json_dict: dict, level: 'Level') -> 'OverworldBackground':
        """Load 'OverworldBackground' object from json dict.

            :param json_dict: Json dictionnary.
            :type json_dict: dict.
            :param level: Loaded level.
            :type level: Level.

            :return: The background.
            :rtype: OverworldBackground.

        """
        background = OverworldBackground(level.worlds[0], True)
        floor: Floor = Floor(r"./resources/sprites/world/background/floor", level.worlds[0].size[0] * 2, level.worlds[0].floor, True)
        backgrounds = json_dict["worlds"]["overworld"]["background"]
        floor.maps = backgrounds["floor"]
        add_check("Loading floor parts.", __name__ + "OverworldBackground.from_json")
        for x in range(level.worlds[0].size[0] * 4 // 16):
            for y in range(level.worlds[0].floor // 16):
                if y == 0:
                    floor.surface.blit(floor.floor_sprites[floor.maps[x][y]], (16 * x, 0))
                else:
                    floor.surface.blit(floor.floor_sprites[floor.maps[x][y]], (16 * x, 16 * y))
        add_check("Loading trees.", __name__ + "OverworldBackground.from_json")
        background.floor = floor
        trees = backgrounds["trees"]
        for x in trees:
            background.trees.append((Tree.from_json(trees[x]), int(x)))
        return background
