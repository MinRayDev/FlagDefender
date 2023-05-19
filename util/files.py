import json
import os
from typing import Any


def get_appdata_path() -> str:
    """Returns the path to the appdata folder."""
    return os.getenv("APPDATA")


def get_base_path() -> str:
    """Returns the path to the base folder.

        :return: The path to the base folder.
        :rtype: str.

    """
    from core.game import Game
    return os.path.join(os.getenv("APPDATA"), Game.name)


def directory_exists(directory_path: str) -> bool:
    """Returns whether the given directory path exists.

        :param directory_path: The directory path to check.
        :type directory_path: str.

        :return: Whether the given directory path exists.
        :rtype: bool.

    """
    return os.path.exists(directory_path)


def file_exists(file_path: str) -> bool:
    """Returns whether the given file path exists.

        :param file_path: The file path to check.
        :type file_path: str.

        :return: Whether the given file path exists.
        :rtype: bool.

    """
    return os.path.isfile(file_path)


def create_directory(directory_path: str) -> None:
    """Creates the given directory path.

        :param directory_path: The directory path to create.
        :type directory_path: str.

    """
    os.mkdir(directory_path)


def get_save_path() -> str:
    """Returns the path to the save folder.

        :return: The path to the save folder.
        :rtype: str.

    """
    return os.path.join(get_base_path(), "saves")


def get_saves() -> list[str]:
    """Returns the saves.

        :return: The saves.
        :rtype: list[str].

    """
    for file in os.listdir(get_save_path()):
        yield os.path.join(get_save_path(), file)


def create_settings_file() -> None:
    """Creates the settings file."""
    open(os.path.join(get_base_path(), "settings.json"), "x").close()


def get_settings_file() -> str:
    """Returns the path to the settings file.

        :return: The path to the settings file.
        :rtype: str.
    """
    return os.path.join(get_base_path(), "settings.json")


def create_data_file() -> None:
    """Creates the data file."""
    open(os.path.join(get_base_path(), "data.json"), "x").close()


def get_data_file() -> str:
    """Returns the path to the data file.

        :return: The path to the data file.
        :rtype: str.
    """
    return os.path.join(get_base_path(), "data.json")


def get_datas() -> Any:
    """Returns the datas.

        :return: The datas.
        :rtype: Any.
    """
    return json.load(open(get_data_file(), "r"))


def write_datas(datas: dict) -> None:
    """Writes the datas to the data file.

        :param datas: The datas to write.
        :type datas: dict.

    """
    json.dump(datas, open(get_data_file(), "w+"))
