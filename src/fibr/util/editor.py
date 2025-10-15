import logging
import fibr.config as config
from .platform import is_linux, is_macos, is_windows

log = logging.getLogger("util")


def get_editor() -> str:
    if not config.exists("editor"):
        if is_linux():
            return config.getStr("editor", "vi")
        elif is_macos():
            return config.getStr("editor", "vi")
        elif is_windows():
            # https://github.com/microsoft/edit
            return config.getStr("editor", "edit.exe")
        else:
            log.error(f"unknown platform")
            return "unknown"
    return config.getStr("editor")
