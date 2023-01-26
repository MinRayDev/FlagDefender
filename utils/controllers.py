import enum

import pygame


def load_controllers():
    return [Controller(pygame.joystick.Joystick(i)) for i in range(pygame.joystick.get_count())]


class Controls(enum.Enum):
    right = {"keyboard": {"pygame_code": pygame.K_RIGHT}, "controller": {"axis": 0, "value": 1}}
    left = {"keyboard": {"pygame_code": pygame.K_LEFT}, "controller": {"axis": 0, "value": -1}}
    down = {"keyboard": {"pygame_code": pygame.K_DOWN}, "controller": {"axis": 1, "value": 1}}
    up = {"keyboard": {"pygame_code": pygame.K_UP}, "controller": {"axis": 1, "value": -1}}
    a = {"keyboard": {"pygame_code": pygame.K_a}, "controller": {"button.py": 0}}


class Events(enum.Enum):
    a = {"keyboard": {"key": 97, "pygame_code": pygame.K_a}, "controller": {"button.py": 0}}
    b = {"keyboard": {"key": 98, "pygame_code": pygame.K_b}, "controller": {"button.py": 1}}
    y = {"keyboard": {"key": 121, "pygame_code": pygame.K_y}, "controller": {"button.py": 3}}
    x = {"keyboard": {"key": 120, "pygame_code": pygame.K_x}, "controller": {"button.py": 2}}
    dipad_d = {"keyboard": {"key": 115, "pygame_code": pygame.K_s}, "controller": {"button.py": 12}}
    dipad_u = {"keyboard": {"key": 122, "pygame_code": pygame.K_z}, "controller": {"button.py": 11}}
    dipad_r = {"keyboard": {"key": 113, "pygame_code": pygame.K_q}, "controller": {"button.py": 13}}
    dipad_l = {"keyboard": {"key": 100, "pygame_code": pygame.K_d}, "controller": {"button.py": 14}}
    trigger_l = {"keyboard": {"key": 99, "pygame_code": pygame.K_c}, "controller": {"button.py": 9}}
    trigger_r = {"keyboard": {"key": 118, "pygame_code": pygame.K_v}, "controller": {"button.py": 10}}


class Mouse(enum.Enum):
    left = {"mouse": {"key": 1}}


class Controller:
    def __init__(self, joystick=None):
        self.joystick = joystick

    def transformer(self, control, up=False):
        if "axis" in control.value["controller"]:
            if round(self.joystick.get_axis(control.value["controller"]["axis"]) * 100 / 5) * 5 / 100 * \
                    control.value["controller"]["value"] > 0:
                return control.value["keyboard"]["pygame_code"]
        elif "button.py" in control.value["controller"]:
            if self.joystick.get_button(control.value["controller"]["button.py"]):
                return control.value["keyboard"]["pygame_code"]
            elif up:
                return control.value["keyboard"]["pygame_code"]

    def get_active_controls(self, keys):
        active_controls = []
        for control in Controls:
            if keys[control.value["keyboard"]["pygame_code"]] is True:
                active_controls.append(control.value["keyboard"]["pygame_code"])
            elif self.joystick is not None:
                transform = self.transformer(control)
                if transform is not None:
                    active_controls.append(transform)
        return active_controls

    def get_down_event_controls(self, events):
        event_controls = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                for control in Events:
                    if event.key == control.value["keyboard"]["key"]:
                        event_controls.append(control.value["keyboard"]["pygame_code"])
            elif event.type == pygame.JOYBUTTONDOWN:
                for control in Events:
                    transform = self.transformer(control)
                    if transform is not None:
                        event_controls.append(self.transformer(control))
        return event_controls

    def get_up_event_controls(self, events):
        event_controls = []
        for event in events:
            if event.type == pygame.KEYUP:
                for control in Events:
                    if event.key == control.value["keyboard"]["key"]:
                        event_controls.append(control.value["keyboard"]["pygame_code"])
            elif event.type == pygame.JOYBUTTONUP:
                for control in Events:
                    transform = self.transformer(control, True)
                    if transform is not None:
                        event_controls.append(transform)
        return event_controls

    @classmethod
    def get_down_event_mouse(cls, events):
        event_controls = []
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for control in Mouse:
                    if event.button == control.value["mouse"]["key"]:
                        event_controls.append(control.value["mouse"]["key"])
        return event_controls

    @classmethod
    def get_up_event_mouse(cls, events):
        event_controls = []
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                for control in Mouse:
                    if event.button == control.value["mouse"]["key"]:
                        event_controls.append(control.value["mouse"]["key"])
        return event_controls
