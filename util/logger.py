import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


def log(content: Any, color: str = "\33[1;97m"):
    try:
        raise Exception()
    except Exception:
        trace_opt = sys.exc_info()[2]
        assert trace_opt is not None
        assert trace_opt.tb_frame is not None
        assert trace_opt.tb_frame.f_back is not None
        code = trace_opt.tb_frame.f_back.f_code
        assert code is not None
        logger_name = f"{Path(code.co_filename).stem}.py/{code.co_name}"
        output = ""
        output += f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] '
        output += f"[{logger_name}]: "
        output += str(content)
        print(color + output + "\33[0;37m")


class LogColors(str, Enum):
    WHITE = "\33[1;97m"
    RED = "\33[0;31m"

