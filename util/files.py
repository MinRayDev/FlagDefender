import os

from util.instance import Game, get_game


def get_appdata_path():
    return os.getenv("APPDATA")


def get_base_path():
    return os.path.join(os.getenv("APPDATA"), Game.instance.name)


def directory_exists(directory_path):
    return os.path.exists(directory_path)


def file_exists(file_path):
    return os.path.isfile(file_path)


def create_directory(directory_path):
    os.mkdir(directory_path)


def get_save_path():
    return os.path.join(os.getenv("APPDATA"), get_game().name, "saves")


def get_saves() -> list[str]:
    for file in os.listdir(get_save_path()):
        yield os.path.join(get_save_path(), file)


def create_settings_file():
    open(os.path.join(get_base_path(), "settings.json"), "x").close()


def get_settings_file() -> str:
    return os.path.join(get_base_path(), "settings.json")
