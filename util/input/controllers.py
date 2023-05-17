import pygame

from util.input.controls import Sources, ControlsEventTypes, Event, Controls, Mouse, Inputs


class Controller:
    def __init__(self, source_type):
        self.source_type: Sources = source_type

    def get_event_controls(self, incoming_events) -> Inputs:
        inputs = Inputs()
        for event in incoming_events:
            inputs.raw_add(event)
            # Si la source est un clavier
            if self.source_type == Sources.keyboard and (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
                if Controls.key_exists(event.key):
                    if event.type == pygame.KEYDOWN:
                        inputs.add(Event(Controls.from_key(event.key).get_code(), ControlsEventTypes.DOWN, source=Sources.keyboard))
                    elif event.type == pygame.KEYUP:
                        inputs.add(Event(Controls.from_key(event.key).get_code(), ControlsEventTypes.UP, source=Sources.keyboard))
            # Si la source est une souris
            elif self.source_type == Sources.mouse and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP):
                if Mouse.key_exists(event.button):
                    if event.type == pygame.MOUSEBUTTONUP:
                        inputs.add(Event(event.button, ControlsEventTypes.UP, source=Sources.mouse))
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        inputs.add(Event(event.button, ControlsEventTypes.DOWN, source=Sources.mouse))
        return inputs

    @classmethod
    def get_active_controls(cls, keys):
        active_controls = []
        for control in Controls:
            if keys[control.get_key()] is True:
                active_controls.append(control.get_code())
        return active_controls
