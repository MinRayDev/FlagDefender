from core.chat.chat import MessageType
from util.world_util import teleport, nearest_entity, give_item
from entities.Entity import Entity
from entities.livingentities.entity_player import PlayerEntity
from util.instance import get_game


class Commands:
    @staticmethod
    def tp(args):
        if len(args) != 0 and str(args[0]).lstrip("-").isnumeric():
            x = int(args[0])
            if x is not None and -get_game().main_player.entity.world.size[
                0] <= x and x + get_game().main_player.entity.width <= get_game().main_player.entity.world.size[0]:
                teleport(get_game().main_player.entity, get_game().main_player.entity.world, x)
            else:
                get_game().chat.write("x invalid", MessageType.GAME)
        else:
            get_game().chat.write("x invalid", MessageType.GAME)

    @staticmethod
    def worldtp(args):
        if len(args) != 0:
            for world in get_game().worlds:
                if args[0] == world.name:
                    teleport(get_game().main_player.entity, world, get_game().main_player.entity.x)
        else:
            get_game().chat.write("world invalid", MessageType.GAME)

    @staticmethod
    def kill(args):
        if len(args) != 0:
            to_kill = args[0]
            if to_kill == "@p":
                nearest_entity(get_game().main_player.entity).death()
            elif to_kill == "@a":
                for entity in get_game().main_player.entity.world.entities:
                    entity.death()
            elif to_kill == "@e":
                for entity in get_game().main_player.entity.world.entities:
                    entity.death()
            else:
                try:
                    Entity.get_entity_by_uuid(to_kill).death()
                except ValueError:
                    get_game().chat.write("invalid uuid", MessageType.GAME)
        else:
            get_game().chat.write("missing args", MessageType.GAME)

    @staticmethod
    def get_uuid(args):
        if len(args) != 0:
            to_kill = args[0]
            if to_kill == "@p":
                print(nearest_entity(get_game().main_player.entity).uuid)
            elif to_kill == "@a":
                for entity in get_game().main_player.entity.world.entities:
                    if isinstance(entity, PlayerEntity):
                        print(entity.uuid)
            elif to_kill == "@e":
                for entity in get_game().main_player.entity.world.entities:
                    print(entity.uuid)
            else:
                get_game().chat.write("invalid arg", MessageType.GAME)
        else:
            get_game().chat.write("missing args", MessageType.GAME)

    @staticmethod
    def give(args):
        if len(args) != 0:
            item_ = args[0]
            amount = 1
            if len(args) == 2 and str(args[1]).isnumeric():
                amount = int(args[1])
            if str(item_).isnumeric():
                returned = give_item(item_id=int(item_), amount=amount)
            else:
                returned = give_item(name=str(item_), amount=amount)
            if not returned:
                get_game().chat.write("item not found", MessageType.GAME)
        else:
            get_game().chat.write("missing args", MessageType.GAME)

    @staticmethod
    def clear(args):
        get_game().main_player.inventory.clear()


class OnlineCommands:
    pass
