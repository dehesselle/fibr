# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
import platform

log = logging.getLogger("util")


def is_linux() -> bool:
    return platform.system() == "Linux"


def is_windows() -> bool:
    return platform.system() == "Windows"


def is_macos() -> bool:
    return platform.system() == "Darwin"
