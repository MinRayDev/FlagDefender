import enum

import pygame

from utils.Test import setter


class Sources(enum.Enum):
    keyboard = 0
    mouse = 1
    controller = 2


class Types(enum.Enum):
    press = 0
    up_event = 1
    down_event = 2
    axis_press = 3
    axis_event = 4


class Input:
    def __init__(self, name, code, value):
        self.source = None
        self.type = None  # event, press
        self.name = name
        self.value = value  # {} ce qui va être check if "keyboard" in values and keys[values["keyboard"]] or
        self.code = code  # ce qui va être check (if code in list: la key est press/dans event)

    def build(self, type_: Types, source: Sources, value=None):
        self.type: Types = type_
        self.source: Sources = source  # keyboard, mouse, controller
        return self


class Inputs(enum.Enum):
    down = {"code": 0, "type": "axis_bool", "values": {"keyboard": (-1, pygame.K_DOWN), "controller": (1, 1)}}
    up = {"code": 1, "type": "axis_bool", "values": {"keyboard": (-1, pygame.K_UP), "controller": (1, -1)}}
    right = {"code": 2, "type": "axis_bool", "values": {"keyboard": (-1, pygame.K_UP), "controller": (0, 1)}}
    left = {"code": 3, "type": "axis_bool", "values": {"keyboard": (-1, pygame.K_UP), "controller": (0, -1)}}
    a = {"code": 100, "type": "button",
         "values": {"keyboard": (97, pygame.K_a), "mouse": 2, "controller": 0}}  # axis: 0 à 1, axis_bool: 0 ou 1

    def get_code(self):
        return self.value["code"]

    def get_type(self):
        return self.value["type"]

    def get_value(self, source: Sources):
        return self.value["values"][str(source.name)]


def test(keys, code):
    for key_ in keys:
        if key_.code == code:
            return True
    return False
