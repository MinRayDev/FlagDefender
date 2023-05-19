import json

from util.input.controls import Controls


def write_settings(fp: str) -> None:
    """Writes the settings to the given file path.

        :param fp: The file path to write the settings to.
        :type fp: str.

    """
    settings_dict = {}
    for control in Controls:
        settings_dict[control.name] = control.value
    json.dump(settings_dict, open(fp, "w"), indent=4)


def load_settings(fp: str) -> None:
    """Loads the settings from the given file path.

        :param fp: The file path to load the settings from.
        :type fp: str.

    """
    with open(fp, "r") as file:
        try:
            settings_dict = json.load(file)
        except Exception as e:
            write_settings(fp)
            settings_dict = json.load(file)
    for control in settings_dict:
        if getattr(Controls, control).value != settings_dict[control]:
            for key in settings_dict[control]:
                getattr(Controls, control).value[key] = settings_dict[control][key]
