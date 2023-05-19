import sys
import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


def log(content: Any, color: str = "\33[1;97m", overwrite=False) -> None:
    """Logs a message to the console.

        :param content: The content to log.
        :type content: Any.
        :param color: The color of the log.
        :type color: str.
        :param overwrite: Whether to overwrite the last log.
        :type overwrite: bool.

    """
    if overwrite:
        print("\r", end="", flush=True)

    try:
        raise Exception()
    except:
        # We need to get the traceback object from the exception to get the function name and the file name.
        trace_opt = sys.exc_info()[2]
        code = trace_opt.tb_frame.f_back.f_code
        logger_name = f"{Path(code.co_filename).stem}.py/{code.co_name}"
        output = f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] '
        output += f"[{logger_name}]: "
        output += str(content)
        print(color + output + "\33[0;37m", end="")

    if not overwrite:
        print()


class LogColors(str, Enum):
    """The colors for the log.

        Extends 'str' and 'Enum'.
        :cvar DARK_YELLOW: The dark yellow color.
        :cvar DARK_RED: The dark red color.
        :cvar DARK_GREEN: The dark green color.
        :cvar DARK_BLUE: The dark blue color.
        :cvar DARK_PURPLE: The dark purple color.
        :cvar LIGHT_RED: The light red color.
        :cvar WHITE: The white color.

    """
    DARK_YELLOW: str = "\33[0;33m"
    DARK_RED: str = "\33[0;31m"
    DARK_GREEN: str = "\33[0;32m"
    DARK_BLUE: str = "\33[0;34m"
    DARK_PURPLE: str = "\33[0;95m"

    LIGHT_RED: str = "\33[1;31m"
    WHITE: str = "\033[0;37m"


