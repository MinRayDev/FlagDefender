import os

from core.game import Game


def get_appdata_path():
    return os.getenv("APPDATA")


def get_base_path():
    return os.path.join(os.getenv("APPDATA"), Game.instance.name)


def base_directory_exists():
    return os.path.exists(get_base_path())


def create_base_directory():
    os.mkdir(get_base_path())


def get_save_path():
    return os.path.join(os.getenv("APPDATA"), Game.instance.name, "saves")


def save_directory_exists():
    return os.path.exists(get_save_path())


def create_save_directory():
    os.mkdir(get_save_path())


def get_saves() -> list[str]:
    for file in os.listdir(get_save_path()):
        yield os.path.join(get_save_path(), file)