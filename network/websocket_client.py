import atexit
import threading
import uuid
from time import sleep
import websocket

nonce = str(uuid.uuid4())


def on_open(ws):
    print(">>>>>>Connected")
    ws.send("hi")


def on_message(message):
    print("Got: {}".format(message))
    if "UWU" in str(message):
        return


def on_close(close_status_code, close_msg):
    print(">>>>>>CLOSED")


def on_pong(response):
    print("PONG: {}".format(response))
    if response == nonce.encode("utf-8"):
        return
    raise Exception("Invalid pong contents.")


class WsClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ws = websocket.WebSocketApp(
            f"ws://{str(self.host)}:{str(self.port)}/echo",
            on_open=on_open,
            on_message=on_message,
            on_close=on_close,
            on_ping=lambda x, y: print("Ping! {}".format(y)),
            on_pong=on_pong
        )
        self.frame_count = 0
        self.frames = 3

    def run(self):
        thread_ = threading.Thread(target=self.ws.run_forever, args=(None, None, 20, 5, nonce), daemon=True)
        thread_.start()
        atexit.register(self.ws.close)
        conn_timeout = 50
        while self.ws.sock is None or (not self.ws.sock.connected and conn_timeout):
            sleep(.1)
            conn_timeout -= 1

    def update(self, infos):
        self.frame_count += 1
        if self.frame_count > self.frames:
            self.frame_count = 0
            self.ws.send(infos)
