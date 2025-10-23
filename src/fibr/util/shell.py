import logging
import os

import fibr.config as config
from .platform import is_linux, is_macos, is_windows

log = logging.getLogger("util")


def get_shell() -> str:
    if not config.exists("shell"):
        if is_linux():
            if shell := os.getenv("SHELL"):
                return config.getStr("shell", shell)
            else:
                return config.getStr("shell", "sh")
        elif is_macos():
            if shell := os.getenv("SHELL"):
                return config.getStr("shell", shell)
            else:
                return config.getStr("shell", "sh")
        elif is_windows():
            # TODO: default shell on Windows?
            return config.getStr("shell", "cmd.exe")
        else:
            log.error(f"unknown platform")
            return "unknown"
    return config.getStr("shell")
