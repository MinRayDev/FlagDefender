import enum

import pygame


class Sources(enum.Enum):
    keyboard = 0
    mouse = 1


class Controls(enum.Enum):
    right_walk = {"keyboard": {"key": 1073741903, "code": pygame.K_RIGHT}}
    left_walk = {"keyboard": {"key": 1073741904, "code": pygame.K_LEFT}}
    run = {"keyboard": {"key": 121, "code": pygame.K_y}}
    attack_1 = {"keyboard": {"key": 97, "code": pygame.K_a}}
    attack_2 = {"keyboard": {"key": 98, "code": pygame.K_b}}
    attack_3 = {"keyboard": {"key": 113, "code": pygame.K_q}}
    attack_4 = {"keyboard": {"key": 100, "code": pygame.K_d}}
    incline_up = {"keyboard": {"key": 1073741906, "code": pygame.K_UP}}
    incline_down = {"keyboard": {"key": 1073741905, "code": pygame.K_DOWN}}
    spell_1 = {"keyboard": {"key": 99, "code": pygame.K_c}}
    spell_2 = {"keyboard": {"key": 118, "code": pygame.K_v}}
    spell_3 = {"keyboard": {"key": 110, "code": pygame.K_n}}
    use = {"keyboard": {"key": 114, "code": pygame.K_r}}
    drop = {"keyboard": {"key": 119, "code": pygame.K_w}}
    inventory = {"keyboard": {"key": 101, "code": pygame.K_e}}

    return_ = {"keyboard": {"key": 13, "code": pygame.K_RETURN}, "register": True}
    esc = {"keyboard": {"key": 27, "code": pygame.K_ESCAPE}, "register": True}
    tab = {"keyboard": {"key": 9, "code": pygame.K_TAB}, "register": True}

    def get_code(self):
        return self.value["keyboard"]["code"]

    def get_key(self):
        return self.value["keyboard"]["key"]

    @staticmethod
    def key_exists(key):
        for control in Controls:
            if key == control.value["keyboard"]["key"]:
                return True
        return False

    @staticmethod
    def code_exists(code):
        for control in Controls:
            if code == control.value["keyboard"]["code"]:
                return True
        return False

    @staticmethod
    def from_code(code):
        for control in Controls:
            if code == control.value["keyboard"]["code"]:
                return control

    @staticmethod
    def from_key(key):
        for control in Controls:
            if key == control.value["keyboard"]["key"]:
                return control

    @staticmethod
    def change_key(key, code):
        from util import settings, files
        for control in Controls:
            if code == control.value["keyboard"]["code"]:
                control.value["keyboard"]["key"] = key
        settings.write_settings(files.get_settings_file())


class Mouse(enum.Enum):
    left = {"mouse": {"key": 1}}

    def get_key(self):
        return self.value["mouse"]["key"]

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


class ControlsEventTypes(enum.Enum):
    UP = 0
    DOWN = 1
    AXIS = 2


class Event:
    def __init__(self, code, event_type, value=None, source=None):
        self.code = code
        self.type = event_type
        self.value = value
        self.source = source
