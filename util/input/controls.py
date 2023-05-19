from __future__ import annotations
import enum
from typing import Generator, Any, Optional

import pygame
from pygame.event import EventType


class Sources(enum.Enum):
    """Class 'Sources'.

        Extends 'Enum'.
        :cvar keyboard: The keyboard sources.
        :cvar mouse: The mouse sources.


    """
    keyboard = 0
    mouse = 1


class Controls(enum.Enum):
    """Class 'Controls'.

        Extends 'Enum'.

    """
    right_walk = {"keyboard": {"key": 1073741903, "code": pygame.K_RIGHT}}
    left_walk = {"keyboard": {"key": 1073741904, "code": pygame.K_LEFT}}
    run = {"keyboard": {"key": 121, "code": pygame.K_y}}
    attack_1 = {"keyboard": {"key": 97, "code": pygame.K_a}}
    attack_2 = {"keyboard": {"key": 98, "code": pygame.K_b}}
    attack_3 = {"keyboard": {"key": 113, "code": pygame.K_q}}
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

    def get_code(self) -> int:
        """Get the code of the control.

            :return: The code of the control.
            :rtype: int.

        """
        return self.value["keyboard"]["code"]

    def get_key(self) -> int:
        """Get the key of the control.

            :return: The key of the control.
            :rtype: int.

        """
        return self.value["keyboard"]["key"]

    @staticmethod
    def key_exists(key: int) -> bool:
        """Check if the key exists.

            :param key: The key to check.
            :type key: int.

            :return: True if the key exists, False otherwise.
            :rtype: bool.

        """
        for control in Controls:
            if key == control.value["keyboard"]["key"]:
                return True
        return False

    @staticmethod
    def code_exists(code: int) -> bool:
        """Check if the code exists.

            :param code: The code to check.
            :type code: int.

            :return: True if the code exists, False otherwise.
            :rtype: bool.

        """
        for control in Controls:
            if code == control.value["keyboard"]["code"]:
                return True
        return False

    @staticmethod
    def from_code(code: int) -> Controls:
        """Get the control from the code.

            :param code: The code to get the control from.
            :type code: int.

            :return: The control from the code.
            :rtype: Controls.

        """
        for control in Controls:
            if code == control.value["keyboard"]["code"]:
                return control

    @staticmethod
    def from_key(key: int) -> Controls:
        """Get the control from the key.

            :param key: The key to get the control from.
            :type key: int.

            :return: The control from the key.
            :rtype: Controls.
        """
        for control in Controls:
            if key == control.value["keyboard"]["key"]:
                return control

    @staticmethod
    def change_key(key: int, code: int) -> None:
        """Change the key of the control.

            :param key: The key to change.
            :type key: int.
            :param code: The code to change.
            :type code: int.

        """
        from util import settings, files
        for control in Controls:
            if code == control.value["keyboard"]["code"]:
                control.value["keyboard"]["key"] = key
        settings.write_settings(files.get_settings_file())


class Mouse(enum.Enum):
    """Class 'Mouse'.

        Extends 'Enum'.

    """
    left = {"mouse": {"key": 1}}

    def get_key(self) -> int:
        """Get the key of the control.

            :return: The key of the control.
            :rtype: int.

        """
        return self.value["mouse"]["key"]

    @staticmethod
    def key_exists(key: int) -> bool:
        """Check if the key exists.

            :param key: The key to check.
            :type key: int.

            :return: True if the key exists, False otherwise.
            :rtype: bool.

        """
        for control in Mouse:
            if key == control.value["mouse"]["key"]:
                return True
        return False

    @staticmethod
    def from_key(key: int) -> Mouse:
        """Get the control from the key.

            :param key: The key to get the control from.
            :type key: int.

            :return: The control from the key.
            :rtype: Controls.
        """
        for control in Mouse:
            if key == control.value["mouse"]["key"]:
                return control


class Inputs:
    """Class 'Inputs'.

        This class is used to store the inputs.

        :ivar inputs: The list of the inputs.
        :type inputs: list[Event].
        :ivar raw_inputs: The list of the raw inputs.
        :type raw_inputs: list[EventType].


    """

    inputs: list[Event]
    raw_inputs: list[EventType]

    def __init__(self):
        """Constructor of the class 'Inputs'."""
        self.inputs = []
        self.raw_inputs = []

    def __iter__(self):
        """Iterate over the inputs."""
        self.i = 0
        return self

    def __next__(self):
        """Get the next input."""
        if self.i < len(self.inputs):
            x = self.i
            self.i += 1
            return self.inputs[x]
        else:
            raise StopIteration

    def get_codes(self) -> Generator[Any, Any, None]:
        """Get the codes of the inputs.

            :return: The codes of the inputs.
            :rtype: Generator[Any, Any, None].

        """
        for input_ in self.inputs:
            yield input_.code

    def add(self, elem: Event) -> None:
        """Add an input to the list of the inputs.

            :param elem: The input to add.
            :type elem: Event.

        """
        self.inputs.append(elem)

    def raw_add(self, elem: EventType) -> None:
        """Add an input to the list of the raw inputs.

            :param elem: The input to add.
            :type elem: EventType.

        """
        self.raw_inputs.append(elem)

    def copy(self) -> Inputs:
        """Copy the inputs."""
        return self

    def __str__(self) -> str:
        """Get the string of the inputs."""
        return str(self.inputs)

    def __len__(self) -> int:
        """Get the length of the inputs."""
        return len(self.inputs)


class ControlsEventTypes(enum.Enum):
    """Class 'ControlsEventTypes'.

        Extends 'Enum'.

    """
    UP = 0
    DOWN = 1
    AXIS = 2


class Event:
    """Class 'Event'.

        This class is used to store an event.
        :ivar code: The code of the event.
        :type code: int.
        :ivar type: The type of the event.
        :type type: ControlsEventTypes.
        :ivar value: The value of the event.
        :type value: int.
        :ivar source: The source of the event.
        :type source: str.
    """
    code: int
    type: ControlsEventTypes
    value: Optional[int]
    source: Optional[Sources]

    def __init__(self, code: int, event_type: ControlsEventTypes, value: Optional[int] = None, source: Optional[Sources] = None):
        self.code = code
        self.type = event_type
        self.value = value
        self.source = source
