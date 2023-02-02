import pygame

from core.menus.main_menu import MainMenu
from core.player import Player
from entities.livingentities.Mobtest import Mob
from entities.livingentities.entity_player import PlayerEntity
from entities.particles.Particle import Particle
from entities.projectiles.Fireball import *
from entities.projectiles.Waterball import *
from core.game import Game
from utils.controllers import Controller
from utils.inputs.controls import *

pygame.init()
# TODO; refaire controlles (transformer sans passer par clavier, faire queue des controlles par controllers)
game = Game()
Game.instance = game
pygame.display.set_caption(game.name)

TPS: float = 60
run = True
# player = PlayerEntity(200, 200, game.actual_world)

Mob(300, 300, game.actual_world)
game.actual_menu = MainMenu()
last_update = -1
keyboard = None
test = game.controllers + [keyboard]
for controller in game.controllers:
    game.players.append(Player([controller], game.actual_world))
if len(game.controllers) == 0:
    game.players.append(Player([Controller(None, Sources.keyboard)], game.actual_world))

while run:
    t = pygame.event.get()
    for event in t:
        if event.type == pygame.QUIT:
            run = False
    m_events = Controller.get_up_event_mouse(t)
    for player in game.players:
        player.get_controls(t)

    ## Game logic
    def game_update():
        if game.actual_menu is not None:
            game.actual_menu.activity(m_events=m_events)
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
                            if pygame.K_a in player_.d_events:
                                game.actual_world.entities.append(
                                    Fireball(player_.entity.x, player_.entity.y, player_.entity))
                            if pygame.K_b in player_.d_events:
                                game.actual_world.entities.append(
                                    Waterball(player_.entity.x, player_.entity.y, player_.entity))

                            if pygame.K_x in player_.d_events:
                                game.actual_world.entities.append(
                                    Particle(player_.entity.x, player_.entity.y, player_.entity.world,
                                             player_.entity.facing))
                            player_.entity.activity(keys=player_.keys, u_events=player_.u_events,
                                                    d_events=player_.d_events)
                            player_.reset_queues()
                            break
        if game.online:
            game.game_websocket.update("")


    delta_time = (pygame.time.get_ticks() - last_update) / 1000.
    if delta_time > 1. / TPS:
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
