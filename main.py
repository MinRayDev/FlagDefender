from os.path import dirname, realpath
import pygame
import sys

from pygame.event import Event


def append_module() -> None:
    root: str = dirname(realpath(__file__))
    sys.path.insert(0, root)


if __name__ == "__main__":
    append_module()
    from core.client import Client
    from core.game import Game
    from ui.game_menu import GameMenu
    from util.input.controls import ControlsEventTypes, Inputs

    client: Client = Client()
    Client.instance = client
    game: Game = Game()
    Game.instance = game

    last_update = -1

    while game.run:
        # Get events and inputs.
        events: list[Event] = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game.run = False
        if game.current_menu is not None:
            for controller in client.controllers:
                events_filtered: Inputs = controller.get_event_controls(events)
                for elem_ in events_filtered:
                    if elem_.type == ControlsEventTypes.UP:
                        game.current_menu.add_queue(elem_)
                for elem_ in events_filtered.raw_inputs:
                    game.current_menu.add_raw_queue(elem_)
        if game.current_menu is None or (isinstance(game.current_menu, GameMenu) and not game.current_menu.game_input_filter):
            for player in game.current_level.players:
                player.get_controls(events)

        # Update logic
        if (pygame.time.get_ticks() - last_update) / 1000 > 1 / game.TPS:
            game.update_logic()
            last_update = pygame.time.get_ticks()

        # Rendering
        game.render(client.get_screen())
        client.clock.tick(120)
        pygame.display.update()
    pygame.quit()
