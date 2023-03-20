import pygame

from util.input.controls import Sources, ControlsEventTypes, Event, Controls, Mouse, Inputs


def load_controllers():
    return [Controller(Sources.controller, pygame.joystick.Joystick(i)) for i in range(pygame.joystick.get_count())]


class Controller:
    def __init__(self, source_type, source=None):
        if source_type == Sources.controller and source is None:
            raise ValueError("Controller source must be specified")
        self.source = source
        self.source_type: Sources = source_type

    def transformer(self, control, up=False):
        if control.has_axis():
            if round(self.source.get_axis(control.get_axis()) * 100 / 5) * 5 / 100 * control.get_value() > 0:
                return control.get_code()
        elif control.has_button():
            if self.source.get_button(control.get_code()):
                return control.get_code()
            elif up:
                return control.get_code()

    def get_active_controls(self, keys):
        active_controls = []
        for control in Controls:
            if keys[control.get_code()] is True:
                active_controls.append(control.get_code())
            elif self.source is not None:
                transform = self.transformer(control)
                if transform is not None:
                    active_controls.append(transform)
        return active_controls

    def get_event_controls(self, incoming_events):
        inputs = Inputs()
        for event in incoming_events:
            inputs.raw_add(event)
            # print(input.raw_inputs)
            # Si la source est un clavier
            if self.source_type == Sources.keyboard and (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
                if Controls.key_exists(event.key):
                    if event.type == pygame.KEYDOWN:
                        inputs.add(Event(Controls.from_key(event.key).get_code(), ControlsEventTypes.DOWN, source=Sources.keyboard))
                    elif event.type == pygame.KEYUP:
                        inputs.add(Event(Controls.from_key(event.key).get_code(), ControlsEventTypes.UP, source=Sources.keyboard))
            # Si la source est une manette
            elif self.source_type == Sources.controller and (event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP):
                for control in Controls:
                    transform = self.transformer(control)
                    if transform is not None:
                        if event.type == pygame.JOYBUTTONDOWN:
                            inputs.add(Event(transform, ControlsEventTypes.DOWN, source=Sources.controller))
                        elif event.type == pygame.JOYBUTTONUP:
                            inputs.add(Event(transform, ControlsEventTypes.UP, source=Sources.controller))
            # Si la source est une souris
            elif self.source_type == Sources.mouse and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP):
                if Mouse.key_exists(event.button):
                    if event.type == pygame.MOUSEBUTTONUP:
                        inputs.add(Event(event.button, ControlsEventTypes.UP, source=Sources.mouse))
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        inputs.add(Event(event.button, ControlsEventTypes.DOWN, source=Sources.mouse))
        return inputs
