import pygame

from entities.livingentities.entity_player import PlayerEntity


class Player:
    def __init__(self, controller, world):
        self.entity = PlayerEntity(0, 0, world)
        self.controller = controller
        self.keys = []
        self.events = []
        self.inventory = {}  # key: item, value: count

    def get_controls(self, events):
        for control in self.controller.get_active_controls(pygame.key.get_pressed()):
            if control not in self.keys:
                self.keys.append(control)
        for event in self.controller.get_event_controls(events):
            if event not in self.events:
                self.events.append(event)

    def reset_queues(self):
        self.keys = []
        self.events = []

    def get_event(self, code, type_):
        for event in self.events:
            if event.code == code and event.type == type_:
                return True
        return False

    def get_inventory(self):
        return self.inventory

    def add_inventory(self, material, count: int = 1):
        if material in self.inventory:
            self.inventory[material] = self.inventory[material] + count
        else:
            self.inventory[material] = count
