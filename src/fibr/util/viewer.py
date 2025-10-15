import logging
import fibr.config as config
from .platform import is_linux, is_macos, is_windows

log = logging.getLogger("util")


def get_viewer() -> str:
    if not config.exists("viewer"):
        if is_linux():
            return config.getStr("viewer", "less")
        elif is_macos():
            return config.getStr("viewer", "less")
        elif is_windows():
            # https://github.com/walles/moor
            return config.getStr("viewer", "moor.exe")
        else:
            log.error(f"unknown platform")
            return "unknown"
    return config.getStr("viewer")
