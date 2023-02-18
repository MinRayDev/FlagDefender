import pygame

from core.menus.impl.main_menu import MainMenu
from core.player import Player
from entities.livingentities.Mobtest import Mob
from entities.livingentities.entity_player import PlayerEntity
from entities.particles.Particle import Particle
from entities.projectiles.impl.fireball import *
from entities.projectiles.impl.trajectorytest import TrajBall
from entities.projectiles.impl.waterball import *
from utils import files
from utils.controllers import Controller
from utils.inputs.controls import *

pygame.init()
game = Game()
Game.instance = game
pygame.display.set_caption(game.name)
pygame.scrap.init()
pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
# player = PlayerEntity(200, 200, game.actual_world)

# Mob(1000, 0, game.actual_world)
# Spawner(500, 0, game.actual_world)
game.actual_menu = MainMenu()
last_update = -1
for controller in game.controllers:
    game.players.append(Player(controller, game.actual_world))
keyboard = Controller(Sources.keyboard, None)
if len(game.players) == 0:
    game.players.append(Player(keyboard, game.actual_world))
game.controllers.append(keyboard)
game.controllers.append(Controller(Sources.mouse, None))
game.main_player = game.players[0]
test: Entity = Entity(300, 300, r"C:\Users\Gekota\Documents\Dev\Python\Game\resources\sprites\palkia_test", game.actual_world, gravity=False)
game.actual_world.entities.append(test)
if not files.base_directory_exists():
    files.create_base_directory()
if not files.save_directory_exists():
    files.create_save_directory()
while game.run:
    t = pygame.event.get()
    for event in t:
        if event.type == pygame.QUIT:
            game.run = False
    if game.actual_menu is not None:
        for controller in game.controllers:
            events_ = controller.get_event_controls(t)
            for elem_ in events_:
                if elem_.type == EventTypes.UP:
                    game.actual_menu.add_queue(elem_)
            for elem_ in events_.raw_inputs:
                game.actual_menu.add_raw_queue(elem_)
    else:
        for player in game.players:
            player.get_controls(t)


    ## Game logic
    def game_update():
        if game.actual_menu is not None:
            game.actual_menu.activity()
        else:
            for elem in game.queue:
                del game.queue[game.queue.index(elem)]
                game.actual_world.entities.append(elem)
            for entity_ in game.actual_world.entities:
                if not isinstance(entity_, PlayerEntity):
                    entity_.activity()
                else:
                    for player_ in game.players:
                        if player_.entity == entity_:
                            if player_.get_event(pygame.K_a, EventTypes.DOWN):
                                game.actual_world.entities.append(
                                    Fireball(player_.entity.x, player_.entity.y, player_.entity))
                            if player_.get_event(pygame.K_b, EventTypes.DOWN):
                                game.actual_world.entities.append(
                                    Waterball(player_.entity.x, player_.entity.y, player_.entity))

                            if player_.get_event(pygame.K_x, EventTypes.DOWN):
                                game.actual_world.entities.append(
                                    TrajBall(player_.entity.x, player_.entity.y, player_.entity))
                            if player_.get_event(pygame.K_p, EventTypes.DOWN):
                                player_.entity.incline += 1
                            if player_.get_event(pygame.K_m, EventTypes.DOWN):
                                player_.entity.incline -= 1
                            player_.entity.activity(keys=player_.keys, events=player_.events)
                            player_.reset_queues()
                            break
        if game.online:
            game.game_websocket.update("")


    delta_time = (pygame.time.get_ticks() - last_update) / 1000.
    if delta_time > 1. / game.TPS:
        game_update()
        last_update = pygame.time.get_ticks()

    ## Rendering

    if game.actual_menu is not None:
        game.screen.fill((35, 39, 42))
        game.actual_menu.draw(game.screen)
    else:
        # Draw world
        game.screen.fill((0, 0, 0))

        for entity in game.actual_world.entities:
            entity.draw(game.screen)
    pygame.display.update()
    # pygame.time.delay(int(1/120))
pygame.quit()
