from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from uuid import UUID

from core.chat.chat import Chat
from core.world import World
from core.ui.menu import Menu


if TYPE_CHECKING:
    from entities.Entity import Entity
    from core.player import Player


class Game:
    instance: Game = None

    def __init__(self):
        self.name: str = "UwU"
        self.version: str = "0.0.1"
        self.menus: list[Menu] = []
        self.actual_menu: Optional[Menu] = None
        self.worlds: list[World] = [World("overworld", 80, (5000, 720))]
        self.queue: list[Entity] = []
        self.actual_world: World = self.worlds[0]
        self.players: list[Player] = []
        self.scroll: int = 0
        self.run: bool = True
        self.main_player: Optional[Player] = None
        self.chat: Chat = Chat()
        self.TPS: float = 60
        self.wave = 1
        # win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def reset_world(self) -> None:
        self.actual_world = None

    def reset_menu(self) -> None:
        self.actual_menu = None

    def set_menu(self, menu: Menu) -> None:
        self.actual_menu = menu

    def has_menu(self) -> bool:
        return self.actual_menu is not None

    def get_world_by_name(self, name: str) -> World:
        for world in self.worlds:
            if world.name == name:
                return world

    def get_entity_by_uuid(self, uuid_: UUID) -> Entity:
        for world in self.worlds:
            for entity in world.entities:
                if entity.uuid == uuid_:
                    return entity
