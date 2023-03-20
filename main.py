import pygame

from core.client import Client
from core.game import Game
from core.ui.game_menu import GameMenu
from core.ui.impl.ingame_menu.chat import ChatMenu
from core.ui.impl.ingame_menu.chat_message import ChatMessageMenu
from core.ui.impl.ingame_menu.hud import HUD
from core.ui.impl.ingame_menu.inventory import InventoryMenu
from core.ui.impl.main_menu import MainMenu
from core.player import Player
from core.world import World
from entities.Entity import Entity
from entities.livingentities.entity_player import PlayerEntity
from entities.livingentities.mob_mortar import MobMortar
from util.input.controllers import Controller
from util.input.controls import ControlsEventTypes, Sources, test

game: Game = Game()
Game.instance = game
client: Client = Client()
Client.instance = client

# player = PlayerEntity(200, 200, ingame.actual_world)

MobMortar(1000, 0, game.actual_world)
MobMortar(600, 0, game.actual_world)
# Spawner(500, 0, ingame.actual_world)
game.actual_menu = MainMenu()
t_world: World = World("test_world", 80, (5000, 720))
game.instance.worlds.append(t_world)
ta = Entity(0, 300, r"./resources/sprites/dialga_test", t_world, gravity=False)
last_update = -1
for controller in client.controllers:
    game.players.append(Player(controller, game.actual_world))
keyboard = Controller(Sources.keyboard, None)
if len(game.players) == 0:
    game.players.append(Player(keyboard, game.actual_world))
client.controllers.append(keyboard)
client.controllers.append(Controller(Sources.mouse, None))
game.main_player = game.players[0]
test_e: Entity = Entity(300, 300, r"./resources/sprites/palkia_test", game.actual_world, gravity=False)
# portal_test = PortalEntity(250, 100, game.main_player.entity.world, t_world)
# portal_test1 = PortalEntity(-100, 100, t_world, game.main_player.entity.world)
chat_menu = ChatMessageMenu()
hud = HUD()

while game.run:
    event_handler = pygame.event.get()
    for event in event_handler:
        if event.type == pygame.QUIT:
            game.run = False
    if game.actual_menu is not None:
        for controller in client.controllers:
            events_ = controller.get_event_controls(event_handler)
            for elem_ in events_:
                if elem_.type == ControlsEventTypes.UP:
                    game.actual_menu.add_queue(elem_)
            for elem_ in events_.raw_inputs:
                game.actual_menu.add_raw_queue(elem_)
    if game.actual_menu is None or (isinstance(game.actual_menu, GameMenu) and not game.actual_menu.game_input_filter):
        for player in game.players:
            player.get_controls(event_handler)

    # Game logic
    def game_update():
        if game.actual_menu is not None and not isinstance(game.actual_menu, GameMenu):
            game.actual_menu.activity()
        else:

            for elem in game.queue:
                del game.queue[game.queue.index(elem)]
                game.actual_world.entities.append(elem)
            if isinstance(game.actual_menu, GameMenu):
                game.actual_menu.activity()
            for entity_ in game.main_player.entity.world.entities:
                if not isinstance(entity_, PlayerEntity) and entity.source == 0:
                    entity_.activity()
            for player_ in game.players:
                player_.attack()

                if player_.get_event(pygame.K_RETURN, ControlsEventTypes.DOWN) and Game.instance.actual_menu is None:
                    Game.instance.set_menu(ChatMenu())
                if player_.get_event(pygame.K_e, ControlsEventTypes.DOWN) and Game.instance.actual_menu is None:
                    Game.instance.set_menu(InventoryMenu())
                for t in test:
                    if player_.get_event(t, ControlsEventTypes.DOWN) and Game.instance.actual_menu is not None and player_.get_inventory().get_item_count(test[t]) > 0:
                        player_.get_inventory().remove_item(test[t], 1)
                        exec(test[t].get_usage() + "(get_game().main_player)")
                player_.entity.activity(keys=player_.keys, events=player_.events)
                player_.reset_queues()
                break

        if client.online:
            pass
            # client.game_websocket.send("")


    delta_time = (pygame.time.get_ticks() - last_update) / 1000.
    if delta_time > 1. / game.TPS:
        game_update()
        last_update = pygame.time.get_ticks()

    # Rendering
    if isinstance(game.actual_menu, GameMenu) or game.actual_menu is None:
        # Draw world
        client.screen.fill((0, 0, 0))

        for entity in game.main_player.entity.world.entities:
            entity.draw(client.screen)
        chat_menu.draw(client.screen)
        hud.draw(client.screen)
    if game.actual_menu is not None:
        game.actual_menu.draw(client.screen)
    client.clock.tick(120)
    pygame.display.update()
pygame.quit()
