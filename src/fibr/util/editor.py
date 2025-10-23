# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
import os

import fibr.config as config
from .platform import is_linux, is_macos, is_windows

log = logging.getLogger("util")


def get_editor() -> str:
    if not config.exists("editor"):
        if is_linux():
            if editor := os.gentenv("EDITOR"):
                return config.getStr("editor", editor)
            else:
                return config.getStr("editor", "vi")
        elif is_macos():
            if editor := os.gentenv("EDITOR"):
                return config.getStr("editor", editor)
            else:
                return config.getStr("editor", "vi")
        elif is_windows():
            # https://github.com/microsoft/edit
            return config.getStr("editor", "edit.exe")
        else:
            log.error(f"unknown platform")
            return "unknown"
    return config.getStr("editor")
