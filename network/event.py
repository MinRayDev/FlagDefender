from __future__ import annotations

import enum


class EventType(enum.IntEnum):
    CHAT_MESSAGE = 0
    ENTITY_TELEPORTATION = 1
    ENTITY_MOVEMENT = 2
    ENTITY_SPAWN = 3
    NEW_PLAYER = 1000
    SPELL = 5000
    ATTACK = 5001


class Event:
    def __init__(self, event_type: EventType, content: dict):
        self.type = event_type
        self.content = content

    def to_json(self) -> dict:
        return {"event_type": self.type.value, "content": self.content}

    @staticmethod
    def from_json(self, json_dict) -> Event:
        return Event(json_dict["event_type"], json_dict["content"])


class ChatEvent(Event):
    def __init__(self, message: str, author_name: str):
        super().__init__(EventType.CHAT_MESSAGE, {"message": message, "author": author_name})
        self.author_name = author_name

    @staticmethod
    def from_json(self, json_dict) -> Event:
        return ChatEvent(json_dict["content"]["message"], json_dict["content"]["author"])
