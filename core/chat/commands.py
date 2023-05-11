import time

from core.chat.chat import MessageType, registered_entities
from util.instance import get_game
from util.world_util import teleport, give_item, summon


class Commands:
    """Command class is the class where all commands are stored."""
    @staticmethod
    def tp(args: list[str]) -> None:
        """Teleport a player from an x position to another x position.

            :param args: List of args.
            :type args: list[str].

        """
        if len(args) != 0 and str(args[0]).lstrip("-").isdigit():
            x: int = int(args[0])
            main_player_entity = get_game().current_level.main_player.entity
            if x is not None and -main_player_entity.world.size[0] <= x and x + main_player_entity.width <= main_player_entity.world.size[0]:
                teleport(main_player_entity, main_player_entity.world, x)
                get_game().chat.write(f"You have been teleported to x {args[0]}.", MessageType.GAME)
            else:
                get_game().chat.write("The x coordinates are invalid.", MessageType.GAME)
        else:
            get_game().chat.write("Argument 'x' is missing.", MessageType.GAME)

    @staticmethod
    def worldtp(args: list[str]) -> None:
        """Teleport a player from world to another one.

            :param args: List of args.
            :type args: list[str].

        """
        if len(args) != 0:
            for world in get_game().current_level.worlds:
                if args[0] == world.name:
                    teleport(get_game().current_level.main_player.entity, world, get_game().current_level.main_player.entity.x)
                    get_game().chat.write(f"You have been teleported to the world {args[0]}.", MessageType.GAME)
                    break
            else:
                get_game().chat.write(f"The world '{args[0]}' cannot be found.", MessageType.GAME)
        else:
            get_game().chat.write("Argument 'world' is missing.", MessageType.GAME)

    @staticmethod
    def give(args: list[str]) -> None:
        """Give an item to a player.

            :param args: List of args.
            :type args: list[str].

        """
        from core.ingame.item.item_type import ItemType
        if len(args) != 0:
            item_: str = args[0]
            amount: int = 1
            if len(args) == 2 and str(args[1]).isdigit():
                amount: int = int(args[1])
            if str(item_).isdigit():
                returned: bool = give_item(item_id=int(item_), amount=amount)
                get_game().chat.write(f"You received {str(amount)} {ItemType.get_by_id(int(item_))}.", MessageType.GAME)
            else:
                returned: bool = give_item(name=str(item_), amount=amount)
                get_game().chat.write(f"You received {str(amount)} {args[0]}.", MessageType.GAME)
            if not returned:
                get_game().chat.write(f"The item '{args[0]}' cannot be found.", MessageType.GAME)
        else:
            get_game().chat.write("Argument 'item' is missing.", MessageType.GAME)

    @staticmethod
    def summon(args) -> None:
        """Summon an entity.

            :param args: List of args.
            :type args: list[str].

        """
        if len(args) == 3:
            potential_entity_type: str = args[0]
            str_x: str = args[1]
            str_world: str = args[2]
            if str(str_x).lstrip("-").isdigit():
                x = int(str_x)
            else:
                get_game().chat.write("The x coordinates are invalid.", MessageType.GAME)
                return
            for temp_world in get_game().current_level.worlds:
                if str_world == temp_world.name:
                    world = temp_world
                    break
            else:
                get_game().chat.write(f"The world '{str_world}' cannot be found.", MessageType.GAME)
                return
            for entity in registered_entities:
                if entity.__name__ == potential_entity_type:
                    summon(entity, x, world)
                    break
            else:
                get_game().chat.write(f"The entity '{args[0]}' cannot be found.", MessageType.GAME)

        elif len(args) == 2:
            get_game().chat.write("Argument 'world' is missing.", MessageType.GAME)
        elif len(args) == 1:
            get_game().chat.write("Arguments 'x' and 'world' are missing.", MessageType.GAME)
        elif len(args) == 0:
            get_game().chat.write("Arguments 'entity_type', 'x' and 'world' are missing.", MessageType.GAME)

    @staticmethod
    def speedmode(args: list[str]) -> None:
        """Change the time to day or night.

            :param args: List of args.
            :type args: list[str].

        """
        if not get_game().current_level.main_player.entity.invincible:
            get_game().current_level.main_player.entity.speed = 50
            get_game().chat.write("You are now in fast mode.", MessageType.GAME)
        else:
            get_game().current_level.main_player.entity.speed = 7
            get_game().chat.write("you are now in normal mode.", MessageType.GAME)
        get_game().current_level.main_player.invincible = not get_game().current_level.main_player.entity.invincible

    @staticmethod
    def time_set(args: list[str]) -> None:
        """Change the time to day or night.

            :param args: List of args.
            :type args: list[str].

        """
        if len(args) > 0 and args[0].lower() in ["night", "day"]:
            if args[0].lower() == "night":
                get_game().day_start = time.time() - 20*60
                get_game().chat.write("Now is the night.", MessageType.GAME)
            elif args[0].lower() == "day":
                get_game().day_start = time.time() - 30 * 60
                get_game().chat.write("Now is the day.", MessageType.GAME)
            else:
                get_game().chat.write("You have to choose between day or night.", MessageType.GAME)
        else:
            get_game().chat.write("Argument 'time' is missing.", MessageType.GAME)

    @staticmethod
    def skip_round(args: list[str]) -> None:
        """Skip a round.

            :param args: List of args.
            :type args: list[str].

        """
        get_game().current_level.round_manager.round.finish()
        get_game().chat.write("The round has been passed.", MessageType.GAME)
