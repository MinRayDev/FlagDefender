import pygame

from core.menus.main_menu import MainMenu
from entities.livingentities.Mobtest import Mob
from entities.livingentities.entity_player import Player
from entities.particles.Particle import Particle
from entities.projectiles.Fireball import *
from entities.projectiles.Waterball import *
from core.game import Game

pygame.init()

game = Game()
Game.instance = game
pygame.display.set_caption("UwU")


run = True
player = Player(200, 200, game.actual_world)
controller = game.controllers[0]
Mob(300, 300, game.actual_world)
game.actual_menu = MainMenu()
while run:
    t = pygame.event.get()
    for event in t:
        if event.type == pygame.QUIT:
            run = False
    keys = controller.get_active_controls(pygame.key.get_pressed())
    u_events = controller.get_up_event_controls(t)
    d_events = controller.get_down_event_controls(t)
    m_events = controller.get_up_event_mouse(t)
    if game.actual_menu is not None:
        game.screen.fill((35, 39, 42))
        game.actual_menu.activity(m_events=m_events)
        if game.actual_menu is not None:
            game.actual_menu.draw(game.screen)
    else:
        game.screen.fill((0, 0, 0))

        if pygame.K_a in d_events:
            game.actual_world.entities.append(Fireball(player.x, player.y, player))
        if pygame.K_b in d_events:
            game.actual_world.entities.append(Waterball(player.x, player.y, player))

        if pygame.K_x in d_events:
            game.actual_world.entities.append(Particle(player.x, player.y, player.world, player.facing))

        for elem in game.queue:
            del game.queue[game.queue.index(elem)]
            game.actual_world.entities.append(elem)
        for entity in game.actual_world.entities:
            entity.activity(keys=keys, u_events=u_events, d_events=d_events)
            entity.draw(game.screen)

    if game.online:
        game.game_websocket.update("")
    pygame.display.update()
    pygame.time.delay(16)
pygame.quit()
