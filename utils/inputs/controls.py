import enum

import pygame


class Sources(enum.Enum):
    keyboard = 0
    mouse = 1
    controller = 2


class Controls(enum.Enum):
    right = {"keyboard": {"key": None, "code": pygame.K_RIGHT}, "controller": {"axis": 0, "value": 1}}
    left = {"keyboard": {"key": None, "code": pygame.K_LEFT}, "controller": {"axis": 0, "value": -1}}
    down = {"keyboard": {"key": None, "code": pygame.K_DOWN}, "controller": {"axis": 1, "value": 1}}
    up = {"keyboard": {"key": None, "code": pygame.K_UP}, "controller": {"axis": 1, "value": -1}}
    a = {"keyboard": {"key": 97, "code": pygame.K_a}, "controller": {"button": 0}}
    b = {"keyboard": {"key": 98, "code": pygame.K_b}, "controller": {"button": 1}}
    y = {"keyboard": {"key": 121, "code": pygame.K_y}, "controller": {"button": 3}}
    x = {"keyboard": {"key": 120, "code": pygame.K_x}, "controller": {"button": 2}}
    c = {"keyboard": {"key": 99, "code": pygame.K_c}}
    d = {"keyboard": {"key": 100, "code": pygame.K_d}}
    e = {"keyboard": {"key": 101, "code": pygame.K_e}}
    f = {"keyboard": {"key": 102, "code": pygame.K_f}}
    g = {"keyboard": {"key": 103, "code": pygame.K_g}}
    h = {"keyboard": {"key": 104, "code": pygame.K_h}}
    i = {"keyboard": {"key": 105, "code": pygame.K_i}}
    j = {"keyboard": {"key": 106, "code": pygame.K_j}}
    k = {"keyboard": {"key": 107, "code": pygame.K_k}}
    l_ = {"keyboard": {"key": 108, "code": pygame.K_l}}
    m = {"keyboard": {"key": 109, "code": pygame.K_m}}
    n = {"keyboard": {"key": 110, "code": pygame.K_n}}
    o = {"keyboard": {"key": 111, "code": pygame.K_o}}
    p = {"keyboard": {"key": 112, "code": pygame.K_p}}
    q = {"keyboard": {"key": 113, "code": pygame.K_q}}
    r = {"keyboard": {"key": 114, "code": pygame.K_r}}
    s = {"keyboard": {"key": 115, "code": pygame.K_s}}
    t = {"keyboard": {"key": 116, "code": pygame.K_t}}
    u = {"keyboard": {"key": 117, "code": pygame.K_u}}
    v = {"keyboard": {"key": 118, "code": pygame.K_v}}
    w = {"keyboard": {"key": 119, "code": pygame.K_w}}
    z = {"keyboard": {"key": 122, "code": pygame.K_z}}
    dipad_d = {"keyboard": {"key": 115, "code": pygame.K_s}, "controller": {"button": 12}}
    dipad_u = {"keyboard": {"key": 122, "code": pygame.K_z}, "controller": {"button": 11}}
    dipad_r = {"keyboard": {"key": 113, "code": pygame.K_q}, "controller": {"button": 13}}
    dipad_l = {"keyboard": {"key": 100, "code": pygame.K_d}, "controller": {"button": 14}}
    trigger_l = {"keyboard": {"key": 99, "code": pygame.K_c}, "controller": {"button": 9}}
    trigger_r = {"keyboard": {"key": 118, "code": pygame.K_v}, "controller": {"button": 10}}

    def get_code(self):
        return self.value["keyboard"]["code"]

    def has_button(self):
        return "button" in self.value["controller"]

    def get_button(self):
        return self.value["controller"]["button"]

    def has_axis(self):
        return "axis" in self.value["controller"]

    def get_axis(self):
        return self.value["controller"]["axis"]

    def get_value(self):
        return self.value["controller"]["value"]

    @staticmethod
    def key_exists(key):
        for control in Controls:
            if key == control.value["keyboard"]["key"]:
                return True
        return False

    @staticmethod
    def from_key(key):
        for control in Controls:
            if key == control.value["keyboard"]["key"]:
                return control


class Mouse(enum.Enum):
    left = {"mouse": {"key": 1}}

    @staticmethod
    def key_exists(key):
        for control in Mouse:
            if key == control.value["mouse"]["key"]:
                return True
        return False

    @staticmethod
    def from_key(key):
        for control in Mouse:
            if key == control.value["mouse"]["key"]:
                return control


class Inputs:
    def __init__(self):
        self.inputs = []
        self.raw_inputs = []

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self.inputs):
            x = self.i
            self.i += 1
            return self.inputs[x]
        else:
            raise StopIteration

    def get_codes(self):
        for input_ in self.inputs:
            yield input_.code

    def add(self, elem):
        self.inputs.append(elem)

    def raw_add(self, elem):
        self.raw_inputs.append(elem)

    def copy(self):
        return self

    def __str__(self):
        return str(self.inputs)

    def __len__(self):
        return len(self.inputs)


class EventTypes(enum.Enum):
    UP = 0
    DOWN = 1
    AXIS = 2


class Event:
    def __init__(self, code, event_type, value=None, source=None):
        self.code = code
        self.type = event_type
        self.value = value
        self.source = source
# import string
# for i, char in enumerate(string.ascii_lowercase):
#     print('a = {"keyboard": {"key": 97, "code": pygame.K_a}}'.replace("a ", char + " ").replace("97", str(97+i)).replace("K_a", "K_" + char))