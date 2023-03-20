from util.input.controls import Controls
import json


def write_settings(fp):
    settings_dict = {}
    for control in Controls:
        settings_dict[control.name] = control.value
    json.dump(settings_dict, open(fp, "w"), indent=4)


def load_settings(fp):
    settings_dict = json.load(open(fp, "r"))
    for control in settings_dict:
        if getattr(Controls, control).value != settings_dict[control]:
            for key in settings_dict[control]:
                getattr(Controls, control).value[key] = settings_dict[control][key]
