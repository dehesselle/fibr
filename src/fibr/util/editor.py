import logging
import platform
import fibr.config as config

log = logging.getLogger("util")


def get_editor() -> str:
    if not config.exists("editor"):
        match platform.system():
            case "Darwin":
                return config.getStr("editor", "vi")
            case "Linux":
                return config.getStr("editor", "vi")
            case "Windows":
                return config.getStr("editor", "edit.exe")
            case _:
                log.error(f"unknown platform {platform.system()}")
                return "unknown"
    return config.getStr("editor")
