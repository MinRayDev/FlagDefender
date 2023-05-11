import enum
import time

from core.ingame.item.item_type import ItemType

registered_entities = []
registered_commands = []
registered_items = []


class MessageType(enum.IntEnum):
    """Class representing different types of messages.

        Extend `IntEnum`.
        :cvar SELF: Message type for when the message comes from the client's player (The player sent a message).
        :cvar ONLINE: Message type for when the message comes from one of the players on the server (A message from another player online).
        :cvar GAME: Message type for when the message comes from the game (An information from the game).
        :cvar CLIENT: Message type for when the message comes from the client (On error from the server).
        :cvar SERVER: Message type for when the message comes from the server (On error from the server).

    """
    SELF = 0
    ONLINE = 1
    GAME = 2
    CLIENT = 3
    SERVER = 4


class Message:
    """Class 'Message'.

        This class represents a message and would be used in case of the game chat.

        :ivar content: Content of the message.
        :type content: str.
        :ivar author: Author of the message.
        :type author: str.
        :ivar type: Type of the message.
        :type type: MessageType.
        :ivar created_time: Timestamp when the message has been created.
        :type created_time: float.

    """
    content: str
    author: str
    type: MessageType
    created_time: float

    def __init__(self, content: str, author: str, message_type: MessageType):
        """Constructor function for Message class.

            :param content: Content of the message.
            :type content: str.
            :param author: Author of the message.
            :type author: str.
            :param message_type: Type of the message.
            :type message_type: str.

        """
        self.content = content
        self.author = author
        self.type = message_type
        self.created_time = time.time()


class Chat:
    """Class 'Message'.

        This class represents a message and would be used in case of the game chat.

        :ivar messages: List of messages (Without commands).
        :type messages: list[Message].
        :ivar client_messages: List of client's messages (It's like a message history).
        :type client_messages: list[Message].

    """
    messages: list[Message]
    client_messages: list[Message]

    def __init__(self):
        """Constructor function for Chat class."""
        self.messages = []
        self.client_messages = []

    def __len__(self) -> int:
        """Return number of messages."""
        return len(self.messages)

    def write_message(self, message: Message) -> None:
        """Add a message in the message list.

            Add the 'message' in the message list and if the length of the message list is above 10 we remove the last message of the list.

            :param message: Message to add.
            :type message: Message.

        """
        self.messages.insert(0, message)
        if len(self) > 10:
            self.messages.pop(10)

    def write(self, content: str, message_type: MessageType, author: str = None) -> None:
        """Add a message in the message list.

            Add a Message with content, message_type and author.
            'author' param is only required if the message type is 'ONLINE'.

            :param content: Content of the message.
            :type content: str.
            :param message_type: Type of the message.
            :type message_type: MessageType.
            :param author: Author of the message (If required).
            :type author: str.

            :raise ValueError: When the message type is 'ONLINE' and the author is not specified.
        """
        match message_type:
            case MessageType.ONLINE:
                if author is None:
                    raise ValueError("No author is specified")
                else:
                    author = f"({author})"
            case MessageType.GAME:
                author = "(Game)"
            case MessageType.CLIENT:
                author = "(Client)"
            case MessageType.SELF:
                author = "(Me)"
        self.write_message(Message(content, author, message_type))


def item_complete(word: str, tab_index: int) -> str:
    """Complete a word.

        Complete the param 'word' if it's started with the same letters as a name of an Item.

        :param word: Word to complete.
        :type word: str.
        :param tab_index: Number of tab pressed by the player.
        :type tab_index: int

        :return: The complete word (if possible).
        :rtype: str.

    """
    return ItemType.get_name_start(word.lower(), tab_index)


def entity_complete(word: str, tab_index: int) -> str:
    """Complete a word.

        Complete the param 'word' if it's started with the same letters as an entity in the list 'registered_entities'.
        Entities are registered in the beginning of the execution of the program with decorators.
        :param word: Word to complete.
        :type word: str.
        :param tab_index: Number of tab pressed by the player.
        :type tab_index: int

        :return: The complete word (if possible).
        :rtype: str.

    """
    i: int = 0
    for entity in registered_entities:
        if entity.__name__.lower().startswith(word.lower()):
            if tab_index == i:
                return entity.__name__
            i += 1


def cmd_complete(word: str, tab_index: int) -> str:
    """Complete a word.

        Complete the param 'word' if it's started with the same letters as a command in the object 'Command'.
        :param word: Word to complete.
        :type word: str.
        :param tab_index: Number of tab pressed by the player.
        :type tab_index: int

        :return: The complete word (if possible).
        :rtype: str.

    """
    from core.chat.commands import Commands
    i = 0
    temp = []
    for var in list(vars(Commands)):
        if not var.startswith("__") and var.startswith(word.lstrip("/")):
            temp.append(var)
    for var in temp:
        if i == tab_index:
            return "/" + var
        i += 1


def get_cmd_tab_index(word: str) -> int:
    """Returns the number olf tab pressed by the player in the case of a command.

        :param word: Word to complete.
        :type word: str.

        :return: Number of tab pressed.
        :rtype: int.

    """
    from core.chat.commands import Commands
    temp = []
    for var in list(vars(Commands)):
        if not var.startswith("__") and var.startswith(word.lstrip("/")):
            temp.append(var)
    return len(temp)


def entity_register(entity_class) -> type:
    """Registers a new entity class in the list 'registered_entities'.

        This function is called automatically by the program when the entities object's modules are imported. We use here decorators to register the entities.

        :param entity_class: Entity class.
        :type entity_class: type.

        :return: Entity class.
        :type: type.

    """
    registered_entities.append(entity_class)
    return entity_class


class Command:
    """Class 'Command'.

        :ivar text: Text content of a command.
        :type text: str.

    """
    def __init__(self, text: str):
        """Constructor function for the Command class.

            :param text: Text content of the command.
            :type text: str.

        """
        self.text = text

    @staticmethod
    def is_command(message: str) -> bool:
        """Return if a message's content is a function.

            :param message: Message's content to check.
            :type message: str.

            :return: True if message's content start with a "/" else False.
            :rtype: bool.

        """
        return message.startswith("/")

    @staticmethod
    def execute(message: str) -> None:
        """Execute a function with its name.

            We use here the 'exec' function, it can return any exception depends on what was passed in.

            :param message: Message's content to execute.
            :type message: str.

        """
        from util.instance import get_game
        if Command.is_command(message):
            string = message[1:]
            cmd = string.split(" ")[0]
            # Here we split arguments of the command (an argument is a part of the command separated by a " " and which is not the command itself
            args = [arg for arg in string.split(" ")[1:]]
            try:
                exec("Commands." + cmd + f"({args})")
            except Exception as e:
                get_game().chat.write("Unknow command", MessageType.GAME)
