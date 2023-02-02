import enum

import pygame

from utils.inputs.controls import Types, Sources, Inputs, Input


def load_controllers():
    return [Controller(pygame.joystick.Joystick(i), Sources.controller) for i in range(pygame.joystick.get_count())]


class Controls(enum.Enum):
    right = {"keyboard": {"pygame_code": pygame.K_RIGHT}, "controller": {"axis": 0, "value": 1}}
    left = {"keyboard": {"pygame_code": pygame.K_LEFT}, "controller": {"axis": 0, "value": -1}}
    down = {"keyboard": {"pygame_code": pygame.K_DOWN}, "controller": {"axis": 1, "value": 1}}
    up = {"keyboard": {"pygame_code": pygame.K_UP}, "controller": {"axis": 1, "value": -1}}
    a = {"keyboard": {"pygame_code": pygame.K_a}, "controller": {"button": 0}}


class Events(enum.Enum):
    a = {"keyboard": {"key": 97, "pygame_code": pygame.K_a}, "controller": {"button": 0}}
    b = {"keyboard": {"key": 98, "pygame_code": pygame.K_b}, "controller": {"button": 1}}
    y = {"keyboard": {"key": 121, "pygame_code": pygame.K_y}, "controller": {"button": 3}}
    x = {"keyboard": {"key": 120, "pygame_code": pygame.K_x}, "controller": {"button": 2}}
    dipad_d = {"keyboard": {"key": 115, "pygame_code": pygame.K_s}, "controller": {"button": 12}}
    dipad_u = {"keyboard": {"key": 122, "pygame_code": pygame.K_z}, "controller": {"button": 11}}
    dipad_r = {"keyboard": {"key": 113, "pygame_code": pygame.K_q}, "controller": {"button": 13}}
    dipad_l = {"keyboard": {"key": 100, "pygame_code": pygame.K_d}, "controller": {"button": 14}}
    trigger_l = {"keyboard": {"key": 99, "pygame_code": pygame.K_c}, "controller": {"button": 9}}
    trigger_r = {"keyboard": {"key": 118, "pygame_code": pygame.K_v}, "controller": {"button": 10}}


class Mouse(enum.Enum):
    left = {"mouse": {"key": 1}}


class Controller:
    def __init__(self, source, source_type):
        self.source = source
        self.source_type: Sources = source_type

    # def axis_transformer(axis, axis_trigger_value):
    #     return round(source.get_axis(axis) * 100 / 5) * 5 / 100 * axis_trigger_value > 0

    def transformer(self, control, up=False):
        if "axis" in control.value["controller"]:
            if round(self.source.get_axis(control.value["controller"]["axis"]) * 100 / 5) * 5 / 100 * \
                    control.value["controller"]["value"] > 0:
                return control.value["keyboard"]["pygame_code"]
        elif "button" in control.value["controller"]:
            if self.source.get_button(control.value["controller"]["button"]):
                return control.value["keyboard"]["pygame_code"]
            elif up:
                return control.value["keyboard"]["pygame_code"]

    def get_active_controls(self, keys):
        active_controls = []
        for control in Controls:
            if keys[control.value["keyboard"]["pygame_code"]] is True:
                active_controls.append(control.value["keyboard"]["pygame_code"])
            elif self.source is not None:
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

    @staticmethod
    def get_up_event_mouse(events):
        event_controls = []
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                for control in Mouse:
                    if event.button == control.value["mouse"]["key"]:
                        event_controls.append(control.value["mouse"]["key"])
        return event_controls
