import pygame
from pygame.event import EventType
from pygame.key import ScancodeWrapper

from util.input.controls import Sources, ControlsEventTypes, Event, Controls, Mouse, Inputs


class Controller:
    """Class 'Controller'.

        :ivar source_type: The source type of the controller.
        :type source_type: Sources.

    """
    source_type: Sources

    def __init__(self, source_type: Sources):
        """Constructor of the class 'Controller'.

            :param source_type: The source type of the controller.
            :type source_type: Sources.
        """
        self.source_type = source_type

    def get_event_controls(self, incoming_events: list[EventType]) -> Inputs:
        """Get the controls from the incoming events.

            :param incoming_events: The incoming events.
            :type incoming_events: list[EventType].

            :return: The controls from the incoming events.
            :rtype: Inputs.

        """
        inputs: Inputs = Inputs()
        for event in incoming_events:
            inputs.raw_add(event)
            # If the source is a keyboard
            if self.source_type == Sources.keyboard and (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
                if Controls.key_exists(event.key):
                    if event.type == pygame.KEYDOWN:
                        inputs.add(Event(Controls.from_key(event.key).get_code(), ControlsEventTypes.DOWN, source=Sources.keyboard))
                    elif event.type == pygame.KEYUP:
                        inputs.add(Event(Controls.from_key(event.key).get_code(), ControlsEventTypes.UP, source=Sources.keyboard))
            # If the source is a mouse
            elif self.source_type == Sources.mouse and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP):
                if Mouse.key_exists(event.button):
                    if event.type == pygame.MOUSEBUTTONUP:
                        inputs.add(Event(event.button, ControlsEventTypes.UP, source=Sources.mouse))
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        inputs.add(Event(event.button, ControlsEventTypes.DOWN, source=Sources.mouse))
        return inputs

    @classmethod
    def get_active_controls(cls, keys: ScancodeWrapper) -> list[int]:
        """Get the active controls from the keys.

            :param keys: The keys to get the active controls from.
            :type keys: ScancodeWrapper.

            :return: The active controls from the keys.
            :rtype: list[int].

        """
        active_controls: list[int] = []
        for control in Controls:
            if keys[control.get_key()] is True:
                active_controls.append(control.get_code())
        return active_controls
