import enum
import time

from core.ingame.item.item_type import ItemType



class MessageType(enum.IntEnum):
    SELF = 0  # joueur
    ONLINE = 1  # autre joueurs online/duo
    GAME = 2  # Annonce du jeu (ex: nouvelle vague)
    CLIENT = 3  # Annonce du client (ex: warn, information controles)
    SERVER = 4


class Message:
    def __init__(self, content: str, author: str, message_type: MessageType):
        self.content: str = content
        self.author: str = author
        self.type: MessageType = message_type
        self.created_time = time.time()


class Chat:
    def __init__(self):
        self.messages = []
        self.messages_to_draw = []
        self.client_messages = []

    def __len__(self):
        return len(self.messages)

    def write_message(self, message: Message):
        self.messages.insert(0, message)
        if len(self) > 10:
            self.messages.pop(10)

    def write(self, content: str, message_type: MessageType, author: str = None):
        if author is None and (message_type == MessageType.ONLINE):
            raise ValueError("Aucun author n'est spécifié")
        elif author is None and (message_type == MessageType.GAME):
            author = "(Game)"
        elif author is None and (message_type == MessageType.CLIENT):
            author = "(Client)"
        elif author is None and (message_type == MessageType.SELF):
            author = "(Moi)"
        elif message_type == MessageType.ONLINE:
            author = f"({author})"
        self.write_message(Message(content, author, message_type))


def execute(string: str):
    from util.instance import get_game
    if string.startswith("/"):
        string = string[1:]
        cmd = string.split(" ")[0]
        args = [arg for arg in string.split(" ")[1:]]
        try:
            exec("Commands." + cmd + f"({args})")
        except NameError:
            get_game().chat.write("command unknown", MessageType.GAME)


def is_command(string: str):
    return string.startswith("/")


def complete(word: str, tab_index: int) -> str:
    return ItemType.get_name_start(word, tab_index)


def cmd_complete(word: str, tab_index: int) -> str:
    from core.chat.commands import Commands, OnlineCommands
    i = 0
    for var in list(vars(Commands)) + list(vars(OnlineCommands)):
        if not var.startswith("__"):
            if var.startswith(word.lstrip("/")) and i == tab_index:
                return "/" + var
            i += 1

