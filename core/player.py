import pygame

from entities.livingentities.entity_player import PlayerEntity


class Player:
    def __init__(self, controllers, world):
        self.entity = PlayerEntity(200, 200, world)
        self.controllers = controllers
        self.keys = []
        self.u_events = []
        self.d_events = []

    def get_controls(self, events):
        for controller in self.controllers:
            for t in controller.get_active_controls(pygame.key.get_pressed()):
                if t not in self.keys:
                    self.keys.append(t)
            for t in controller.get_up_event_controls(events):
                if t not in self.u_events:
                    self.u_events.append(t)
            for t in controller.get_down_event_controls(events):
                if t not in self.d_events:
                    self.d_events.append(t)

    def reset_queues(self):
        self.keys = []
        self.u_events = []
        self.d_events = []
