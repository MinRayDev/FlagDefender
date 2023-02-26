import atexit
import json
import threading
import uuid
from time import sleep

import websocket

from core.chat.chat import MessageType
from network.event import EventType
from network.types import NetworkEntityTypes
from util.instance import get_game

nonce = str(uuid.uuid4())


# print(NetworkEntityTypes.from_json('{"value": 0, "class": PlayerEntity}'))

def first_contact(ws):
    ws.send(json.dumps({"event_type": EventType.ENTITY_SPAWN, "content": {"entity_type": NetworkEntityTypes.from_class(
        get_game().main_player.entity).get_value(),
                                                                           "entity": get_game().main_player.entity.to_json()}}))


def on_open(ws):
    print(">>>>>>Connected")
    first_contact(ws)


def on_message(ws, message):
    print("Got: {}".format(message))
    try:
        message_json = json.loads(message)
        if "event_type" in message_json and "content" in message_json:
            match message_json["event_type"]:
                case EventType.CHAT_MESSAGE:
                    print("New chat message: {}".format(message_json["content"]))
                    get_game().chat.write(message_json["content"], MessageType.ONLINE, "Test")
                case EventType.ENTITY_SPAWN:
                    print("New entity spawn: {}".format(message_json["content"]))
                    if get_game().get_entity_by_uuid(message_json["content"]["entity"]["uuid"]) is None:
                        get_game().queue.append(
                            NetworkEntityTypes.from_json(message_json["content"]["entity_type"]).get_class().from_json(
                                message_json["content"]["entity"]))
                    print("q", get_game().queue)
                case EventType.ENTITY_MOVEMENT:
                    get_game().get_entity_by_uuid(message_json["content"]["entity_id"]).x = message_json["content"]["x"]
                    get_game().get_entity_by_uuid(message_json["content"]["entity_id"]).y = message_json["content"]["y"]
                case EventType.NEW_PLAYER:
                    first_contact(ws)
    except Exception as e:
        print(e)


def on_close(close_status_code, close_msg):
    print(">>>>>>CLOSED")


def on_pong(ws, response):
    # print("PONG: {}".format(response))
    if response == nonce.encode("utf-8"):
        return
    raise Exception("Invalid pong contents.")


class WsClient:
    def __init__(self, host, port, client_id):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ws = None

    def run(self, party_id):
        self.ws = websocket.WebSocketApp(
            f"ws://{str(self.host)}:{str(self.port)}/echo?client_id={str(self.client_id)}&user_id={str(get_game().main_player.user_id)}&party_id={str(party_id)}",
            on_open=on_open,
            on_message=on_message,
            on_close=on_close,
            on_ping=lambda x, y: print("Ping! {}".format(y)),
            on_pong=on_pong
        )
        thread_ = threading.Thread(target=self.ws.run_forever, args=(None, None, 20, 5, nonce), daemon=True)
        thread_.start()
        atexit.register(self.ws.close)
        conn_timeout = 50
        while self.ws.sock is None or (not self.ws.sock.connected and conn_timeout):
            sleep(.1)
            conn_timeout -= 1

    def send(self, infos):
        self.ws.send(infos)

    def close(self):
        self.ws.close()

    def is_started(self):
        return self.ws.sock is not None

    def send_event(self, event, content):
        self.send(json.dumps({"event_type": event.value, "content": content}))
