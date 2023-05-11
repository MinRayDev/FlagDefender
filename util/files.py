import json
import os


def get_appdata_path():
    return os.getenv("APPDATA")


def get_base_path():
    from core.game import Game
    return os.path.join(os.getenv("APPDATA"), Game.name)


def directory_exists(directory_path):
    return os.path.exists(directory_path)


def file_exists(file_path):
    return os.path.isfile(file_path)


def create_directory(directory_path):
    os.mkdir(directory_path)


def get_save_path():
    return os.path.join(get_base_path(), "saves")


def get_saves() -> list[str]:
    for file in os.listdir(get_save_path()):
        yield os.path.join(get_save_path(), file)


def create_settings_file():
    open(os.path.join(get_base_path(), "settings.json"), "x").close()


def get_settings_file() -> str:
    return os.path.join(get_base_path(), "settings.json")


def create_data_file():
    open(os.path.join(get_base_path(), "data.json"), "x").close()


def get_data_file() -> str:
    return os.path.join(get_base_path(), "data.json")


def get_datas() -> dict:
    return json.load(open(get_data_file(), "r"))


def write_datas(datas: dict):
    json.dump(datas, open(get_data_file(), "w+"))
